import pygame
import pygame_gui

from scripts.utility import scale
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.image_button import UIImageButton
from pygame_gui.elements import UIWindow

# TODO: seems pop-up window don't work in threads of patrol screen.
# therefore -> add a "inbetween" scene before the result is shown 


class DnDRolling(UIWindow):
    """This window allows the user to specify the cat's gender"""

    def __init__(self, cat_list, skills_to_roll):
        game.switches['window_open'] = True
        self.the_cat_list = cat_list
        self.the_cat = cat_list[0]
        self.skills_to_roll = skills_to_roll
        self.chosen_skill = None
        pos_y = 400
        length = 600
        done_button_x = 323
        done_button_y = 520

        super().__init__(scale(pygame.Rect((400, pos_y), (800, length))),
                         window_display_title='Change Cat Gender',
                         object_id='#change_cat_gender_window',
                         resizable=False)

        skill_names = [skill.value for skill in skills_to_roll]

        self.heading = pygame_gui.elements.UITextBox(
            f"<b>- Decide which cat should take the roll -</b>",
            scale(pygame.Rect((20, 20), (790, 80))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            container=self)
        self.more_info = pygame_gui.elements.UITextBox(
            ", ".join(skill_names),
            scale(pygame.Rect((20, 80), (760, 500))),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=MANAGER,
            container=self)
        self.done_button = UIImageButton(
            scale(pygame.Rect((done_button_x, done_button_y), (154, 60))), "",
            object_id="#done_button",
            manager=MANAGER,
            container=self)

        self.skill_buttons = {}
        self.skill_info = {}
        self.update_skill_info()
        self.set_blocking(True)

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

        for skill in self.skills_to_roll:
            text = skill.value
            object_id = "#dnd_prof_free"
            if skill == self.chosen_skill:
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
            if self.chosen_skill and skill != self.chosen_skill:
                self.skill_buttons[skill.value].disable()
            text_pos_y += step_increase
            button_pos_y += step_increase

        if self.chosen_skill:
            self.done_button.disable()
        else:
            self.done_button.enable()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                game.switches['window_open'] = False
                self.kill()
            elif event.ui_element in self.skill_buttons.values():
                for skill in self.the_cat.dnd_skills.skills:
                    if event.ui_element == self.skill_buttons[skill.value]:
                        if skill == self.chosen_skill:
                            self.chosen_skill = None
                        else:
                            self.chosen_skill = skill
                self.update_skill_info()
