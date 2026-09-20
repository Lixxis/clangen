from math import ceil
from random import choice

import i18n
import pygame.transform
import pygame_gui.elements

from scripts.cat.cats import Cat
from scripts.game_structure import image_cache, game, constants
from scripts.ui.elements.relation_display import UIRelationDisplay
from scripts.ui.elements.sprite_button import UISpriteButton
from scripts.ui.elements.image_button import UIImageButton
from scripts.ui.elements.surface_image_button import UISurfaceImageButton
from scripts.ui.theme import get_text_box_theme
from scripts.events_module.text_adjust import shorten_text_to_fit
from scripts.ui.scale import ui_scale, ui_scale_dimensions
from scripts.screens.Screens import Screens
from scripts.screens.enums import GameScreen
from scripts.clan_package.settings import get_clan_setting
from scripts.game_structure.game.settings import game_setting_get
from scripts.game_structure.game.switches import switch_set_value, switch_get_value, Switch
from scripts.game_structure.screen_settings import MANAGER
from scripts.ui.generate_box import get_box, BoxStyles
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.icon import Icon

from scripts.dnd.dnd_types import StatType

def get_leveled_cat():
    "Returns if a cat had a level up or not."
    leveled_cat = []
    for cat_id, cat in Cat.all_cats.items():
        if cat.dead:
            continue
        if cat_id in game.clan.xp and cat.experience_level != game.clan.xp[cat_id]:
            leveled_cat.append(cat)
        if not cat.faded and cat_id not in game.clan.xp:
            game.clan.xp[cat_id] = cat.experience_level
    return leveled_cat


class LevelingScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.back_button = None
        self.selected_cat = None
        self.search_bar = None
        self.search_bar_image = None
        self.cat_buttons = []
        self.page = 1
        self.selected_cat_elements = {}
        self.current_listed_cats = None
        self.previous_search_text = ""
        self.original_cat_stats = None
        self.stat_focus = 0
        self.update_stat = 0
        self.update_skill = 0

        self.skill_start_text = None
        self.skill_buttons = {}
        self.skill_info = {}
        self.skill_modifier = {}
        self.new_proficiency = []

        self.stat_start_text = None
        self.stat_info_obj = {}
        self.stat_info_modifier = {}
        self.increases = {}
        self.stat_inc_buttons = {}
        self.stat_dec_buttons = {}

        self.stat_list = [stat for stat in StatType]
        self.current_skills = None
        self.selected_stat = None
        self.choose_class = False

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            self.mute_button_pressed(event)

            if event.ui_element == self.back_button:
                self.change_screen(game.last_screen_forupdate)
            elif event.ui_element == self.next_page:
                self.page += 1
                self.update_page()
            elif event.ui_element == self.previous_page:
                self.page -= 1
                self.update_page()
            elif event.ui_element == self.next_stat:
                self.stat_focus += 1
                if self.stat_focus > len(StatType) -1:
                    self.stat_focus = 0
                stat = list(StatType)[self.stat_focus].value
                self.stat_focus_button.set_text(f"dnd.stats.{stat}")
                self.update_skill_info()
            elif event.ui_element == self.last_stat:
                self.stat_focus -= 1
                if self.stat_focus < 0:
                    self.stat_focus = len(StatType) - 1
                stat = list(StatType)[self.stat_focus].value
                self.stat_focus_button.set_text(f"dnd.stats.{stat}")
                self.update_skill_info()
            elif event.ui_element in self.skill_buttons.values():
                for skill in self.selected_cat.dnd_skills.skills:
                    if skill not in self.current_skills:
                        continue
                    if event.ui_element == self.skill_buttons[skill.value]:
                        if skill in self.new_proficiency:
                            self.new_proficiency.remove(skill)
                            self.update_skill += 1
                        else:
                            self.new_proficiency.append(skill)
                            self.update_skill -= 1
                self.current_skills = self.selected_cat.dnd_skills.skill_based[self.selected_stat]
                self.update_skill_info()
            elif event.ui_element == self.done_button:
                stats = self.selected_cat.dnd_stats.genetic_stats
                for stat in StatType:
                    self.selected_cat.dnd_stats.genetic_stats[stat] = stats[stat]
                    if stat in self.increases:
                        self.selected_cat.dnd_stats.genetic_stats[stat] += self.increases[stat]
                self.selected_cat.dnd_stats.update_stats()
                self.selected_cat.dnd_skills.proficiency.extend(self.new_proficiency)
                self.selected_cat.dnd_skills.update_skills(self.selected_cat.dnd_stats)
                game.clan.xp[self.selected_cat.ID] = self.selected_cat.experience_level
                self.selected_cat = None
                self.update_selected_cats()
                self.update_list_cats()
            elif event.ui_element in self.stat_dec_buttons.values():
                for stat in StatType:
                    if self.stat_dec_buttons[stat] == event.ui_element:
                        if stat in self.increases:
                            self.increases[stat] -= 1
                        self.update_stat +=1
                self.update_stat_info()
                self.update_skill_info()
            elif event.ui_element in self.stat_inc_buttons.values():
                for stat in StatType:
                    if self.stat_inc_buttons[stat] == event.ui_element:
                        if stat in self.increases:
                            self.increases[stat] += 1
                        else:
                            self.increases[stat] = 1
                        self.update_stat -=1
                self.update_stat_info()
                self.update_skill_info()
            elif event.ui_element in self.cat_buttons:
                if event.ui_element.return_cat_object() != self.selected_cat:
                    self.selected_cat = event.ui_element.return_cat_object()
                    self.update_selected_cats()

    def screen_switches(self):
        super().screen_switches()
        self.show_mute_buttons()

        self.skill_start_text = None
        self.skill_buttons = {}
        self.skill_info = {}
        self.skill_modifier = {}
        self.new_proficiency = []

        self.stat_start_text = None
        self.stat_info_obj = {}
        self.stat_info_modifier = {}
        self.increases = {}
        self.stat_inc_buttons = {}
        self.stat_dec_buttons = {}

        self.stat_list = [stat for stat in StatType]
        self.current_skills = None
        self.selected_stat = None

        self.page = 1

        self.back_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 25), (105, 30))),
            "buttons.back",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

        self.selected_frame = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((50, 80), (200, 350))),
            get_box(BoxStyles.ROUNDED_BOX, (200, 350)),
        )
        self.selected_frame.disable()
        self.skill_frame = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((550, 80), (200, 350))),
            get_box(BoxStyles.ROUNDED_BOX, (200, 350)),
        )
        self.skill_frame.disable()

        self.cat_bg = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((50, 470), (700, 150))),
            get_box(BoxStyles.ROUNDED_BOX, (700, 150)),
        )
        self.cat_bg.disable()

        self.done_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 430), (100, 30))),
            "buttons.done_lower",
            get_button_dict(ButtonStyles.SQUOVAL, (100, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        self.done_button.disable()

        self.next_stat = UIImageButton(
            ui_scale(pygame.Rect((750, 238), (22, 34))), "",
            object_id="#dnd_leveling_next",
            manager=MANAGER,
        )
        
        self.last_stat = UIImageButton(
            ui_scale( pygame.Rect((528, 238), (22, 34))), "",
            object_id="#dnd_leveling_prev",
            manager=MANAGER,
        )

        self.next_page = UISurfaceImageButton(
            ui_scale(pygame.Rect((433, 619), (34, 34))),
            Icon.ARROW_RIGHT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
        )
        self.previous_page = UISurfaceImageButton(
            ui_scale(pygame.Rect((333, 619), (34, 34))),
            Icon.ARROW_LEFT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
        )

        self.search_bar_image = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((55, 625), (118, 34))),
            pygame.image.load("resources/images/search_bar.png").convert_alpha(),
            manager=MANAGER,
        )
        self.search_bar = pygame_gui.elements.UITextEntryLine(
            ui_scale(pygame.Rect((60, 629), (115, 27))),
            object_id="#search_entry_box",
            placeholder_text="general.name_search",
            manager=MANAGER,
        )

        stat = list(StatType)[self.stat_focus].value
        button_dict = get_button_dict(ButtonStyles.DROPDOWN, (200, 30))
        button_dict["disabled"] = button_dict["normal"]
        self.stat_focus_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((550, 80), (200, 30))),
            f"dnd.stats.{stat}",
            button_dict,
            object_id="@buttonstyles_dropdown",
            manager=MANAGER,
        )
        self.stat_focus_button.disable()

        self.update_list_cats()
        self.update_buttons()
        if not self.all_cats_list:
            NoLevelingNeeded()

    def random_cat(self):
        if self.selected_cat_list():
            random_list = [
                i for i in self.all_cats_list if i.ID not in self.selected_cat_list()
            ]
        else:
            random_list = self.all_cats_list
        return choice(random_list)

    def update_list_cats(self):
        self.all_cats_list = [
            i
            for i in get_leveled_cat()
            if i.status.alive_in_player_clan
        ]
        self.all_cats = self.chunks(self.all_cats_list, 24)
        self.current_listed_cats = self.all_cats_list
        self.all_pages = (
            int(ceil(len(self.current_listed_cats) / 24.0))
            if len(self.current_listed_cats) > 24
            else 1
        )
        self.update_page()

    def update_page(self):
        for cat in self.cat_buttons:
            cat.kill()
        self.cat_buttons = []
        if self.page > self.all_pages:
            self.page = self.all_pages
        elif self.page < 1:
            self.page = 1

        if self.page >= self.all_pages:
            self.next_page.disable()
        else:
            self.next_page.enable()

        if self.page <= 1:
            self.previous_page.disable()
        else:
            self.previous_page.enable()

        x = 65
        y = 485
        chunked_cats = self.chunks(self.current_listed_cats, 24)
        if chunked_cats:
            for cat in chunked_cats[self.page - 1]:
                if get_clan_setting("show fav") and cat.favourite:
                    _temp = pygame.transform.scale(
                        pygame.image.load(
                            f"resources/images/fav_marker.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((50, 50)),
                    )

                    self.cat_buttons.append(
                        pygame_gui.elements.UIImage(
                            ui_scale(pygame.Rect((x, y), (50, 50))), _temp
                        )
                    )
                    self.cat_buttons[-1].disable()

                self.cat_buttons.append(
                    UISpriteButton(
                        ui_scale(pygame.Rect((x, y), (50, 50))),
                        cat.sprite,
                        cat_object=cat,
                    )
                )
                x += 55
                if x > 700:
                    y += 55
                    x = 65

    def update_selected_cats(self):
        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}
        self.new_proficiency = []
        self.increases = {}

        self.draw_info_block(self.selected_cat, (50, 80))

        if self.selected_cat:
            self.collect_leveling_need()
            self.update_skill_info()
            self.update_stat_info()
            self.update_class_selection()
        self.update_buttons()

    def draw_info_block(self, cat, starting_pos: tuple):
        if not cat:
            return

        other_cat = [Cat.fetch_cat(i) for i in self.selected_cat_list() if i != cat.ID]
        if other_cat:
            other_cat = other_cat[0]
        else:
            other_cat = None

        tag = str(starting_pos)

        x = starting_pos[0]
        y = starting_pos[1]

        self.selected_cat_elements["cat_image" + tag] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((x + 50, y + 7), (100, 100))),
            pygame.transform.scale(cat.sprite, ui_scale_dimensions((100, 100))),
        )

        name = str(cat.name)
        short_name = shorten_text_to_fit(name, 62, 7)
        self.selected_cat_elements["name" + tag] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((x, y + 100), (200, 30))),
            short_name,
            object_id="#text_box_30_horizcenter",
        )

        # Level information
        current_level = cat.experience_level
        self.selected_cat_elements["current_level" + tag] = pygame_gui.elements.UITextBox(
            f"<b>Current level: {current_level}</b>",
            ui_scale(pygame.Rect((x + 245 , y ), (200, 30))),
            object_id="#text_box_30_horizcenter",
        )
        saved_level = game.clan.xp[cat.ID]
        self.selected_cat_elements["saved_level" + tag] = pygame_gui.elements.UITextBox(
            f"Previous level: {saved_level}",
            ui_scale(pygame.Rect((x + 245 , y + 25), (200, 30))),
            object_id="#text_box_30_horizcenter",
        )

        # Gender
        if cat.genderalign == "female":
            gender_icon = image_cache.load_image(
                "resources/images/female_big.png"
            ).convert_alpha()
        elif cat.genderalign == "male":
            gender_icon = image_cache.load_image(
                "resources/images/male_big.png"
            ).convert_alpha()
        elif cat.genderalign == "trans female":
            gender_icon = image_cache.load_image(
                "resources/images/transfem_big.png"
            ).convert_alpha()
        elif cat.genderalign == "trans male":
            gender_icon = image_cache.load_image(
                "resources/images/transmasc_big.png"
            ).convert_alpha()
        else:
            # Everyone else gets the nonbinary icon
            gender_icon = image_cache.load_image(
                "resources/images/nonbi_big.png"
            ).convert_alpha()

        self.selected_cat_elements["gender" + tag] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((x + 160, y + 12), (25, 25))),
            pygame.transform.scale(gender_icon, ui_scale_dimensions((25, 25))),
        )

        related = False
        # MATE
        if other_cat and len(cat.mate) > 0 and other_cat.ID in cat.mate:
            self.selected_cat_elements["mate_icon" + tag] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((x + 14, y + 14), (22, 20))),
                pygame.transform.scale(
                    image_cache.load_image(
                        "resources/images/heart_big.png"
                    ).convert_alpha(),
                    ui_scale_dimensions((44, 40)),
                ),
            )

        col1 = i18n.t("general.moons_age", count=cat.moons)
        trait = i18n.t(f"cat.personality.{cat.personality.trait}")
        if len(trait) > 15:
            col1 += "\n" + trait[:12] + "..."
        else:
            col1 += "\n" + trait
        self.selected_cat_elements["col1" + tag] = pygame_gui.elements.UITextBox(
            col1,
            ui_scale(pygame.Rect((x + 21, y + 126), (90, -1))),
            object_id="#text_box_22_horizleft_spacing_95",
            manager=MANAGER,
        )
        self.selected_cat_elements["col1" + tag].disable()

        mates = False
        lineage = i18n.t(f"dnd.lineage.{cat.dnd_lineage.lineage_type.value}")
        if len(cat.mate) > 0:
            col2 = i18n.t("general.has_a_mate")
            if other_cat:
                if other_cat.ID in cat.mate:
                    mates = True
                    col2 = i18n.t("general.cats_mate", name=other_cat.name)
        else:
            col2 = i18n.t("general.mate_none")

        if len(lineage) > 15:
            col2 += "\n" + lineage[:12] + "..."
        else:
            col2 += "\n" + lineage


        self.selected_cat_elements["col2" + tag] = pygame_gui.elements.UITextBox(
            col2,
            ui_scale(pygame.Rect((x + 110, y + 126), (80, -1))),
            object_id="#text_box_22_horizleft_spacing_95",
            manager=MANAGER,
        )
        self.selected_cat_elements["col2" + tag].disable()

        # Relation info:
        if related and other_cat and not mates:
            relation = ""
            if cat.is_uncle_aunt(other_cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.niece"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.nephew"
                else:
                    relation = "general.siblings_child"
            elif other_cat.is_uncle_aunt(cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.aunt"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.uncle"
                else:
                    relation = "general.parents_sibling"
            elif other_cat.is_grandparent(cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.grandmother"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.grandfather"
                else:
                    relation = "general.grandparent"
            elif cat.is_grandparent(other_cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.granddaughter"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.grandson"
                else:
                    relation = "general.grandchild"
            elif other_cat.is_parent(cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.mother"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.father"
                else:
                    relation = "general.parent"
            elif cat.is_parent(other_cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.daughter"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.son"
                else:
                    relation = "general.child"
            elif other_cat.is_sibling(cat) or cat.is_sibling(other_cat):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.sister"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.brother"
                else:
                    relation = "general.sibling"

                if other_cat.is_littermate(cat) or cat.is_littermate(other_cat):
                    relation = i18n.t(
                        "general.sibling_littermate", relation=i18n.t(relation)
                    )
            elif not get_clan_setting("first cousin mates") and other_cat.is_cousin(
                cat
            ):
                if other_cat.genderalign in ("female", "trans female"):
                    relation = "general.cousin_female"
                elif other_cat.genderalign in ("male", "trans male"):
                    relation = "general.cousin_male"
                else:
                    relation = "general.cousin_nb"

            self.selected_cat_elements[
                "col2_relation" + tag
            ] = pygame_gui.elements.UITextBox(
                i18n.t("general.related_text"),
                ui_scale(pygame.Rect((x + 110, -15), (80, -1))),
                starting_height=3,
                object_id="#text_box_22_horizleft_spacing_95",
                manager=MANAGER,
                anchors={"top_target": self.selected_cat_elements["col2" + tag]},
            )
            self.selected_cat_elements["col2_relation" + tag].set_tooltip(
                text=i18n.t(relation)
            )
            self.selected_cat_elements["col2_relation" + tag].tool_tip_delay = 0
            self.selected_cat_elements["col2_relation" + tag].disable()

    def update_skill_info(self):
        self.selected_stat = self.stat_list[self.stat_focus]
        self.current_skills = self.selected_cat.dnd_skills.skill_based[self.selected_stat]
        for skill in self.skill_buttons.keys():
            self.skill_buttons[skill].kill()
        self.skill_buttons = {}
        for skill in self.skill_info.keys():
            self.skill_info[skill].kill()
        self.skill_info = {}
        for skill in self.skill_modifier.keys():
            self.skill_modifier[skill].kill()
        self.skill_modifier = {}

        if self.skill_start_text:
            self.skill_start_text.kill()
        self.skill_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_skill),
            ui_scale(pygame.Rect((600, 120), (100, 35))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER
        )

        text_pos_x = 590
        button_pos_x = text_pos_x - 23

        text_pos_y = 140
        button_pos_y = text_pos_y + 8
        step_increase = 25

        skills = self.selected_cat.dnd_skills.skills
        proficiency = self.selected_cat.dnd_skills.proficiency
        for skill in skills:
            if skill not in self.current_skills:
                continue
            text = i18n.t(f"dnd.skills.{skill.value}")
            object_id = "#dnd_prof_free"
            if skill in proficiency:
                object_id = "#dnd_prof"
                text = "<b><i>" +  text + "</i></b>"
            elif skill in self.new_proficiency:
                object_id = "#dnd_prof_selected"


            modifier = skills[skill]
            stat_based_on = [stat for stat in StatType if skill in self.selected_cat.dnd_skills.skill_based[stat]][0]
            if stat_based_on in self.increases:
                new_stat_number = self.selected_cat.dnd_stats.stats[stat_based_on] + self.increases[stat_based_on]
                modifier = self.selected_cat.dnd_stats.modifier[new_stat_number]
                modifier += constants.DND_CONFIG["proficiency_bonus"] if skill in self.selected_cat.dnd_skills.proficiency else 0
            if skill in self.new_proficiency:
                modifier += constants.DND_CONFIG["proficiency_bonus"]
            addition = 23
            if modifier < 0:
                addition += 2
            self.skill_info[skill.value] = pygame_gui.elements.UITextBox(
                text,
                ui_scale(pygame.Rect((text_pos_x + 23, text_pos_y), (140, 40))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER
            )
            self.skill_buttons[skill.value] = UIImageButton(
                ui_scale(pygame.Rect((button_pos_x, button_pos_y), (22, 22))), "",
                object_id=object_id, 
                manager=MANAGER
            )
            if modifier >= 0:
                modifier = "+" + str(modifier)
            else:
                modifier = str(skills[skill])
            self.skill_modifier[skill.value] = pygame_gui.elements.UITextBox(
                modifier,
                ui_scale(pygame.Rect((text_pos_x, text_pos_y), (140, 40))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER
            )
            if skill in proficiency or (self.update_skill <= 0 and skill not in self.new_proficiency):
                self.skill_buttons[skill.value].disable()
            text_pos_y += step_increase
            button_pos_y += step_increase

        self.update_buttons()

    def update_stat_info(self):
        stats = self.selected_cat.dnd_stats.stats
        text_pos_x = 270
        button_pos_x_decr = text_pos_x + 180 + 5 
        button_pos_x_incr = text_pos_x + 180 + 5 + 22 + 5

        text_pos_y = 190
        button_pos_y = text_pos_y + 8
        step_increase = 24

        if self.stat_start_text:
            self.stat_start_text.kill()
        self.stat_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_stat),
            ui_scale(pygame.Rect((text_pos_x, text_pos_y - 20), (100, 35))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER
        )

        for stat in StatType:
            # STAT INFO
            if stat in self.stat_info_obj:
                self.stat_info_obj[stat].kill()
            name = i18n.t(f"dnd.stats.{stat.value}_upper")
            text = f"{name}: " + str(stats[stat])
            if stat in self.increases:
                text = f"{name}: " + str(stats[stat] + self.increases[stat])
            self.stat_info_obj[stat] = pygame_gui.elements.UITextBox(
                text,
                ui_scale(pygame.Rect((text_pos_x, text_pos_y), (150, 35))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )

            # INCREASE
            if stat in self.stat_inc_buttons:
                self.stat_inc_buttons[stat].kill()
            self.stat_inc_buttons[stat] = UIImageButton(
                ui_scale(pygame.Rect((button_pos_x_incr, button_pos_y), (22, 22))), "",
                object_id="#dnd_stats_add",
                manager=MANAGER,
            )

            # DECREASE
            if stat in self.stat_dec_buttons:
                self.stat_dec_buttons[stat].kill()
            self.stat_dec_buttons[stat] = UIImageButton(ui_scale(
                pygame.Rect((button_pos_x_decr, button_pos_y), (22, 22))), "",
                object_id="#dnd_stats_sub",
                manager=MANAGER,
            )

            # ACTIVATE OR DEACTIVATE
            if stat in self.increases:
                if self.increases[stat] == 0:
                    self.stat_dec_buttons[stat].disable()
            else:
                self.increases[stat] = 0
                self.stat_dec_buttons[stat].disable()
            if self.update_stat < 1:
                self.stat_inc_buttons[stat].disable()

            # MODIFIER
            if stat in self.stat_info_modifier:
                self.stat_info_modifier[stat].kill()
            current_stat_value = self.selected_cat.dnd_stats.stats[stat]
            if stat in self.increases:
                current_stat_value += self.increases[stat]
            modifier = self.selected_cat.dnd_stats.modifier[current_stat_value]
            text = "(" + str(modifier) + ")"
            if modifier >= 0:
                text = "(+" + str(modifier) + ")"
            self.stat_info_modifier[stat] = pygame_gui.elements.UITextBox(
                text,
                ui_scale(pygame.Rect((text_pos_x + 139, text_pos_y), (50, 40))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )
            text_pos_y += step_increase
            button_pos_y += step_increase

        self.update_buttons()

    def update_class_selection(self):
        if self.choose_class:
            print("Choosing class...")
        if self.selected_cat.dnd_class:
            print("Class already selected")

    def selected_cat_list(self):
        output = []
        if self.selected_cat:
            output.append(self.selected_cat.ID)

        return output

    def update_buttons(self):
        if self.selected_cat:
            if self.update_stat > 0 or self.update_skill > 0:
                self.done_button.disable()
            else:
                self.done_button.enable()
        else:
            self.done_button.disable()

    def update_search_cats(self, search_text):
        """Run this function when the search text changes, or when the screen is switched to."""
        self.current_listed_cats = []
        Cat.sort_cats(self.all_cats_list)

        search_text = search_text.strip()
        if search_text not in (""):
            for cat in self.all_cats_list:
                if search_text.lower() in str(cat.name).lower():
                    self.current_listed_cats.append(cat)
        else:
            self.current_listed_cats = self.all_cats_list.copy()

        self.all_pages = (
            int(ceil(len(self.current_listed_cats) / 24.0))
            if len(self.current_listed_cats) > 24
            else 1
        )

        Cat.ordered_cat_list = self.current_listed_cats
        self.update_page()

    def collect_leveling_need(self):
        self.update_stat = 0
        self.update_skill = 0
        self.choose_class = False

        end_level_number = int(self.selected_cat.experience_level.split(" ")[1])
        start_level_number = end_level_number
        saved_level_number = int(game.clan.xp[self.selected_cat.ID].split(" ")[1])
        if start_level_number > saved_level_number:
            start_level_number = saved_level_number
        for level in constants.DND_CONFIG["leveling"].keys():
            current_level_number = int(level.split(" ")[1])
            if start_level_number <= current_level_number and constants.DND_CONFIG["leveling"][level]:
                info = constants.DND_CONFIG["leveling"][level].split(":")
                if info == constants.DND_CONFIG["choosing_class"]:
                    self.choose_class = True
                lvl_type = info[0]
                amount = info[1]
                if lvl_type == "stat":
                    self.update_stat += int(amount)
                if lvl_type == "skill":
                    self.update_skill += int(amount)
            if current_level_number == end_level_number:
                break

    def exit_screen(self):
        self.selected_cat = None

        for cat in self.cat_buttons:
            cat.kill()
        self.cat_buttons = []

        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}

        self.back_button.kill()
        del self.back_button
        self.selected_frame.kill()
        del self.selected_frame
        self.skill_frame.kill()
        del self.skill_frame
        self.cat_bg.kill()
        del self.cat_bg
        self.done_button.kill()
        del self.done_button
        self.last_stat.kill()
        del self.last_stat
        self.next_stat.kill()
        del self.next_stat
        self.stat_focus_button.kill()
        del self.stat_focus_button
        if self.skill_start_text:
            self.skill_start_text.kill()
            del self.skill_start_text
        if self. stat_start_text:
            self.stat_start_text.kill()
            del self.stat_start_text
        for skill in self.skill_buttons.keys():
            self.skill_buttons[skill].kill()
        del self.skill_buttons
        for skill in self.skill_info.keys():
            self.skill_info[skill].kill()
        del self.skill_info
        for skill in self.skill_modifier.keys():
            self.skill_modifier[skill].kill()
        del self.skill_modifier
        for stat in self.stat_info_obj.keys():
            self.stat_info_obj[stat].kill()
        del self.stat_info_obj
        for stat in self.stat_info_modifier.keys():
            self.stat_info_modifier[stat].kill()
        del self.stat_info_modifier
        for stat in self.stat_inc_buttons.keys():
            self.stat_inc_buttons[stat].kill()
        del self.stat_inc_buttons
        for stat in self.stat_dec_buttons.keys():
            self.stat_dec_buttons[stat].kill()
        del self.stat_dec_buttons
        self.next_page.kill()
        del self.next_page
        self.previous_page.kill()
        del self.previous_page
        self.search_bar_image.kill()
        del self.search_bar_image
        self.search_bar.kill()
        del self.search_bar

    def on_use(self):
        super().on_use()
        # Only update the positions if the search text changes
        if self.search_bar.is_focused and self.search_bar.get_text() == "name search":
            self.search_bar.set_text("")
        if self.search_bar.get_text() != self.previous_search_text:
            self.update_search_cats(self.search_bar.get_text())
        self.previous_search_text = self.search_bar.get_text()


import pygame
import pygame_gui

from scripts.ui.elements.text_box_tweaked import UITextBoxTweaked
from scripts.ui.windows.window_base_class import GameWindow


class NoLevelingNeeded(GameWindow):
    def __init__(self):
        super().__init__(
            ui_scale(pygame.Rect((300, 200), (250, 170))),
            window_display_title="No Leveling Needed",
            click_outside_to_close=False,
        )

        self.missing_info = UITextBoxTweaked(
            "windows.no_leveling",
            ui_scale(pygame.Rect((0, 30), (220, -1))),
            line_spacing=1,
            manager=MANAGER,
            object_id="#text_box_30_horizcenter",
            container=self,
            anchors={
                "centerx": "centerx",
            },
        )

        self.return_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((0, 100), (105, 30))),
            "buttons.back",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
            container=self,
            anchors={"centerx": "centerx"},
        )


    def process_event(self, event) -> bool:
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in (self.return_button, self.back_button):
                switch_set_value(Switch.cur_screen, game.last_screen_forupdate)
                game.last_screen_forupdate = GameScreen.LEVELING
                game.switch_screens = True
                self.kill()

        return super().process_event(event)
