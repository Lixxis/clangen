import pygame
import pygame_gui

from re import sub
from scripts.dnd.dnd_types import StatType, ClassType
from scripts.utility import scale
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.ui_elements import (
    UISpriteButton,
    UIImageButton,
    UITextBoxTweaked,
)
from scripts.utility import get_text_box_theme, scale, shorten_text_to_fit
from scripts.dnd.dnd_skills import DnDSkills
from scripts.dnd.dnd_stats import Stats

from .Screens import Screens

def get_leveled_cat():
    "Returns if a cat had a level up or not."
    leveled_cat = []
    print(game.clan.xp.keys())
    for cat_id, cat in Cat.all_cats.items():
        if cat.dead or cat.outside:
            continue
        if cat_id in game.clan.xp and cat.experience_level != game.clan.xp[cat_id]:
            leveled_cat.append(cat)
        if not cat.faded and cat_id not in game.clan.xp:
            print("NEW CAT!", cat.name)
            game.clan.xp[cat_id] = "level 0"
            leveled_cat.append(cat)
    return leveled_cat

def update_levels(leveled_cats):
    "Updates the levels of the given cats in the overall game xp documentation."
    for cat in leveled_cats:
        game.clan.xp[cat.ID] = cat.experience_level

class DnDLevelScreen(Screens):
    elements = {}
    focus_cat = None
    focus_cat_object = None
    focus_info = None
    focus_name = None
    focus_info1 = None
    focus_info2 = None
    back_button = None
    cat_buttons = {}
    cat_names = []

    next_button = None
    prev_button = None

    stat_info_obj = {}
    stat_info_modifier = {}
    increases = {}
    stat_inc_buttons = {}
    stat_dec_buttons = {}
    stat_start_text = None

    skill_pos_y = 90
    skill_pos_x = 530
    skill_width = 380
    skill_length = 430
    skill_start_text = None
    skill_buttons = {}
    skill_info = {}
    skill_modifier = {}
    new_proficiency = []

    class_buttons = {}
    class_info = {}

    update_skill = 0
    update_stat = 0
    level_class = False
    new_class = []
    stat_list = [stat for stat in StatType]
    selected_stat_idx = 0
    selected_stat = stat_list[selected_stat_idx]
    current_skills = DnDSkills().skill_based[selected_stat]

    def screen_switches(self):
        self.hide_menu_buttons()
        
        self.cat_bg = pygame_gui.elements.UIImage(
            scale(pygame.Rect((280, 880), (1120, 400))),
            pygame.image.load("resources/images/sick_hurt_bg.png").convert_alpha(),
            manager=MANAGER,
        )
        self.cat_bg.disable()
        self.back_button = UIImageButton(
            scale(pygame.Rect((50, 50), (210, 60))),
            "",
            object_id="#back_button",
            manager=MANAGER,
        )
        self.last_page = UIImageButton(
            scale(pygame.Rect((660, 1275), (68, 68))),
            "",
            object_id="#arrow_left_button",
            manager=MANAGER,
        )
        self.next_page = UIImageButton(
            scale(pygame.Rect((952, 1275), (68, 68))),
            "",
            object_id="#arrow_right_button",
            manager=MANAGER,
        )
        self.done_button = UIImageButton(
            scale(pygame.Rect((1100, 800), (154, 60))), "",
            object_id="#done_button",
            manager=MANAGER,
        )
        self.done_button.disable()

        self.elements["level_profile"] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((80, 150), (384, 478))),
                pygame.transform.scale(
                    pygame.image.load(
                        f"resources/images/dnd/leveling_profile.png").convert_alpha(),
                        (384, 478)
                    ),
                manager=MANAGER,
            )

        self.stop_focus_button = UIImageButton(
            scale(pygame.Rect((80 + 384 + 4, 150 + 2), (44, 44))),
            "",
            object_id="#exit_window_button",
            manager=MANAGER,
        )
        self.stop_focus_button.hide()
        
        arrow_width = 44
        arrow_length = 68

        for stat in StatType:
            if stat.value == "constitution":
                continue
            self.elements[stat] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((self.skill_pos_x, self.skill_pos_y), (self.skill_width, self.skill_length))),
                pygame.transform.scale(
                    pygame.image.load(
                        f"resources/images/dnd/skill_based_{stat.value}.png").convert_alpha(),
                        (self.skill_width, self.skill_length)
                    ),
                manager=MANAGER,
            )
            if stat.value != self.selected_stat.value:
                self.elements[stat].hide()

        self.next_button = UIImageButton(
            scale(pygame.Rect((self.skill_pos_x + self.skill_width, self.skill_pos_y + self.skill_length/2 - arrow_length/2), (arrow_width, arrow_length))), "",
            object_id="#dnd_lvl_next",
            manager=MANAGER,
        )
        self.next_button.disable()
        self.prev_button = UIImageButton(
            scale(pygame.Rect((self.skill_pos_x - arrow_width, self.skill_pos_y + self.skill_length/2 - arrow_length/2), (arrow_width, arrow_length))), "",
            object_id="#dnd_lvl_prev",
            manager=MANAGER,
        )
        self.prev_button.disable()

        self.current_page = 1
        self.update_leveling_cats()
        self.update_skill_info()
        self.update_class()
        self.update_stat_info()

    def update_focus_cat(self):
        if not self.focus_cat_object:
            return
        self.clear_cat_infos()
        self.collect_leveling_need()
        self.stop_focus_button.show()

        self.focus_name = pygame_gui.elements.UITextBox(
            f"<b>- {self.focus_cat_object.name} leveled up ({self.focus_cat_object.experience_level}) -</b>",
            scale(pygame.Rect((30, 30), (1600, 80))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            )


        self.focus_cat = pygame_gui.elements.UIImage(
            scale(pygame.Rect((130, 150), (300, 300))),
            pygame.transform.scale(self.focus_cat_object.sprite,(300, 300)),
            manager=MANAGER,
        )
        cat_information = self.focus_cat_object.genderalign + "<br>"
        cat_information += str(self.focus_cat_object.moons) + " moons <br>"
        cat_information += self.focus_cat_object.age + "<br>"
        self.focus_info1 = pygame_gui.elements.UITextBox(
            f"{cat_information}",
            scale(pygame.Rect((90, 460), (200, 200))),
            object_id="#text_box_30_horizcenter_spacing_95_light",
            manager=MANAGER,
        )
        cat_information = self.focus_cat_object.dnd_linage.linage_type.value + "<br>"
        cat_information += self.focus_cat_object.personality.trait + "<br>"
        self.focus_info2 = pygame_gui.elements.UITextBox(
            f"{cat_information}",
            scale(pygame.Rect((90 + 190, 460), (200, 200))),
            object_id="#text_box_30_horizcenter_spacing_95_light",
            manager=MANAGER,
        )

        self.update_stat_info()
        self.update_skill_info()
        self.update_class()

    def update_skill_info(self):
        self.clear_skill_buttons()
        if not self.focus_cat_object:
            return

        for key in self.elements.keys():
            if key == self.selected_stat or key == "cat_bg" or key == "level_profile":
                self.elements[key].show()
            else:
                self.elements[key].hide()

        text_pos_x = self.skill_pos_x + 70
        button_pos_x = text_pos_x - 46

        text_pos_y = self.skill_pos_y + 80
        button_pos_y = text_pos_y + 17
        step_increase = 50

        if self.skill_start_text:
            self.skill_start_text.kill()
        self.skill_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_skill),
            scale(pygame.Rect((text_pos_x, text_pos_y-30), (200, 70))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER,
            )

        skills = DnDSkills().skills
        if self.focus_cat_object:
            skills = self.focus_cat_object.dnd_skills.skills
        proficiency = DnDSkills().proficiency
        if self.focus_cat_object:
            proficiency = self.focus_cat_object.dnd_skills.proficiency
        for skill in skills:
            if skill not in self.current_skills:
                continue
            text = skill.value
            object_id = "#dnd_prof_free"
            if skill in proficiency:
                object_id = "#dnd_prof"
                text = "<b><i>" + text + "</i></b>"
            elif skill in self.new_proficiency:
                object_id = "#dnd_prof_selected"

            modifier = skills[skill]
            stat_based_on = None
            if self.focus_cat_object:
                stat_based_on = [stat for stat in StatType if skill in self.focus_cat_object.dnd_skills.skill_based[stat]][0]
            if stat_based_on in self.increases:
                new_stat_number = self.focus_cat_object.dnd_stats.stats[stat_based_on] + self.increases[stat_based_on]
                modifier = self.focus_cat_object.dnd_stats.modifier[new_stat_number]
                modifier += game.dnd_config["proficiency_bonus"] if skill in self.focus_cat_object.dnd_skills.proficiency else 0
                modifier += game.dnd_config["proficiency_bonus"] if skill in self.focus_cat_object.dnd_skills.class_proficiency else 0
            if skill in self.new_proficiency:
                modifier += game.dnd_config["proficiency_bonus"]
            addition = 46
            if modifier < 0:
                addition += 5
            self.skill_info[skill.value] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x + 46, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
                )
            self.skill_buttons[skill.value] = UIImageButton(scale(pygame.Rect((button_pos_x, button_pos_y), (44, 44))), "", 
                                            object_id=object_id, 
                                            manager=MANAGER,
                                            )
            if modifier >= 0:
                modifier = "+" + str(modifier)
            else:
                modifier = str(skills[skill])
            self.skill_modifier[skill.value] = pygame_gui.elements.UITextBox(
                modifier,
                scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )
            if skill in proficiency or (self.update_skill <= 0 and skill not in self.new_proficiency):
                self.skill_buttons[skill.value].disable()
            text_pos_y += step_increase
            button_pos_y += step_increase

        if not self.focus_cat_object or self.update_stat > 0 or self.update_skill > 0 or (len(self.new_class) <= 0 and self.level_class):
            self.done_button.disable()
        else:
            self.done_button.enable()

    def update_leveling_cats(self):
        """
        set tab showing as either self.hungry_cats or self.satisfied_cats; whichever one you want to
        display and update
        """
        self.clear_cat_buttons()
        tab_list = get_leveled_cat()

        if not tab_list:
            all_pages = []
        else:
            all_pages = self.chunks(tab_list, 10)

        self.current_page = max(1, min(self.current_page, len(all_pages)))

        # Check for empty list (no cats)
        if all_pages:
            self.display_cats = all_pages[self.current_page - 1]
        else:
            self.display_cats = []

        # Update next and previous page buttons
        if len(all_pages) <= 1:
            self.next_page.disable()
            self.last_page.disable()
        else:
            if self.current_page >= len(all_pages):
                self.next_page.disable()
            else:
                self.next_page.enable()

            if self.current_page <= 1:
                self.last_page.disable()
            else:
                self.last_page.enable()

        pos_x = 350
        pos_y = 920
        i = 0
        for cat in self.display_cats:
            self.cat_buttons["able_cat" + str(i)] = UISpriteButton(
                scale(pygame.Rect((pos_x, pos_y), (100, 100))),
                cat.sprite,
                cat_object=cat,
                manager=MANAGER,
                starting_height=2,
            )

            name = str(cat.name)
            short_name = shorten_text_to_fit(name, 185, 30)
            self.cat_names.append(
                pygame_gui.elements.UITextBox(
                    short_name,
                    scale(pygame.Rect((pos_x - 60, pos_y + 100), (220, 60))),
                    object_id="#text_box_30_horizcenter",
                    manager=MANAGER,
                )
            )

            pos_x += 200
            if pos_x >= 1340:
                pos_x = 350
                pos_y += 160
            i += 1

    def update_class(self):
        if not self.focus_cat_object:
            return
        self.clear_class_buttons()

        for key in self.elements.keys():
            if key == self.selected_stat or key == "cat_bg" or key == "level_profile":
                self.elements[key].show()
            else:
                self.elements[key].hide()

        text_pos_x = self.skill_pos_x + 500
        button_pos_x = text_pos_x - 12

        text_pos_y = self.skill_pos_y
        button_pos_y = text_pos_y + 17
        step_increase = 55

        for dnd_class in ClassType:
            text = dnd_class.value
            object_id = "#dnd_prof_free"
            if dnd_class == self.focus_cat_object.dnd_class:
                object_id = "#dnd_prof"
                text = "<b><i>" + text + "</i></b>"
            elif dnd_class in self.new_class:
                object_id = "#dnd_prof_selected"

            self.class_info[dnd_class.value] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x + 46, text_pos_y), (400, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
                )
            self.class_buttons[dnd_class.value] = UIImageButton(scale(pygame.Rect((button_pos_x, button_pos_y), (44, 44))), "", 
                                            object_id=object_id,
                                            tool_tip_text=self.focus_cat_object.dnd_skills.class_prof_description[dnd_class],
                                            manager=MANAGER,
                                            )
            if self.focus_cat_object.dnd_class or (len(self.new_class) > 0 and dnd_class not in self.new_class) or not self.level_class:
                self.class_buttons[dnd_class.value].disable()
            if dnd_class == ClassType.BLOOD_CHOSEN:
                self.class_buttons[dnd_class.value].disable()

            text_pos_y += step_increase
            button_pos_y += step_increase

        if not self.focus_cat_object or self.update_stat > 0 or self.update_skill > 0 or (len(self.new_class) <= 0 and self.level_class):
            self.done_button.disable()
        else:
            self.done_button.enable()

    def update_stat_info(self):
        self.clear_stats_buttons()
        stats = Stats().stats
        if self.focus_cat_object:
            stats = self.focus_cat_object.dnd_stats.stats
        text_pos_x = self.skill_pos_x - 33
        button_pos_x_decr = text_pos_x + 360
        button_pos_x_incr = text_pos_x + 410

        text_pos_y = self.skill_pos_y + self.skill_length + 20
        button_pos_y = text_pos_y + 17
        step_increase = 52
        if self.stat_start_text:
            self.stat_start_text.kill()
        self.stat_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_stat),
            scale(pygame.Rect((text_pos_x, text_pos_y-30), (250, 80))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER,
        )

        for stat in StatType:
            # STAT INFO
            if stat in self.stat_info_obj:
                self.stat_info_obj[stat].kill()
            name = stat.value.upper()
            text = f"{name}: " + str(stats[stat])
            if stat in self.increases:
                text = f"{name}: " + str(stats[stat] + self.increases[stat])
            self.stat_info_obj[stat] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )

            # INCREASE
            if stat in self.stat_inc_buttons:
                self.stat_inc_buttons[stat].kill()
            self.stat_inc_buttons[stat] = UIImageButton(
                scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                object_id="#dnd_stats_add",
                manager=MANAGER,
            )

            # DECREASE
            if stat in self.stat_dec_buttons:
                self.stat_dec_buttons[stat].kill()
            self.stat_dec_buttons[stat] = UIImageButton(scale(
                pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
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
            current_stat_value = Stats().stats[stat]
            if self.focus_cat_object:
                current_stat_value = self.focus_cat_object.dnd_stats.stats[stat]
            if stat in self.increases:
                current_stat_value += self.increases[stat]
            modifier = 0
            if self.focus_cat_object:
                modifier = self.focus_cat_object.dnd_stats.modifier[current_stat_value]
            text = "(" + str(modifier) + ")"
            if modifier >= 0:
                text = "(+" + str(modifier) + ")"
            self.stat_info_modifier[stat] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x + 278, text_pos_y), (100, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )
            text_pos_y += step_increase
            button_pos_y += step_increase

        if not self.focus_cat_object or self.update_stat > 0 or self.update_skill > 0 or (len(self.new_class) < 0 and self.level_class):
            self.done_button.disable()
        else:
            self.done_button.enable()

    def exit_screen(self):
        self.cat_bg.kill()
        self.back_button.kill()
        self.last_page.kill()
        self.next_page.kill()
        self.done_button.kill()
        self.next_button.kill()
        self.prev_button.kill()
        self.stop_focus_button.kill()
        self.clear_cat_buttons()
        self.clear_skill_buttons()
        self.clear_cat_infos()
        self.clear_stats_buttons()
        if self.skill_start_text:
            self.skill_start_text.kill()
        if self.elements:
            for id, element in self.elements.items():
                self.elements[id].kill()
            self.elements = {}
        if self.focus_cat:
            self.focus_cat.kill()
        if self.focus_info:
            self.focus_info.kill()
        if self.focus_name:
            self.focus_name.kill()
        for dnd_class in self.class_buttons.keys():
            self.class_buttons[dnd_class].kill()
        self.class_buttons = {}
        for dnd_class in self.class_info.keys():
            self.class_info[dnd_class].kill()
        self.class_info = {}
        if self.focus_cat:
            self.focus_cat = None
        if self.focus_cat_object:
            self.focus_cat_object = None

    def collect_leveling_need(self):
        self.update_stat = 0
        self.update_skill = 0
        self.level_class = False
        start_level_number = int(self.focus_cat_object.experience_level.split(" ")[1])
        end_level_number = int(self.focus_cat_object.experience_level.split(" ")[1])
        if not self.focus_cat_object.dnd_class and start_level_number >= int(game.dnd_config["choosing_class"].split(" ")[1]):
            self.level_class = True
        if start_level_number > int(game.clan.xp[self.focus_cat_object.ID].split(" ")[1]):
            start_level_number = int(game.clan.xp[self.focus_cat_object.ID].split(" ")[1])
        elif end_level_number == int(game.clan.xp[self.focus_cat_object.ID].split(" ")[1]):
            return
        for level in game.dnd_config["leveling"].keys():
            current_level_number = int(level.split(" ")[1])
            if start_level_number <= current_level_number and game.dnd_config["leveling"][level]:
                info = game.dnd_config["leveling"][level].split(":")
                lvl_type = info[0]
                amount = info[1]
                if lvl_type == "stat":
                    self.update_stat += int(amount)
                if lvl_type == "skill":
                    self.update_skill += int(amount)
            if current_level_number == end_level_number:
                break

    def reset_skill(self):
        if len(self.new_class) > 0:
            self.new_class = []
        if len(self.increases) > 0:
            self.increases = {}
        if len(self.new_proficiency) > 0:
            self.new_proficiency = []

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen(game.last_screen_forupdate)
            elif event.ui_element == self.next_page:
                self.current_page += 1
                self.update_leveling_cats()
            elif event.ui_element == self.last_page:
                self.current_page -= 1
                self.update_leveling_cats()
            elif (
                event.ui_element in self.cat_buttons.values()
                and event.ui_element != self.focus_cat
            ):
                self.focus_cat_object = event.ui_element.return_cat_object()
                self.reset_skill()
                self.update_focus_cat()
                self.next_button.enable()
                self.prev_button.enable()
            if event.ui_element == self.stop_focus_button:
                self.stop_focus_button.hide()
                self.focus_cat_object = None
                if self.skill_start_text:
                    self.skill_start_text.kill()
                self.clear_cat_infos()
                self.reset_skill()
                self.next_button.disable()
                self.prev_button.disable()
            elif event.ui_element == self.done_button:
                stats = self.focus_cat_object.dnd_stats.genetic_stats
                for stat in StatType:
                    self.focus_cat_object.dnd_stats.genetic_stats[stat] = stats[stat]
                    if stat in self.increases:
                        self.focus_cat_object.dnd_stats.genetic_stats[stat] += self.increases[stat]
                self.focus_cat_object.dnd_stats.update_stats()
                self.focus_cat_object.dnd_skills.proficiency.extend(self.new_proficiency)
                self.focus_cat_object.dnd_skills.update_skills(self.focus_cat_object.dnd_stats)
                if self.level_class and len(self.new_class) > 0:
                    self.focus_cat_object.dnd_class = self.new_class[0]
                    self.focus_cat_object.dnd_skills.update_class_proficiency(self.focus_cat_object.dnd_class, self.focus_cat_object.experience_level)
                update_levels([self.focus_cat_object])
                self.focus_cat_object = None
                self.update_skill = 0
                self.update_stat = 0
                self.clear_cat_infos()
                self.reset_skill()
                self.update_leveling_cats()
            elif event.ui_element in self.skill_buttons.values():
                for skill in self.focus_cat_object.dnd_skills.skills:
                    if skill not in self.current_skills:
                        continue
                    if event.ui_element == self.skill_buttons[skill.value]:
                        if skill in self.new_proficiency:
                            self.new_proficiency.remove(skill)
                            self.update_skill += 1
                        else:
                            self.new_proficiency.append(skill)
                            self.update_skill -= 1
                self.current_skills = self.focus_cat_object.dnd_skills.skill_based[self.selected_stat]
                self.update_skill_info()
            elif event.ui_element in self.class_buttons.values():
                for dnd_class in ClassType:
                    if event.ui_element == self.class_buttons[dnd_class.value]:
                        if dnd_class in self.new_class:
                            self.new_class.remove(dnd_class)
                        else:
                            self.new_class.append(dnd_class)
                self.update_class()
            elif event.ui_element == self.next_button:
                next_idx = self.selected_stat_idx + 1
                if next_idx >= len(StatType):
                    next_idx = 0
                self.selected_stat_idx = next_idx
                self.selected_stat = self.stat_list[self.selected_stat_idx]
                if self.selected_stat == StatType.CONSTITUTION:
                    next_idx = self.selected_stat_idx + 1
                    if next_idx >= len(StatType):
                        next_idx = 0
                    self.selected_stat_idx = next_idx
                    self.selected_stat = self.stat_list[self.selected_stat_idx]
                self.current_skills = self.focus_cat_object.dnd_skills.skill_based[self.selected_stat]
                self.update_skill_info()
            elif event.ui_element == self.prev_button:
                prev_idx = self.selected_stat_idx - 1
                if prev_idx < -1:
                    prev_idx = len(self.stat_list) - 2
                self.selected_stat_idx = prev_idx
                self.selected_stat = self.stat_list[self.selected_stat_idx]
                if self.selected_stat == StatType.CONSTITUTION:
                    prev_idx = self.selected_stat_idx - 1
                    if prev_idx < -1:
                        prev_idx = len(self.stat_list) - 2
                    self.selected_stat_idx = prev_idx
                    self.selected_stat = self.stat_list[self.selected_stat_idx]
                self.current_skills = self.focus_cat_object.dnd_skills.skill_based[self.selected_stat]
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
            elif event.ui_element in self.stat_dec_buttons.values():
                for stat in StatType:
                    if self.stat_dec_buttons[stat] == event.ui_element:
                        if stat in self.increases:
                            self.increases[stat] -= 1
                        self.update_stat +=1
                self.update_stat_info()
                self.update_skill_info()

        if not self.focus_cat_object or self.update_stat > 0 or self.update_skill > 0 or (len(self.new_class) <= 0 and self.level_class):
            self.done_button.disable()
        else:
            self.done_button.enable()

    def clear_cat_infos(self):
        if self.focus_cat:
            self.focus_cat.kill()
        if self.focus_name:
            self.focus_name.kill()
        if self.focus_info1:
            self.focus_info1.kill()
        if self.focus_info2:
            self.focus_info2.kill()
        self.update_stat_info()
        self.clear_skill_buttons()
        self.clear_class_buttons()

    def clear_cat_buttons(self):
        for cat in self.cat_buttons:
            self.cat_buttons[cat].kill()
        for x in range(len(self.cat_names)):
            self.cat_names[x].kill()

        self.cat_names = []
        self.cat_buttons = {}

    def clear_skill_buttons(self):
        for skill in self.skill_buttons.keys():
            self.skill_buttons[skill].kill()
        self.skill_buttons = {}
        for skill in self.skill_info.keys():
            self.skill_info[skill].kill()
        self.skill_info = {}
        for skill in self.skill_modifier.keys():
            self.skill_modifier[skill].kill()
        self.skill_modifier = {}

    def clear_class_buttons(self):
        for dnd_class in self.class_buttons.keys():
            self.class_buttons[dnd_class].kill()
        self.class_buttons = {}
        for dnd_class in self.class_info.keys():
            self.class_info[dnd_class].kill()
        self.class_info = {}

    def clear_stats_buttons(self):
        if self.stat_start_text:
            self.stat_start_text.kill()
        if self.stat_info_obj:
            for id in self.stat_info_obj.keys():
                self.stat_info_obj[id].kill()
        if self.stat_dec_buttons:
            for id in self.stat_dec_buttons:
                self.stat_dec_buttons[id].kill()
        if self.stat_inc_buttons:
            for id in self.stat_inc_buttons:
                self.stat_inc_buttons[id].kill()
        if self.stat_info_modifier:
            for id in self.stat_info_modifier:
                self.stat_info_modifier[id].kill()

    def chunks(self, L, n):
        return [L[x : x + n] for x in range(0, len(L), n)]