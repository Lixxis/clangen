import pygame
import pygame_gui

from re import sub
from scripts.dnd.dnd_types import StatType
from scripts.utility import scale
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.image_button import UIImageButton, UITextBoxTweaked
from pygame_gui.elements import UIWindow


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

def update_levels(leveled_cats):
    "Updates the levels of the given cats in the overall game xp documentation."
    for cat in leveled_cats:
        game.clan.xp[cat.ID] = cat.experience_level

class DnDCatLevels(UIWindow):
    """This window allows the user to specify the cat's gender"""

    def __init__(self, cat):
        game.switches['window_open'] = True
        self.elements = {}
        self.the_cat = cat
        self.update_skill = 0
        self.update_stat = 0
        self.stat_list = [stat for stat in StatType]
        self.selected_stat_idx = 0
        self.selected_stat = self.stat_list[self.selected_stat_idx]
        self.current_skills = self.the_cat.dnd_skills.skill_based[self.selected_stat]
        self.collect_leveling_need()
        pos_y = 150
        self.length = 1120
        pos_x = 310
        self.width = 980

        # automatic position done button at the bottom center
        done_button_width = 154
        done_button_length = 60
        done_button_x = self.width / 2 - done_button_width / 2
        done_button_y = self.length - done_button_length - done_button_length / 2

        super().__init__(scale(pygame.Rect((pos_x, pos_y), (self.width, self.length))),
                         window_display_title='Cat Level-up',
                         object_id='#cat_level_up',
                         resizable=False)

        stat_pos_y = 290
        stat_pos_x = (self.width/2) + 30
        stat_width = 380
        stat_length = 580
        arrow_width = 44
        arrow_length = 68
        for stat in StatType:
            if stat.value == "constitution":
                continue
            self.elements[stat] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((stat_pos_x, stat_pos_y), (stat_width, stat_length))),
                pygame.transform.scale(
                    pygame.image.load(
                        f"resources/images/dnd/skill_based_{stat.value}.png").convert_alpha(),
                        (stat_width, stat_length)
                    ),
                manager=MANAGER,
                container=self
            )
            if stat.value != self.selected_stat.value:
                self.elements[stat].hide()

        self.next_button = UIImageButton(
            scale(pygame.Rect((stat_pos_x + stat_width, stat_pos_y + stat_length/2 - arrow_length/2), (arrow_width, arrow_length))), "",
            object_id="#dnd_lvl_next",
            manager=MANAGER,
            container=self
        )

        self.prev_button = UIImageButton(
            scale(pygame.Rect((stat_pos_x - arrow_width, stat_pos_y + stat_length/2 - arrow_length/2), (arrow_width, arrow_length))), "",
            object_id="#dnd_lvl_prev",
            manager=MANAGER,
            container=self
        )

        self.heading = pygame_gui.elements.UITextBox(
            f"<b>- {self.the_cat.name} leveled up ({self.the_cat.experience_level}) -</b>",
            scale(pygame.Rect((20, 20), (self.width, 80))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            container=self)

        self.done_button = UIImageButton(
            scale(pygame.Rect((done_button_x, done_button_y), (done_button_width, done_button_length))), "",
            object_id="#done_button",
            manager=MANAGER,
            container=self
        )

        self.elements["cat_bg"] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((50, 100), (384, 478))),
                pygame.transform.scale(
                    pygame.image.load(
                        f"resources/images/dnd/leveling_profile.png").convert_alpha(),
                        (384, 478)
                    ),
                manager=MANAGER,
                container=self
            )
        self.cat_image = pygame_gui.elements.UIImage(
            scale(pygame.Rect((100, 110), (300, 300))),
            pygame.transform.scale(self.the_cat.sprite,(300, 300)),
            manager=MANAGER,
            container=self
        )
        cat_information = self.the_cat.genderalign + "<br>"
        cat_information += str(self.the_cat.moons) + " moons <br>"
        cat_information += self.the_cat.age + "<br>"
        self.cat_text1 = pygame_gui.elements.UITextBox(
            f"{cat_information}",
            scale(pygame.Rect((52, 420), (200, 200))),
            object_id="#text_box_30_horizcenter_spacing_95_light",
            manager=MANAGER,
            container=self
        )
        cat_information = self.the_cat.dnd_linage.linage_type.value + "<br>"
        self.cat_text2 = pygame_gui.elements.UITextBox(
            f"{cat_information}",
            scale(pygame.Rect((52 + 200, 420), (200, 200))),
            object_id="#text_box_30_horizcenter_spacing_95_light",
            manager=MANAGER,
            container=self
        )

        self.stat_info_obj = {}
        self.stat_info_modifier = {}
        self.increases = {}
        self.stat_inc_buttons = {}
        self.stat_dec_buttons = {}
        self.stat_start_text = None
        self.update_stat_info()

        self.skill_start_text = None
        self.skill_buttons = {}
        self.skill_info = {}
        self.skill_modifier = {}
        self.new_proficiency = []
        self.update_skill_info()

        if self.update_stat > 0 or self.update_skill > 0:
            self.done_button.disable()

        self.set_blocking(True)

    def collect_leveling_need(self):
        start_level_number = int(self.the_cat.experience_level.split(" ")[1])
        end_level_number = int(self.the_cat.experience_level.split(" ")[1])
        if end_level_number < int(game.clan.xp[self.the_cat.ID].split(" ")[1]):
            end_level_number = int(game.clan.xp[self.the_cat.ID].split(" ")[1])
        elif end_level_number == int(game.clan.xp[self.the_cat.ID].split(" ")[1]):
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

    def update_stat_info(self):
        stats = self.the_cat.dnd_stats.stats
        text_pos_x = 30
        button_pos_x_decr = 390
        button_pos_x_incr = 440

        text_pos_y = 630
        button_pos_y = text_pos_y + 17
        step_increase = 60
        if self.stat_start_text:
            self.stat_start_text.kill()
        self.stat_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_stat),
            scale(pygame.Rect((text_pos_x, text_pos_y-30), (250, 80))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER,
            container=self
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
                container=self
            )

            # INCREASE
            if stat in self.stat_inc_buttons:
                self.stat_inc_buttons[stat].kill()
            self.stat_inc_buttons[stat] = UIImageButton(
                scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                object_id="#dnd_stats_add",
                manager=MANAGER,
                container=self
            )

            # DECREASE
            if stat in self.stat_dec_buttons:
                self.stat_dec_buttons[stat].kill()
            self.stat_dec_buttons[stat] = UIImageButton(scale(
                pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
                object_id="#dnd_stats_sub",
                manager=MANAGER,
                container=self
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
            current_stat_value = self.the_cat.dnd_stats.stats[stat]
            if stat in self.increases:
                current_stat_value += self.increases[stat]
            modifier = self.the_cat.dnd_stats.modifier[current_stat_value]
            text = "(" + str(modifier) + ")"
            if modifier >= 0:
                text = "(+" + str(modifier) + ")"
            self.stat_info_modifier[stat] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x + 278, text_pos_y), (100, 80))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
                container=self
            )
            text_pos_y += step_increase
            button_pos_y += step_increase

        if self.update_stat > 0 or self.update_skill > 0:
            self.done_button.disable()
        else:
            self.done_button.enable()

    def update_skill_info(self):
        for skill in self.skill_buttons.keys():
            self.skill_buttons[skill].kill()
        self.skill_buttons = {}
        for skill in self.skill_info.keys():
            self.skill_info[skill].kill()
        self.skill_info = {}
        for skill in self.skill_modifier.keys():
            self.skill_modifier[skill].kill()
        self.skill_modifier = {}

        for key in self.elements.keys():
            if key == self.selected_stat or key == "cat_bg":
                self.elements[key].show()
            else:
                self.elements[key].hide()

        text_pos_x = (self.width/2) + 106
        button_pos_x = text_pos_x - 46

        text_pos_y = 400
        button_pos_y = text_pos_y + 17
        step_increase = 50

        if self.skill_start_text:
            self.skill_start_text.kill()
        self.skill_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_skill),
            scale(pygame.Rect((text_pos_x, text_pos_y-30), (200, 70))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER,
            container=self)

        skills = self.the_cat.dnd_skills.skills
        proficiency = self.the_cat.dnd_skills.proficiency
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
            stat_based_on = [stat for stat in StatType if skill in self.the_cat.dnd_skills.skill_based[stat]][0]
            if stat_based_on in self.increases:
                new_stat_number = self.the_cat.dnd_stats.stats[stat_based_on] + self.increases[stat_based_on]
                modifier = self.the_cat.dnd_stats.modifier[new_stat_number]
                modifier += game.dnd_config["proficiency_bonus"] if skill in self.the_cat.dnd_skills.proficiency else 0
            if skill in self.new_proficiency:
                modifier += game.dnd_config["proficiency_bonus"]
            addition = 46
            if modifier < 0:
                addition += 5
            self.skill_info[skill.value] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x + 46, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                container=self,
                manager=MANAGER)
            self.skill_buttons[skill.value] = UIImageButton(scale(pygame.Rect((button_pos_x, button_pos_y), (44, 44))), "", 
                                            object_id=object_id, 
                                            manager=MANAGER,
                                            container=self)
            if modifier >= 0:
                modifier = "+" + str(modifier)
            else:
                modifier = str(skills[skill])
            self.skill_modifier[skill.value] = pygame_gui.elements.UITextBox(
                modifier,
                scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                container=self,
                manager=MANAGER
            )
            if skill in proficiency or (self.update_skill <= 0 and skill not in self.new_proficiency):
                self.skill_buttons[skill.value].disable()
            text_pos_y += step_increase
            button_pos_y += step_increase

        if self.update_stat > 0 or self.update_skill > 0:
            self.done_button.disable()
        else:
            self.done_button.enable()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                stats = self.the_cat.dnd_stats.genetic_stats
                for stat in StatType:
                    self.the_cat.dnd_stats.genetic_stats[stat] = stats[stat]
                    if stat in self.increases:
                        self.the_cat.dnd_stats.genetic_stats[stat] += self.increases[stat]
                self.the_cat.dnd_stats.update_stats()
                self.the_cat.dnd_skills.proficiency.extend(self.new_proficiency)
                self.the_cat.dnd_skills.update_skills(self.the_cat.dnd_stats)
                game.switches['window_open'] = False
                self.kill()
            elif event.ui_element in self.skill_buttons.values():
                for skill in self.the_cat.dnd_skills.skills:
                    if skill not in self.current_skills:
                        continue
                    if event.ui_element == self.skill_buttons[skill.value]:
                        if skill in self.new_proficiency:
                            self.new_proficiency.remove(skill)
                            self.update_skill += 1
                        else:
                            self.new_proficiency.append(skill)
                            self.update_skill -= 1
                self.current_skills = self.the_cat.dnd_skills.skill_based[self.selected_stat]
                self.update_skill_info()
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
                self.current_skills = self.the_cat.dnd_skills.skill_based[self.selected_stat]
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
                self.current_skills = self.the_cat.dnd_skills.skill_based[self.selected_stat]
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
