import pygame
import pygame_gui

from re import sub
from scripts.utility import scale
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.image_button import UIImageButton, UITextBoxTweaked
from pygame_gui.elements import UIWindow


def get_leveled_cat():
    "Returns if a cat had a level up or not."
    leveled_cat = []
    for cat_id, cat in Cat.all_cats.items():
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
        self.the_cat = cat
        self.update_skill = 0
        self.update_stat = 0
        self.collect_leveling_need()
        pos_y = 400
        length = 600
        done_button_x = 323
        done_button_y = 520
        image_pos_x = 250

        if self.update_stat:
            image_pos_x = 50

        if self.update_skill > 0:
            image_pos_x = 50
            pos_y = 150
            length = 1100
            done_button_x = 120
            done_button_y = 1000
        super().__init__(scale(pygame.Rect((400, pos_y), (800, length))),
                         window_display_title='Change Cat Gender',
                         object_id='#change_cat_gender_window',
                         resizable=False)

        self.heading = pygame_gui.elements.UITextBox(
            f"<b>- {self.the_cat.name} leveled up ({self.the_cat.experience_level}) -</b>",
            scale(pygame.Rect((20, 20), (760, 80))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            container=self)

        self.done_button = UIImageButton(
            scale(pygame.Rect((done_button_x, done_button_y), (154, 60))), "",
            object_id="#done_button",
            manager=MANAGER,
            container=self)

        self.cat_image = pygame_gui.elements.UIImage(scale(pygame.Rect((image_pos_x, 80), (300, 300))),
                                                     pygame.transform.scale(self.the_cat.sprite,(300, 300)),
                                                     manager=MANAGER,
                                                     container=self)
        
        self.stat_info = None
        self.str_info = None
        self.str_increase = 0
        self.str_dec_button = None
        self.str_inc_button = None
        self.dex_info = None
        self.dex_increase = 0
        self.dex_dec_button = None
        self.dex_inc_button = None
        self.con_info = None
        self.con_increase = 0
        self.con_dec_button = None
        self.con_inc_button = None
        self.int_info = None
        self.int_increase = 0
        self.int_dec_button = None
        self.int_inc_button = None
        self.wis_info = None
        self.wis_increase = 0
        self.wis_dec_button = None
        self.wis_inc_button = None
        self.cha_info = None
        self.cha_increase = 0
        self.cha_dec_button = None
        self.cha_inc_button = None
        if self.update_stat > 0:
            self.update_stat_info()

        self.skill_start_text = None
        self.skill_buttons = {}
        self.skill_info = {}
        self.new_proficiency = []
        if self.update_skill > 0:
            self.update_skill_info()

        if self.update_stat > 0 or self.update_skill > 0:
            self.done_button.disable()
            print("SKILL ", self.update_skill)
            print("STAT ", self.update_stat)

        self.set_blocking(True)

    def collect_leveling_need(self):
        start_level_reached = False
        for level in game.dnd_config["leveling"].keys():
            # look for the level to start level counting
            if not start_level_reached:
                if level == game.clan.xp[self.the_cat.ID]:
                    start_level_reached = True
                else:
                    continue
            else:
                if game.dnd_config["leveling"][level]:
                    info = game.dnd_config["leveling"][level].split(":")
                    lvl_type = info[0]
                    amount = info[1]
                    if lvl_type == "stat":
                        self.update_stat += int(amount)
                    if lvl_type == "skill":
                        self.update_skill += int(amount)
                # if the new current level is reached, stop looking for the update
                if self.the_cat.experience_level == level:
                    break

    def kill_stats_buttons(self):
        if self.str_dec_button:
            self.str_dec_button.kill()
        if self.str_inc_button:
            self.str_inc_button.kill()
        if self.dex_dec_button:
            self.dex_dec_button.kill()
        if self.dex_inc_button:
            self.dex_inc_button.kill()
        if self.con_dec_button:
            self.con_dec_button.kill()
        if self.con_inc_button:
            self.con_inc_button.kill()
        if self.int_dec_button:
            self.int_dec_button.kill()
        if self.int_inc_button:
            self.int_inc_button.kill()
        if self.wis_dec_button:
            self.wis_dec_button.kill()
        if self.wis_inc_button:
            self.wis_inc_button.kill()
        if self.cha_dec_button:
            self.cha_dec_button.kill()
        if self.cha_inc_button:
            self.cha_inc_button.kill()

    def update_stat_info(self):
        self.kill_stats_buttons()
        stat = self.the_cat.dnd_stats
        text_pos_x = 360
        button_pos_x_decr = 650
        button_pos_x_incr = 700

        text_pos_y = 110
        button_pos_y = text_pos_y + 17
        step_increase = 60
        if self.stat_info:
            self.stat_info.kill()
        self.stat_info = pygame_gui.elements.UITextBox("points to give: " + str(self.update_stat),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y-30), (300, 80))),
                                                     object_id="#text_box_22_horizleft",
                                                     manager=MANAGER,
                                                     container=self)

        if self.str_info:
            self.str_info.kill()
        self.str_info = pygame_gui.elements.UITextBox("STRENGTH: " + str(stat.str + self.str_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.str_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "", 
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.str_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add",
                                            manager=MANAGER,
                                            container=self)
        if self.str_increase == 0:
            self.str_dec_button.disable()

        if self.dex_info:
            self.dex_info.kill()
        text_pos_y += step_increase
        button_pos_y += step_increase
        self.dex_info = pygame_gui.elements.UITextBox("DEXTERITY: " + str(stat.dex + self.dex_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.dex_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.dex_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add", 
                                            manager=MANAGER,
                                            container=self)
        if self.dex_increase == 0:
            self.dex_dec_button.disable()

        if self.con_info:
            self.con_info.kill()
        text_pos_y += step_increase
        button_pos_y += step_increase
        self.con_info = pygame_gui.elements.UITextBox("CONSTITUTION: " + str(stat.con + self.con_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.con_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "", 
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.con_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add", 
                                            manager=MANAGER,
                                            container=self)
        if self.con_increase == 0:
            self.con_dec_button.disable()

        if self.int_info:
            self.int_info.kill()
        text_pos_y += step_increase
        button_pos_y += step_increase
        self.int_info = pygame_gui.elements.UITextBox("INTELLIGENCE: " + str(stat.int + self.int_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.int_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.int_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add", 
                                            manager=MANAGER,
                                            container=self)
        if self.int_increase == 0:
            self.int_dec_button.disable()

        if self.wis_info:
            self.wis_info.kill()
        text_pos_y += step_increase
        button_pos_y += step_increase
        self.wis_info = pygame_gui.elements.UITextBox("WISDOM: " + str(stat.wis + self.wis_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.wis_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.wis_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add", 
                                            manager=MANAGER,
                                            container=self)
        if self.wis_increase == 0:
            self.wis_dec_button.disable()

        if self.cha_info:
            self.cha_info.kill()
        text_pos_y += step_increase
        button_pos_y += step_increase
        self.cha_info = pygame_gui.elements.UITextBox("CHARISMA: " + str(stat.cha + self.cha_increase),
                                                     scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)
        self.cha_dec_button = UIImageButton(scale(pygame.Rect((button_pos_x_decr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_sub", 
                                            manager=MANAGER,
                                            container=self)
        self.cha_inc_button = UIImageButton(scale(pygame.Rect((button_pos_x_incr, button_pos_y), (44, 44))), "",
                                            object_id="#dnd_stats_add", 
                                            manager=MANAGER,
                                            container=self)
        if self.cha_increase == 0:
            self.cha_dec_button.disable()


        if self.update_stat <= 0:
            self.str_inc_button.disable()
            self.dex_inc_button.disable()
            self.con_inc_button.disable()
            self.int_inc_button.disable()
            self.wis_inc_button.disable()
            self.cha_inc_button.disable()

        if self.update_stat > 0:
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

        text_pos_x = 450
        button_pos_x = 400

        text_pos_y = 110
        button_pos_y = text_pos_y + 17
        step_increase = 50

        if self.skill_start_text:
            self.skill_start_text.kill()
        self.skill_start_text = pygame_gui.elements.UITextBox(
            "points to give: " + str(self.update_skill),
            scale(pygame.Rect((text_pos_x, text_pos_y-30), (300, 80))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER,
            container=self)

        skills = self.the_cat.dnd_skills.skills
        proficiency = self.the_cat.dnd_skills.proficiency
        for skill in skills:
            text = skill.value
            object_id = "#dnd_prof_free"
            if skill in proficiency:
                object_id = "#dnd_prof"
                text = "<b><i>" + text + "</i></b>"
            elif skill in self.new_proficiency:
                object_id = "#dnd_prof_selected"

            self.skill_info[skill.value] = pygame_gui.elements.UITextBox(
                text,
                scale(pygame.Rect((text_pos_x, text_pos_y), (300, 80))),
                object_id="#text_box_30_horizleft",
                container=self,
                manager=MANAGER)
            self.skill_buttons[skill.value] = UIImageButton(scale(pygame.Rect((button_pos_x, button_pos_y), (44, 44))), "", 
                                            object_id=object_id, 
                                            manager=MANAGER,
                                            container=self)
            if skill in proficiency or (self.update_skill <= 0 and skill not in self.new_proficiency):
                self.skill_buttons[skill.value].disable()
            text_pos_y += step_increase
            button_pos_y += step_increase

        if self.update_skill > 0:
            self.done_button.disable()
        else:
            self.done_button.enable()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                stat = self.the_cat.dnd_stats
                self.the_cat.dnd_stats.str = stat.str + self.str_increase
                self.the_cat.dnd_stats.dex = stat.dex + self.dex_increase
                self.the_cat.dnd_stats.con = stat.con + self.con_increase
                self.the_cat.dnd_stats.int = stat.int + self.int_increase
                self.the_cat.dnd_stats.wis = stat.wis + self.wis_increase
                self.the_cat.dnd_stats.cha = stat.cha + self.cha_increase
                self.the_cat.dnd_skills.proficiency.extend(self.new_proficiency)
                self.the_cat.dnd_skills.update_skills(self.the_cat.dnd_stats)
                game.switches['window_open'] = False
                self.kill()
            elif event.ui_element in self.skill_buttons.values():
                for skill in self.the_cat.dnd_skills.skills:
                    if event.ui_element == self.skill_buttons[skill.value]:
                        if skill in self.new_proficiency:
                            self.new_proficiency.remove(skill)
                            self.update_skill += 1
                        else:
                            self.new_proficiency.append(skill)
                            self.update_skill -= 1
                self.update_skill_info()
            elif event.ui_element == self.str_inc_button:
                self.str_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.dex_inc_button:
                self.dex_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.con_inc_button:
                self.con_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.int_inc_button:
                self.int_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.wis_inc_button:
                self.wis_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.cha_inc_button:
                self.cha_increase += 1
                self.update_stat -= 1
                self.update_stat_info()
            elif event.ui_element == self.str_dec_button:
                self.str_increase -= 1
                self.update_stat += 1
                self.update_stat_info()
            elif event.ui_element == self.dex_dec_button:
                self.dex_increase -= 1
                self.update_stat += 1
                self.update_stat_info()
            elif event.ui_element == self.con_dec_button:
                self.con_increase -= 1
                self.update_stat += 1
                self.update_stat_info()
            elif event.ui_element == self.int_dec_button:
                self.int_increase -= 1
                self.update_stat += 1
                self.update_stat_info()
            elif event.ui_element == self.wis_dec_button:
                self.wis_increase -= 1
                self.update_stat += 1
                self.update_stat_info()
            elif event.ui_element == self.cha_dec_button:
                self.cha_increase -= 1
                self.update_stat += 1
                self.update_stat_info()