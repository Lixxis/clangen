import pygame
import pygame_gui

from re import sub
from scripts.dnd.dnd_types import StatType, ClassType
from scripts.utility import scale
from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.ui_elements import UIImageButton
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

class DnDLevelsReminder(UIWindow):
    """This window will remind the player, that there are cats which can be leveled."""

    def __init__(self):
        game.switches['window_open'] = True
        length = 250
        pos_y = 750 - length/2
        width = 700
        pos_x = 800 - width/2

        # automatic position done button at the bottom center
        done_button_width = 154
        done_button_length = 60
        done_button_x = width / 2 - done_button_width / 2
        done_button_y = length - done_button_length - done_button_length / 2

        super().__init__(scale(pygame.Rect((pos_x, pos_y), (width, length))),
                         window_display_title='Cat Level-up',
                         object_id='#cat_level_up',
                         resizable=False)

        self.heading = pygame_gui.elements.UITextBox(
            f"<b>- One or multiple cat's can be leveled! -</b><br>" +
            "Click on the 'level up' button on the right side.",
            scale(pygame.Rect((0, 20), (width, 160))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            container=self)

        self.done_button = UIImageButton(
            scale(pygame.Rect((done_button_x, done_button_y), (done_button_width, done_button_length))), "",
            object_id="#done_button",
            manager=MANAGER,
            container=self
        )

        self.set_blocking(True)

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                game.switches['window_open'] = False
                self.kill()