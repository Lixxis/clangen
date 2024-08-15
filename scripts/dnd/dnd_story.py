import os
import ujson
import logging
from copy import deepcopy
from random import choice
from typing import List, Dict
from random import randint
from scripts.cat.cats import Cat
from scripts.cat_relations.relationship import Relationship
from scripts.dnd.dnd_event import DnDEvent
from scripts.dnd.dnd_types import DnDEventRole, transform_roles_dict_to_json
from scripts.game_structure.game_essentials import game
from scripts.utility import (
    create_new_cat_block,
    process_text,
)

class DnDStory:
    
    base_path = os.path.join(
        "resources",
        "dicts",
        "dnd_stories"
    )

    EVENTS_DICT = {}
    for smaller_stories in os.listdir(base_path):
        file_path = os.path.join(base_path, smaller_stories)
        with open(file_path, 'r') as read_file:
            file_content = ujson.load(read_file)
            EVENTS_DICT.update(DnDEvent.generate_from_info(file_content))
            
    del base_path

    def __init__(
            self,
            story_id,
            current_event_id,
            current_conversation_id: str = "start",
            start_countdown: List[int] | int = 1,
            decide_countdown: List[int] | int = 1,
            roles: Dict[DnDEventRole, List[str]] = None,
        ) -> None:
        self.story_id = story_id
        self.current_event_id = current_event_id
        self.current_conversation_id = current_conversation_id
        if self.current_event_id in  DnDStory.EVENTS_DICT:
            self.current_event = deepcopy(DnDStory.EVENTS_DICT[self.current_event_id])
        self.start_countdown = randint(start_countdown[0],start_countdown[1]) if isinstance(start_countdown, list) else start_countdown
        self.decide_countdown = randint(decide_countdown[0],decide_countdown[1]) if isinstance(decide_countdown, list) else decide_countdown
        self.roles = roles if roles else {}
    
    def add_role(self, role: DnDEventRole, cat_id: str):
        """Add a cat id to a role for this ongoing story."""
        if role in self.roles.keys():
            self.roles[role].append(cat_id)
        else:
            self.roles[role] = [cat_id]

    def update_countdown(self, countdown_type: str , countdown: List[int]):
        "Update the countdown of the story"
        countdown_to_use = 1
        if isinstance(countdown, int):
            countdown_to_use = countdown
        elif len(countdown) == 1:
            countdown_to_use = countdown[0]
        elif len(countdown) > 1:
            countdown_to_use = randint(countdown[0],countdown[1]) if isinstance(countdown, list) else 1
        elif countdown_type == "start":
            self.start_countdown = countdown_to_use
        elif countdown_type == "decide":
            self.decide_countdown = countdown_to_use

    def skip_moon(self):
        """Reduce every"""
        if self.start_countdown != None and self.start_countdown > 0:
            self.start_countdown -= 1
        else:
            logging.info("trigger event - or it is now shown in the patrol ?")

        # if the event already started count down the decision
        if not self.start_countdown or self.start_countdown <= 0:
            if self.decide_countdown != None and self.decide_countdown > 0:
                self.decide_countdown -= 1
            else:
                self.random_event_continue()

    def continue_story(self, cat_dict):
        if self.current_event_id in  DnDStory.EVENTS_DICT:
            self.current_event = deepcopy(DnDStory.EVENTS_DICT[self.current_event_id])
            
        if not self.current_event:
            print(f"ERROR DnD: the event {self.current_event_id} can't be found!")
            return

        # first create new cats if needed
        if self.current_event.new_cats:
            new_cats = deepcopy(self.current_event.new_cats)
            self.current_event.new_cats = []
            for i, attribute_list in enumerate(new_cats):
                n_c = create_new_cat_block(Cat, Relationship, self.current_event, cat_dict, i, attribute_list)
                self.current_event.new_cats.append(
                    n_c
                )
                cat_dict[f"n_c:{i}"] = (str(n_c[0].name), choice(n_c[0].pronouns))
        
        self.update_roles()

        current_conversation = self.current_event.conversations[self.current_conversation_id]
        return self.current_event, current_conversation

    def update_roles(self):
        """Update all the roles of the story according to the current event."""
        for role_name, cats_list in self.current_event.roles.items():
            fitting_role = [role.value for role in DnDEventRole if role.value == role_name]
            if len(fitting_role) > 0:
                fitting_role = fitting_role[0]
            else:
                logging.error(f"DnD Error! loaded role '{role_name}' does not fit any DnDEventRole type.")
                continue
            cats_to_append = []
            for cat_shortcut in cats_list:
                cat_info = cat_shortcut.split(":")
                cat_role_location = cat_info[0]
                cat_index = int(cat_info[1])

                cat_id = None
                if cat_role_location == "n_c":
                    cat_id = self.current_event.new_cats[cat_index][0].ID
                else:
                    old_fitting_role = [role for role in DnDEventRole if role.value == cat_role_location]
                    cat_id = self.roles[old_fitting_role][cat_index]

                if cat_id:
                    cats_to_append.append(cat_id)
                    if fitting_role == DnDEventRole.SEARCH_TARGET.value:
                        game.clan.dnd_unknown_cats[cat_id] = ["look"]


            if fitting_role in self.roles.keys():
                self.roles[fitting_role].extend(cats_to_append)
            else:
                self.roles[fitting_role] = cats_to_append

            game.clan.stories["NPC"].extend(cats_to_append)

    def handle_outcome(self, skill_to_roll, cat_to_roll):
        if skill_to_roll in self.current_event.checks.keys():
            roll_check = self.current_event.checks[skill_to_roll]
            was_success, critical_success, rolled_number, outcome = roll_check.roll_skill(cat_to_roll)
            if outcome:
                self.current_event_id = outcome.next_id
                next_event = DnDStory.EVENTS_DICT[outcome.next_id]
                self.update_countdown("start", next_event.start_cooldown)
                self.update_countdown("decide", next_event.decide_cooldown)
                return outcome.text[0]
            return "No outcome was found"
        return "Selected skill not defined as a check"

    def random_event_continue(self):
        """
        Handles to continue the story on a random bases.
        """
        print("DnD - random_event_continue (WIP)")

    def to_json(self):
        """Transform the story into a saveable format."""
        usable_dict = {
            "story_id": self.story_id,
            "current_event_id": self.current_event_id,
            "start_countdown": self.start_countdown,
            "decide_countdown": self.decide_countdown,
            "roles": transform_roles_dict_to_json(self.roles)
        }
        return usable_dict

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def generate_from_info(info: Dict[str, dict]) -> Dict[str,'DnDStory']:
        story_dict = {}

        for key, value in info.items():
            if key == "NPC" or not value:
                story_dict[key] = value
                continue
            roles_dict = {}
            roles_info = value.get("roles")
            for role_key, role_value in roles_info.items():
                fitting_role = [role.value for role in DnDEventRole if role.value == role_key]
                if fitting_role:
                    roles_dict[fitting_role[0]] = role_value
                else:
                    logging.error(f"DnD Error! loaded role '{role_key}' does not fit any DnDEventRole type.")
            story = DnDStory(
                story_id = key,
                current_event_id = value.get("current_event_id"),
                start_countdown = value.get("start_countdown"),
                decide_countdown = value.get("decide_countdown"),
                roles=roles_dict
            )
            story_dict[key] = story

        return story_dict

    @staticmethod
    def get_start_events() -> List[DnDEvent]:
        """Returns a list of all events which can be a trigger for a story to unfold."""
        trigger_events = []

        for key, value in DnDStory.EVENTS_DICT.items():
            if value.start_event:
                trigger_events.append(value)

        return trigger_events
