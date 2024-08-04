import random
import traceback
from copy import deepcopy

from scripts.dnd.dnd_leveling import DnDLevelsReminder, get_leveled_cat

import pygame
import pygame_gui

from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game, MANAGER, screen, screen_x, screen_y
from scripts.game_structure.ui_elements import UISpriteButton, UIImageButton
from scripts.game_structure.windows import SaveError
from scripts.utility import scale
from .Screens import Screens


class WorldScreen(Screens):
    story_buttons={}
    story_titles={}
    
    def __init__(self, name=None):
        super().__init__(name)

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
            if event.ui_element == self.save_button:
                try:
                    self.save_button_saving_state.show()
                    self.save_button.disable()
                    game.save_cats()
                    game.clan.save_clan()
                    game.clan.save_pregnancy(game.clan)
                    game.save_events()
                    game.save_settings()
                    game.switches['saved_clan'] = True
                    self.update_buttons_and_text()
                except RuntimeError:
                    SaveError(traceback.format_exc())
                    self.change_screen("start screen")
            else:
                self.menu_button_pressed(event)
        elif event.type == pygame.KEYDOWN and game.settings['keybinds']:
            if event.key == pygame.K_RIGHT:
                self.change_screen('list screen')
            elif event.key == pygame.K_LEFT:
                self.change_screen('events screen')
            elif event.key == pygame.K_SPACE:
                self.save_button_saving_state.show()
                self.save_button.disable()
                game.save_cats()
                game.clan.save_clan()
                game.clan.save_pregnancy(game.clan)
                game.save_events()
                game.save_settings()
                game.switches['saved_clan'] = True
                self.update_buttons_and_text()

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
            starting_height=2,
            manager=MANAGER,
        )
        self.events_bg.disable()
        self.events_frame = pygame_gui.elements.UIImage(
            scale(pygame.Rect((322, 300), (1068, 740))),
            image_cache.load_image(
                "resources/images/event_page_frame.png"
            ).convert_alpha(),
            object_id="#events_frame",
            starting_height=2,
            manager=MANAGER,
        )
        self.events_frame.disable()

        self.set_disabled_menu_buttons(["world_screen"])
        self.update_heading_text(f'{game.clan.name}Clan')
        self.show_menu_buttons()

        button_width = 228
        self.save_button = UIImageButton(scale(pygame.Rect(((1600 /2 - button_width/2, 1286), (button_width, 60)))), "", object_id="#save_button")
        self.save_button.enable()
        self.save_button_saved_state = pygame_gui.elements.UIImage(
            scale(pygame.Rect((686, 1286), (228, 60))),
            pygame.transform.scale(
                image_cache.load_image('resources/images/save_clan_saved.png'),
                (228, 60)))
        self.save_button_saved_state.hide()
        self.save_button_saving_state = pygame_gui.elements.UIImage(
            scale(pygame.Rect((686, 1286), (228, 60))),
            pygame.transform.scale(
                image_cache.load_image('resources/images/save_clan_saving.png'),
                (228, 60)))
        self.save_button_saving_state.hide()

        self.story_buttons = {}
        self.story_titles = {}
        stepsize = 60
        story_button_pos_y = 280
        story_button_pos_x = 200
        for story_id in range(game.dnd_config["max_story_amount"]):
            text = "story title"
            object_id = "#dnd_prof_free"
            if str(story_id) in game.clan.stories:# and game.clan.stories[str(story_id)]:
                self.story_titles[str(story_id)] = pygame_gui.elements.UITextBox(
                    text,
                    scale(pygame.Rect((story_button_pos_x + 46, story_button_pos_y - 20), (400, 80))),
                    object_id="#text_box_30_horizleft",
                    manager=MANAGER,
                )
                self.story_buttons[str(story_id)] = UIImageButton(
                    scale(pygame.Rect((story_button_pos_x, story_button_pos_y), (44, 44))), "", 
                    object_id=object_id,
                    tool_tip_text="nur ein test",
                    manager=MANAGER,
                    )
            story_button_pos_y += stepsize

        self.update_buttons_and_text()
        leveled_cats = get_leveled_cat()
        if (leveled_cats and not game.clan.level_reminder) or game.clan.levelable_cats < len(leveled_cats):
            game.clan.level_reminder = True
            game.clan.levelable_cats = len(leveled_cats)
            DnDLevelsReminder()

    def exit_screen(self):
        # Kill all other elements, and destroy the reference so they aren't hanging around
        self.save_button.kill()
        del self.save_button
        self.save_button_saved_state.kill()
        del self.save_button_saved_state
        self.save_button_saving_state.kill()
        del self.save_button_saving_state
        self.events_bg.kill()
        del self.events_bg
        self.events_frame.kill()
        del self.events_frame
        for id, story_button in self.story_buttons.items():
            story_button.kill()
        del self.story_buttons
        for id, story_button in self.story_titles.items():
            story_button.kill()
        del self.story_titles

        # reset save status
        game.switches['saved_clan'] = False

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

    def update_buttons_and_text(self):
        if game.switches['saved_clan']:
            self.save_button_saving_state.hide()
            self.save_button_saved_state.show()
            self.save_button.disable()
        else:
            self.save_button.enable()

