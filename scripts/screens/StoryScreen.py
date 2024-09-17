import pygame
import pygame_gui
from random import choice, randint
from typing import Dict, Any

from scripts.cat.cats import Cat
from scripts.events import Events
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game, MANAGER, screen, screen_x, screen_y
from scripts.game_structure.ui_elements import UISpriteButton, UIImageButton
from scripts.utility import (
    scale,
    process_text,
    shorten_text_to_fit,
    get_text_box_theme
)
from scripts.dnd.dnd_story import DnDStory
from scripts.dnd.dnd_types import DnDEventRole, create_cat_dict
from scripts.dnd.dnd_leveling import DnDLevelsReminder
from scripts.screens.DnDLevelScreen import get_leveled_cat
from .Screens import Screens


class StoryScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.fav = {}
        self.wandering_fav = {}
        self.story_buttons={}
        self.story_titles={}
        self.answer_buttons={}
        self.answer_titles={}
        self.skill_buttons = {}
        self.skill_info = {}
        self.cat_buttons = {}  # Hold cat image sprites.
        self.elements = {}  # hold elements for sub-page
        self.skill_to_roll = None
        self.make_roll = False
        self.selected_cat = None
        self.current_page = 1
        self.back_button = None
        self.wandering_cats = []
        self.wandering_cat_buttons = {}  # Hold cat image sprites.
        self.included_cats = []
        if game.clan:
            game.clan.current_story_id = None

    def on_use(self):
        if game.clan.clan_settings['backgrounds']:
            if game.clan.current_season == 'Newleaf':
                screen.blit(self.newleaf_bg, (0, 0))
            elif game.clan.current_season == 'Greenleaf':
                screen.blit(self.greenleaf_bg, (0, 0))
            elif game.clan.current_season == 'Leaf-bare':
                screen.blit(self.leafbare_bg, (0, 0))
            elif game.clan.current_season == 'Leaf-fall':
                screen.blit(self.leaffall_bg, (0, 0))

    def handle_event(self, event):
        if game.switches['window_open']:
            pass
        elif event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.story_buttons.values():
                for story_id, button in self.story_buttons.items():
                    if event.ui_element == self.story_buttons[story_id]:
                        game.clan.current_story_id = str(story_id)
                self.create_story_buttons()
                self.update_cat_images_buttons()
                self.update_buttons()
            elif event.ui_element == self.elements["continue"]:
                print(str(game.clan.current_story_id))
                active_story = game.clan.stories[str(game.clan.current_story_id)]
                print("current_story: ", game.clan.current_story_id)
                for cat in self.wandering_cat_buttons:
                    self.wandering_cat_buttons[cat].disable()
                self.handle_story(active_story)
            elif event.ui_element == self.elements["add_cat"] or event.ui_element == self.elements["remove_cat"]:
                if self.selected_cat in self.wandering_cats:
                    self.wandering_cats.remove(self.selected_cat)
                else:
                    self.wandering_cats.append(self.selected_cat)
                self.update_buttons()
            elif event.ui_element in self.answer_buttons.values():
                answer_id = [answer_id for answer_id in self.answer_buttons.keys() if event.ui_element == self.answer_buttons[answer_id]][0]
                self.handle_conversation(answer_id)
            elif event.ui_element == self.elements["dice"]:
                print("current_event: ", self.current_event.event_id)
                self.cat_to_roll = self.selected_cat # self.selected_cat
                self.update_selected_cat()
                self.clear_cat_buttons()
                self.elements["next_page"].hide()
                self.elements["last_page"].hide()
                self.clear_selected_cat_buttons()
                self.handle_outcome()
                self.done_button.show()
                self.skill_to_roll = None
                self.selected_cat = None
                self.elements["dice"].hide()  
                for skill in self.skill_buttons.values():
                    skill.kill()
                self.clear_wandering_cat_buttons()
            elif self.make_roll and event.ui_element in self.skill_buttons.values():
                for skill in self.current_conversation.answers[0]:
                    skill = skill.split(":")[0]
                    if event.ui_element == self.skill_buttons[skill]:
                        self.skill_to_roll = skill
                        self.skill_buttons[skill].select()
                self.update_buttons()
                self.update_skills_information()
            elif event.ui_element in self.cat_buttons.values():
                self.selected_cat = event.ui_element.return_cat_object()
                self.update_buttons()
                self.update_selected_cat()
            elif event.ui_element in self.wandering_cat_buttons.values():
                self.selected_cat = event.ui_element.return_cat_object()
                self.update_buttons()
                self.update_selected_cat()
            elif event.ui_element == self.back_button:
                self.change_screen(game.last_screen_forupdate)
            elif event.ui_element == self.done_button:
                self.skill_to_roll = None
                self.selected_cat = None
                self.change_screen(game.last_screen_forupdate)
            else:
                self.menu_button_pressed(event)

    def screen_switches(self):
        self.update_camp_bg()
        game.switches['cat'] = None
        if game.clan.biome + game.clan.camp_bg in game.clan.layouts:
            self.layout = game.clan.layouts[game.clan.biome + game.clan.camp_bg]
        else:
            self.layout = game.clan.layouts["default"]

        self.events_bg = pygame_gui.elements.UIImage(
            scale(pygame.Rect((322, 300), (1068, 740))),
            image_cache.load_image(
                "resources/images/event_page_bg.png"
            ).convert_alpha(),
            object_id="#events_bg",
            starting_height=-1,
            manager=MANAGER,
        )
        self.events_bg.disable()
        self.events_frame = pygame_gui.elements.UIImage(
            scale(pygame.Rect((322, 300), (1068, 740))),
            image_cache.load_image(
                "resources/images/event_page_frame.png"
            ).convert_alpha(),
            object_id="#events_frame",
            starting_height=-1,
            manager=MANAGER,
        )
        self.events_frame.disable()
        self.side_panel = pygame_gui.elements.UIImage(
            scale(pygame.Rect((60, 310), (360, 720))),
            image_cache.load_image(
                "resources/images/dnd/story_side_panel.png"
            ).convert_alpha(),
            object_id="#events_bg",
            starting_height=-2,
            manager=MANAGER,
        )
        self.side_panel.disable()

        self.story_text = pygame_gui.elements.UITextBox("",
                                       scale(pygame.Rect((750, 345), (570, 300))),
                                       object_id="#text_box_30_horizleft_pad_10_10_spacing_95",
                                       manager=MANAGER)
        self.story_text.hide()

        self.elements["dice"] = UIImageButton(
            scale(pygame.Rect((1200, 1050), (156, 156))), "",
            object_id="#dnd_dice",
            manager=MANAGER
        )
        self.elements["dice"].hide()
        
        # Able cat page buttons
        diff_x = 350
        page_x_pos = 1600/2-diff_x/2+34
        page_y_pos = 968
        self.elements['last_page'] = UIImageButton(scale(pygame.Rect((page_x_pos, page_y_pos), (68, 68))), "",
                                                   object_id="#patrol_last_page",
                                                   starting_height=2,
                                                   manager=MANAGER)
        self.elements['last_page'].hide()
        self.elements['next_page'] = UIImageButton(scale(pygame.Rect((page_x_pos+diff_x, page_y_pos), (68, 68))), "",
                                                   object_id="#patrol_next_page",
                                                   starting_height=2,
                                                   manager=MANAGER)
        self.elements['next_page'].hide()

        self.elements["add_cat"] = UIImageButton(scale(pygame.Rect((1100, 680), (196, 60))), "",
                                                        object_id="#add_cat_button", manager=MANAGER)
        self.elements["add_cat"].disable()
        self.elements["remove_cat"] = UIImageButton(
                scale(pygame.Rect((1071, 680), (254, 60))),
                "", starting_height=3,
                object_id="#remove_cat_button",
                manager=MANAGER)
        self.elements["remove_cat"].hide()

        self.elements["continue"] = UIImageButton(
            scale(pygame.Rect((1600/2-204/2, 1050), (204, 60))),
            "",
            object_id="#continue_button_small",
            manager=MANAGER
        )
        self.elements["continue"].disable()

        self.done_button = UIImageButton(
            scale(pygame.Rect((1200, 950), (154, 60))), "",
            object_id="#done_button",
            starting_height=2,
            manager=MANAGER
        )
        self.done_button.hide()

        self.set_disabled_menu_buttons(["world_screen"])
        self.update_heading_text(f'{game.clan.name}Clan')
        self.show_menu_buttons()
        self.back_button = UIImageButton(
            scale(pygame.Rect((50, 50), (210, 60))),
            "",
            object_id="#back_button",
            manager=MANAGER,
        )

        self.create_story_buttons()
        self.clear_cat_buttons()
        self.update_cat_images_buttons()
        leveled_cats = get_leveled_cat()
        if (leveled_cats and not game.clan.level_reminder) or game.clan.moonstart_levelable_cats < len(leveled_cats):
            game.clan.level_reminder = True
            game.clan.moonstart_levelable_cats = len(leveled_cats)
            DnDLevelsReminder()

    def exit_screen(self):
        # Kill all other elements, and destroy the reference so they aren't hanging around
        self.events_bg.kill()
        self.events_frame.kill()
        self.story_text.kill()
        self.clear_selected_cat_buttons()
        self.clear_story_buttons()
        self.clear_cat_buttons()
        self.clear_wandering_cat_buttons()
        self.clear_answer_buttons()
        for ele in self.elements:
            self.elements[ele].kill()
        self.elements = {}
        for skill in self.skill_buttons.values():
            skill.kill()
        self.skill_buttons = {}
        self.back_button.kill()
        self.done_button.kill()
        self.side_panel.kill()
        self.wandering_cats = []
        self.skill_info = {}
        self.make_roll = False
        game.clan.current_story_id = None

    def update_buttons(self):
        if self.wandering_cats and game.clan.current_story_id:
            self.elements["continue"].enable()
        else:
            self.elements["continue"].disable()

        if self.skill_to_roll and self.selected_cat:
            self.elements["dice"].enable()
        else:
            self.elements["dice"].disable()

        if self.selected_cat in self.wandering_cats and not self.make_roll:
            self.elements["remove_cat"].show()
            self.elements["remove_cat"].enable()
            self.elements["add_cat"].hide()
        elif self.selected_cat is None or len(self.wandering_cats) >= 6 and not self.make_roll:
            self.elements["add_cat"].show()
            self.elements["add_cat"].disable()
            self.elements["remove_cat"].hide()
        elif not self.make_roll:
            self.elements["remove_cat"].hide()
            self.elements["add_cat"].show()
            self.elements["add_cat"].enable()

        if self.make_roll:
            self.update_cat_images_buttons(self.wandering_cats, pos_y = 750, pos_x = 350, end_list_pos = 1300)
        else:
            self.update_cat_images_buttons(self.wandering_cats, pos_y=340, pos_x = 100, end_list_pos=250)

    def update_selected_cat(self):
        """Refreshes the image displaying the selected cat, traits, mentor/apprentice/mate ext"""
        self.clear_selected_cat_buttons()
        if self.make_roll:
            self.roll_cat_selection()
            self.update_cat_images_buttons(self.wandering_cats, pos_y = 750, pos_x = 350, end_list_pos = 1300)
        else:
            self.patrol_cat_selection()

    def handle_story(self, active_story: DnDStory):
        self.clear_cat_buttons()
        self.clear_story_buttons()
        self.clear_selected_cat_buttons()
        self.elements["add_cat"].hide()
        self.elements["remove_cat"].hide()
        self.elements["continue"].hide()
        current_story = game.clan.stories[str(game.clan.current_story_id)]
        cat_dict = create_cat_dict(Cat, self.wandering_cats, current_story.new_cats)

        text = "This will be replaced with the text of the current event"
        self.current_event, self.current_conversation = active_story.continue_story(cat_dict)
        self.current_event.random_cat = self.wandering_cats[randint(0,len(self.wandering_cats)-1)]
        cat_dict = create_cat_dict(Cat, self.wandering_cats, current_story.new_cats, self.current_event.random_cat)
        self.current_event.wandering_cats = self.wandering_cats

        # process the text
        text = self.current_conversation.get_text(len(self.wandering_cats))
        text = process_text(text, cat_dict)
        if "c_n" in text:
            text = text.replace("c_n", game.clan.name + "clan")
        self.story_text.show()
        self.story_text.set_text(
            text
        )
        self.create_answer_buttons(cat_dict)

    def handle_conversation(self, answer_id):
        if answer_id not in self.current_event.conversations:
            print(f"ERROR DnD: answer {answer_id} was given, which is not defined in the event {self.current_event.event_id}!")
            return

        self.clear_answer_buttons()
        current_story = game.clan.stories[str(game.clan.current_story_id)]
        self.current_event.continue_conversation(answer_id)
        current_story.current_conversation_id = answer_id
        self.current_conversation = self.current_event.current_conversation
        text = self.current_conversation.get_text(1)
        cat_dict = create_cat_dict(Cat, self.wandering_cats, current_story.new_cats)
        text = process_text(text, cat_dict)
        if "c_n" in text:
            text = text.replace("c_n", game.clan.name + "clan")
        self.story_text.show()
        self.story_text.set_text(
            text
        )
        self.create_answer_buttons(cat_dict)

    def handle_outcome(self):
        current_story = game.clan.stories[str(game.clan.current_story_id)]
        cat_ids = [cat.ID for cat in self.wandering_cats if DnDEventRole.PARTICIPANT.value in current_story.roles and cat.ID not in current_story.roles[DnDEventRole.PARTICIPANT.value]]
        if DnDEventRole.PARTICIPANT.value in current_story.roles:
            current_story.roles[DnDEventRole.PARTICIPANT.value].extend(cat_ids)
        else:
            current_story.roles[DnDEventRole.PARTICIPANT.value] = cat_ids
        cat_dict = create_cat_dict(Cat, self.wandering_cats, current_story.new_cats)
        pass_number = None
        if self.skill_to_roll in self.skill_info:
            pass_number = self.skill_info[self.skill_to_roll]["pass_number"]
        outcome_text = current_story.handle_outcome(self.skill_to_roll, self.cat_to_roll, pass_number)
        text = process_text(outcome_text, cat_dict)
        if "c_n" in text:
            text = text.replace("c_n", game.clan.name + "clan")
        self.story_text.show()
        self.story_text.set_text(
            text
        )
        if current_story.current_event_id:
            self.create_answer_buttons(cat_dict)
        else:
            print("HERE THE STORY ENDS")
            del game.clan.stories[str(game.clan.current_story_id)]
            self.done_button.show()

    def update_skills_information(self):
        self.hide_menu_buttons()
        self.back_button.hide()
        for skill in self.skill_buttons.keys():
            self.skill_buttons[skill].kill()
        self.skill_buttons = {}
        self.skill_info = {}

        button_pos_x = 500
        button_pos_y = 1032
        step_increase = 72

        for skill in self.current_conversation.answers[0]:
            if ":" in skill:
                pass_number = skill.split(":")[1]
                skill = skill.split(":")[0]
                if skill not in self.skill_info:
                    self.skill_info[skill] = {}
                    self.skill_info[skill]["pass_number"] = int(pass_number)
                else:
                    self.skill_info[skill]["pass_number"] = int(pass_number)
            is_selected = ""
            if skill == self.skill_to_roll:
                is_selected = "_selected"
            prepared_skill_name = skill.replace(" ", "_")
            self.skill_buttons[skill] = UIImageButton(
                scale(pygame.Rect((button_pos_x, button_pos_y), (280, 72))), "",
                    object_id=f"#dnd_skill_{prepared_skill_name}{is_selected}",
                    manager=MANAGER
                )
            button_pos_y += step_increase

    def update_cat_images_buttons(self, able_cats = None, pos_y: int = 750, pos_x: int = 350, end_list_pos: int = 1300):
        """Updates all the cat sprite buttons. Also updates the skills tab, if open, and the next and
            previous page buttons.  """
        cat_list = able_cats if able_cats else []
        if not isinstance(able_cats, list):
            self.clear_cat_buttons()
            # ASSIGN TO ABLE CATS
            for the_cat in Cat.all_cats_list:
                if not the_cat.dead and the_cat.in_camp and the_cat.status != 'kitten' and\
                    not the_cat.outside and not the_cat.not_working():
                    if the_cat.status == 'newborn' or game.config['fun']['all_cats_are_newborn']:
                        if game.config['fun']['newborns_can_patrol']:
                            cat_list.append(the_cat)
                    else:
                        cat_list.append(the_cat)
        else:
            self.clear_wandering_cat_buttons()

        all_pages = self.chunks(cat_list, 16)
        self.current_page = max(1, min(self.current_page, len(all_pages)))

        # Check for empty list (no able cats)
        if all_pages:
            display_cats = all_pages[self.current_page - 1]
        else:
            display_cats = []

        # Update next and previous page buttons
        if len(all_pages) <= 1:
            self.elements["next_page"].disable()
            self.elements["last_page"].disable()
        else:
            if self.current_page >= len(all_pages):
                self.elements["next_page"].disable()
            else:
                self.elements["next_page"].enable()

            if self.current_page <= 1:
                self.elements["last_page"].disable()
            else:
                self.elements["last_page"].enable()

        # Draw able cats.
        start_pos = pos_x
        cat_size = 100
        i = 0
        for cat in display_cats:
            if cat.ID in self.included_cats:
                fav_image = pygame_gui.elements.UIImage(
                    scale(pygame.Rect((pos_x, pos_y), (cat_size, cat_size))),
                    pygame.transform.scale(
                        pygame.image.load(
                            f"resources/images/fav_marker.png").convert_alpha(),
                        (cat_size, cat_size))
                )
                if not isinstance(able_cats, list):
                    self.fav[str(i)] = fav_image
                    self.fav[str(i)].disable()
                else:
                    self.wandering_fav[str(i)] = fav_image
                    self.wandering_fav[str(i)].disable()
            tool_tip_text = f"<b>{str(cat.name)}</b><br><b>Skills:</b><br>"
            tool_tip_text += cat.dnd_skills.get_display_text(False)
            button = UISpriteButton(
                scale(pygame.Rect((pos_x, pos_y), (cat_size, cat_size))),
                pygame.transform.scale(cat.sprite, (cat_size, cat_size)),
                cat_object=cat, manager=MANAGER,
                tool_tip_text=tool_tip_text,
                starting_height=3)
            if not isinstance(able_cats, list):
                self.cat_buttons["able_cat" + str(i)] = button
            else:
                self.wandering_cat_buttons["able_cat" + str(i)] = button
            pos_x += cat_size
            if pos_x >= end_list_pos:
                pos_x = start_pos
                pos_y += cat_size
            i += 1

    def patrol_cat_selection(self):
        # Now, if the selected cat is not None, we rebuild everything with the correct cat info
        # Selected Cat Image
        pos_x = 1600/2+200
        pos_y = 360

        name = str(self.selected_cat.name)  # get name
        short_name = shorten_text_to_fit(name, 350, 30)

        self.elements['selected_name'] = pygame_gui.elements.UITextBox(
            short_name,
            scale(pygame.Rect((pos_x, pos_y - 40), (400, 60))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER
        )
        self.elements["selected_image"] = pygame_gui.elements.UIImage(
            scale(pygame.Rect((pos_x + 40 , pos_y), (300, 300))),
            pygame.transform.scale(self.selected_cat.sprite,(300, 300)),
            manager=MANAGER
        )

    def roll_cat_selection(self):
        # Now, if the selected cat is not None, we rebuild everything with the correct cat info
        # Selected Cat Image
        pos_x = 1600/2-300/2
        pos_y = 50

        name = str(self.selected_cat.name)  # get name
        short_name = shorten_text_to_fit(name, 350, 30)

        self.elements['selected_name'] = pygame_gui.elements.UITextBox(
            short_name,
            scale(pygame.Rect((pos_x, pos_y - 50), (400, 60))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER
        )
        self.elements["selected_image"] = pygame_gui.elements.UIImage(
            scale(pygame.Rect((pos_x + 40 , pos_y), (300, 300))),
            pygame.transform.scale(self.selected_cat.sprite,(300, 300)),
            manager=MANAGER
        )

        dnd_skill_string = "<b>Skills:</b> (relevant bold) <br>"
        dnd_skill_string += self.selected_cat.dnd_skills.get_display_text(False, self.current_conversation.answers[0])
        if "skill_info" in self.elements:
            self.elements['skill_info'].kill()
        self.elements['skill_info'] = pygame_gui.elements.UITextBox(
            dnd_skill_string,
            scale(pygame.Rect((80, 315), (480, 1000))),
            object_id="#text_box_22_horizleft",
            manager=MANAGER)

    def create_story_buttons(self):
        for id, story_button in self.story_buttons.items():
            story_button.kill()
        for id, story_button in self.story_titles.items():
            story_button.kill()
        self.story_buttons = {}
        self.story_titles = {}
        self.included_cats = []
        stepsize = 60
        story_button_pos_y = 350
        story_button_pos_x = 380
        for story_id in range(game.dnd_config["max_story_amount"]):
            text = f"story {story_id}"
            object_id = "#dnd_prof_free"
            if str(story_id) == str(game.clan.current_story_id):
                object_id = "#dnd_prof_selected"
            if str(story_id) in game.clan.stories and game.clan.stories[str(story_id)] and game.clan.stories[str(story_id)].start_countdown < 1:
                participants = game.clan.stories[str(story_id)].get_participant_names()
                if DnDEventRole.PARTICIPANT.value in game.clan.stories[str(story_id)].roles:
                    if game.clan.current_story_id:
                        if str(story_id) == str(game.clan.current_story_id):
                            self.included_cats = game.clan.stories[str(story_id)].roles[DnDEventRole.PARTICIPANT.value]
                    else:
                        self.included_cats.extend(
                            game.clan.stories[str(story_id)].roles[DnDEventRole.PARTICIPANT.value]
                        )
                
                hover_display = "Involved cats: "
                if participants:
                    hover_display += ", ".join(participants)
                self.story_titles[str(story_id)] = pygame_gui.elements.UITextBox(
                    text,
                    scale(pygame.Rect((story_button_pos_x + 46, story_button_pos_y - 20), (400, 80))),
                    object_id="#text_box_30_horizleft",
                    manager=MANAGER,
                )
                self.story_buttons[str(story_id)] = UIImageButton(
                    scale(pygame.Rect((story_button_pos_x, story_button_pos_y), (44, 44))), "", 
                    object_id=object_id,
                    tool_tip_text=hover_display,
                    manager=MANAGER,
                    )
                #self.story_buttons[str(story_id)].disable()
            story_button_pos_y += stepsize

    def create_answer_buttons(self, pronoun_dict):
        answer_button_pos_y = 600
        answer_button_pos_x = 400

        answers = self.current_conversation.answers

        # if there is no answer, the story stops
        if not answers:
            print("HERE THE STORY ENDS")
            game.clan.stories[str(game.clan.current_story_id)] = None
            self.done_button.show()

        # if there is only one answer, the roll has to be made!
        if len(answers) == 1:
            self.make_roll = True
            self.elements["dice"].show()
            self.elements["dice"].enable()
            self.elements['next_page'].show()
            self.elements['last_page'].show()
            self.update_skills_information()
            self.clear_cat_buttons()
            self.update_cat_images_buttons(self.wandering_cats, pos_y = 750, pos_x = 350, end_list_pos = 1300)
            return


        button_height = 44
        for answer in answers:
            answer_id = answer[0]
            answer_text = answer[1]
            answer_text = process_text(answer_text, pronoun_dict)
            stepsize = button_height + (button_height/2)
            button_y_fix = (stepsize - button_height)/2
            if len(answer_text) >= 58:
                stepsize += button_height
                button_y_fix += button_height/2
            if "c_n" in answer_text:
                answer_text = answer_text.replace("c_n", game.clan.name + "clan")
            object_id = "#dnd_prof_free"
            self.answer_titles[answer_id] = pygame_gui.elements.UITextBox(
                answer_text,
                scale(pygame.Rect((answer_button_pos_x + button_height + 2, answer_button_pos_y), (900, stepsize))),
                object_id="#text_box_30_horizleft",
                manager=MANAGER,
            )
            self.answer_buttons[answer_id] = UIImageButton(
                scale(pygame.Rect((answer_button_pos_x , answer_button_pos_y + button_y_fix), (44, button_height))), "", 
                object_id=object_id,
                manager=MANAGER,
                )
            answer_button_pos_y += stepsize

    def clear_answer_buttons(self):
        for id, element in self.answer_buttons.items():
            element.kill()
        self.answer_buttons = {}
        for id, element in self.answer_titles.items():
            element.kill()
        self.answer_titles = {}

    def clear_story_buttons(self):
        for id, story_button in self.story_buttons.items():
            story_button.kill()
        for id, story_button in self.story_titles.items():
            story_button.kill()

    def clear_cat_buttons(self):
        for cat in self.cat_buttons:
            self.cat_buttons[cat].kill()
        self.cat_buttons = {}
        for marker in self.fav:
            self.fav[marker].kill()
        self.fav = {}

    def clear_wandering_cat_buttons(self):
        for cat in self.wandering_cat_buttons:
            self.wandering_cat_buttons[cat].kill()
        self.wandering_cat_buttons = {}
        for marker in self.wandering_fav:
            self.wandering_fav[marker].kill()
        self.wandering_fav = {}

    def clear_selected_cat_buttons(self):
        if "selected_image" in self.elements:
            self.elements["selected_image"].kill()
        
        if "selected_name" in self.elements:
            self.elements["selected_name"].kill()

        if "skill_info" in self.elements:
            self.elements['skill_info'].kill()

    def update_camp_bg(self):
        light_dark = "light"
        if game.settings["dark mode"]:
            light_dark = "dark"

        camp_bg_base_dir = 'resources/images/camp_bg/'
        leaves = ["newleaf", "greenleaf", "leafbare", "leaffall"]
        camp_nr = game.clan.camp_bg

        if camp_nr is None:
            camp_nr = 'camp1'
            game.clan.camp_bg = camp_nr

        available_biome = ['Forest', 'Mountainous', 'Plains', 'Beach']
        biome = game.clan.biome
        if biome not in available_biome:
            biome = available_biome[0]
            game.clan.biome = biome
        biome = biome.lower()

        all_backgrounds = []
        for leaf in leaves:
            platform_dir = f'{camp_bg_base_dir}/{biome}/{leaf}_{camp_nr}_{light_dark}.png'
            all_backgrounds.append(platform_dir)

        self.newleaf_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[0]).convert(), (screen_x, screen_y))
        self.greenleaf_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[1]).convert(), (screen_x, screen_y))
        self.leafbare_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[2]).convert(), (screen_x, screen_y))
        self.leaffall_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[3]).convert(), (screen_x, screen_y))

    def chunks(self, L, n):
        return [L[x: x + n] for x in range(0, len(L), n)]
