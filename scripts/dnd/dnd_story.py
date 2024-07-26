import os
import ujson
import logging
from typing import List, Dict
from random import randint
from scripts.dnd.dnd_event import DnDEvent
from scripts.dnd.dnd_types import DnDEventRole, transform_roles_dict_to_json

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
            start_countdown: List[int] | int = None,
            decide_countdown: List[int] | int = None,
            repeat_countdown: List[int] | int = None,
            roles: Dict[DnDEventRole, List[str]] = None,
        ) -> None:
        self.story_id = story_id
        self.current_event_id = current_event_id
        self.start_countdown = randint(start_countdown[0],start_countdown[1]) if isinstance(start_countdown, list) else start_countdown
        self.decide_countdown = randint(decide_countdown[0],decide_countdown[1]) if isinstance(decide_countdown, list) else decide_countdown
        self.repeat_countdown = randint(repeat_countdown[0],repeat_countdown[1]) if isinstance(repeat_countdown, list) else repeat_countdown
        self.roles = roles
    
    def add_role(self, role: DnDEventRole, cat_id: str):
        """Add a cat id to a role for this ongoing story."""
        if role in self.roles.keys():
            self.roles[role].append(cat_id)
        else:
            self.roles[role] = [cat_id]

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
            "repeat_countdown": self.repeat_countdown,
            "roles": transform_roles_dict_to_json(self.roles)
        }
        return usable_dict

    def __str__(self):
        return str(self.to_json())

    @staticmethod
    def get_start_events() -> List[DnDEvent]:
        """Returns a list of all events which can be a trigger for a story to unfold."""
        trigger_events = []

        for key, value in DnDStory.EVENTS_DICT.items():
            if value.start_event:
                trigger_events.append(value)

        return trigger_events