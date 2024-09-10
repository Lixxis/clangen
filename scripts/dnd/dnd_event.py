from typing import List, Dict
import logging
from copy import deepcopy

from scripts.dnd.dnd_types import DnDEventRole
from scripts.dnd.dnd_check import DnDCheck
from scripts.dnd.dnd_conversation import DnDConversation

class DnDEvent:
    def __init__(
            self,
            event_id,
            start_event: bool = False,
            constraints: Dict[str, str] = None,
            conversations: Dict[str, DnDConversation] = None,
            current_conversation_id: str = "start",
            tags: List[str] = None,
            start_cooldown: List[int] = None,
            decide_cooldown: List[int] = None,
            change: Dict[str, str] = None,
            new_cats: List[str] = None,
            roles: Dict[DnDEventRole, List[str]] = None,
            checks: Dict[str, DnDCheck] = None
        ) -> None:
        self.event_id = event_id
        self.start_event = start_event
        self.constraints = constraints
        self.conversations = conversations if conversations else {}
        self.current_conversation_id = current_conversation_id
        self.tags = tags if tags else []
        self.start_cooldown = start_cooldown if start_cooldown else [1]
        self.decide_cooldown = decide_cooldown if decide_cooldown else [1]
        self.change = change if change else {}
        self.new_cats = new_cats if new_cats else []
        self.roles = roles if roles else {}
        self.checks = checks if checks else {}
        self.wandering_cats = []
        self.random_cat = None

        self.current_conversation = None
        self.set_current_conversation()

    def _check_constraints(self) -> bool:
        return True

    def continue_conversation(self, chosen_answer_id) -> None:
        """Handles to switch to the new conversation."""
        if not chosen_answer_id:
            logging.error(f"DnD Error! - nothing was chosen as answer")
            return
        if not self.current_conversation_id:
            logging.error(f"DnD Error! - the next id is missing")
            return
        if self.current_conversation_id not in self.conversations.keys():
            logging.error(f"DnD ERROR! - the conversation with the key {self.current_conversation_id} is missing in event {self.event_id}")
            return
        if chosen_answer_id not in self.conversations.keys():
            logging.error(f"DnD ERROR! - the conversation with the key {chosen_answer_id} is missing in event {self.event_id}")
            return

        self.current_conversation_id = chosen_answer_id
        self.set_current_conversation()

    def set_current_conversation(self) -> None:
        """Set the text and answers for the current conversation in values."""
        if not self.current_conversation_id:
            logging.error(f"DnD Error! - the next id is missing")
            return
        if self.current_conversation_id not in self.conversations:
            logging.error(f"DnD ERROR! - the conversation with the key {self.current_conversation_id} is missing in event {self.event_id}")
            return
        self.current_conversation = self.conversations[self.current_conversation_id]

    @staticmethod
    def generate_from_info(info: Dict[str, dict]) -> Dict[str,'DnDEvent']:
        """Factory method generates a list of DnDConversation objects based on the Dict."""
        event_dict = {}

        for key, value in info.items():
            checks = DnDCheck.generate_from_info(value.get("checks"))
            duplicate_check_ids = [id for id in checks.keys() if checks[id].duplicate]
            for check_id in duplicate_check_ids:
                checks[check_id] = deepcopy(checks[checks[check_id].duplicate])

            event_dict[key] = DnDEvent(
                event_id = key,
                start_event = value.get("start_event"),
                constraints = value.get("constraints"),
                conversations = DnDConversation.generate_from_info(value.get("conversations")),
                tags = value.get("tags"),
                start_cooldown = value.get("start_cooldown"),
                decide_cooldown = value.get("decide_cooldown"),
                change = value.get("change"),
                new_cats = value.get("new_cat"),
                roles = value.get("roles"),
                checks = checks,
            )
        return event_dict
