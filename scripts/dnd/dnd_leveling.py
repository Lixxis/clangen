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
        super().__init__(scale(pygame.Rect((400, 400), (800, 600))),
                         window_display_title='Change Cat Gender',
                         object_id='#change_cat_gender_window',
                         resizable=False)
        game.switches['window_open'] = True
        self.the_cat = cat
        self.update_skill = 0
        self.update_stat = 0
        self.collect_leveling_need()

        self.back_button = UIImageButton(
            scale(pygame.Rect((740, 10), (44, 44))),
            "",
            object_id="#exit_window_button",
            container=self
        )
        self.heading = pygame_gui.elements.UITextBox(f"<b>- {self.the_cat.name} leveled up -</b>",
                                                     scale(pygame.Rect(
                                                         (20, 20), (760, 150))),
                                                     object_id="#text_box_30_horizcenter_spacing_95",
                                                     manager=MANAGER,
                                                     container=self)
        self.stat_info = None
        self.str_dec_button = None
        self.str_inc_button = None
        self.dex_dec_button = None
        self.dex_inc_button = None
        self.con_dec_button = None
        self.con_inc_button = None
        self.int_dec_button = None
        self.int_inc_button = None
        self.wis_dec_button = None
        self.wis_inc_button = None
        self.cha_dec_button = None
        self.cha_inc_button = None
        self.update_stat_buttons()

        image_pos_x = 250
        if self.update_skill or self.update_stat:
            image_pos_x = 50
        self.cat_image = pygame_gui.elements.UIImage(scale(pygame.Rect((image_pos_x, 45), (300, 300))),
                                                     pygame.transform.scale(self.the_cat.sprite,(300, 300)),
                                                     manager=MANAGER,
                                                     container=self)

        self.done_button = UIImageButton(scale(pygame.Rect((323, 520), (154, 60))), "",
                                         object_id="#done_button",
                                         manager=MANAGER,
                                         container=self)
        if self.update_skill or self.update_stat:
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
        

    def update_stat_buttons(self):
        self.kill_stats_buttons()
        stat = self.the_cat.dnd_stats
        dnd_stat_string = "strength: " + str(stat.str) + "<br>"
        dnd_stat_string += "dexterity: " + str(stat.dex) + "<br>"
        dnd_stat_string += "constitution: " + str(stat.con) + "<br>"
        dnd_stat_string += "intelligence: " + str(stat.int) + "<br>"
        dnd_stat_string += "wisdom: " + str(stat.wis) + " <br>"
        dnd_stat_string += "charisma: " + str(stat.cha) + " <br>"
        if self.stat_info:
            self.stat_info.kill()
        self.stat_info = pygame_gui.elements.UITextBox(dnd_stat_string,
                                                     scale(pygame.Rect((450, 110), (400, 350))),
                                                     object_id="#text_box_30_horizleft",
                                                     manager=MANAGER,
                                                     container=self)

        self.str_dec_button = UIImageButton(scale(pygame.Rect((380, 110), (68, 68))), "", 
                                            object_id="#arrow_left_button", 
                                            manager=MANAGER,
                                            container=self)
        self.str_inc_button = UIImageButton(scale(pygame.Rect((680, 110), (68, 68))), "",
                                            object_id="#arrow_right_button",
                                            manager=MANAGER,
                                            container=self)
        self.dex_dec_button = None
        self.dex_inc_button = None
        self.con_dec_button = None
        self.con_inc_button = None
        self.int_dec_button = None
        self.int_inc_button = None
        self.wis_dec_button = None
        self.wis_inc_button = None
        self.cha_dec_button = None
        self.cha_inc_button = None

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                game.switches['window_open'] = False
                self.kill()
            elif event.ui_element == self.back_button:
                game.switches['window_open'] = False
                self.kill()
