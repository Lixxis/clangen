from typing import List, Dict, Optional
from random import randint
import logging

from scripts.dnd.dnd_types import DnDSkillType, DnDEventRole
from scripts.dnd.dnd_event_outcome import DnDEventOutcome
from scripts.cat.cats import Cat

# implement conversation like cat selection
class DnDConversation:
    def __init__(self, id, text, answers) -> None:
        self.id = id
        self.text = text
        self.answers = answers
    
    def get_text(self, amount_of_cats) -> str:
        "Returns the text of this conversation based on the amount of cats in the patrol."
        if len(self.text) >= amount_of_cats:
            return self.text[amount_of_cats]
        elif len(self.text) > 0:
            return self.text[0]
        return f"There is no conversation text found for conversation with the id {self.id}!"

    def get_all_answer_text(self) -> List[str]:
        "Returns all the answers which are possible for this conversation."
        if len(self.answers) == 0:
            return None
        if len(self.answers) == 1:
            # if there is only one answer it is the list of possible rolling checks
            return []
        return [answer[1] for answer in self.answers]

    def get_next_id(self, chosen_answer) -> str:
        "Returns the next id of the answer."
        next_id = None
        for answer in self.answers:
            if chosen_answer in answer:
                return chosen_answer[0]
        return next_id

    def get_check_type(self) -> Optional[List[str]]:
        "Returns the type of check if the only answer is an roll check."
        if len(self.answers) == 1:
            return self.answers[0]
        return None

    @staticmethod
    def generate_from_info(info: Dict[str, dict]) -> Dict[str,'DnDConversation']:
        """Factory method generates a list of DnDConversation objects based on the dicts."""
        conversation_dict = {}

        if not isinstance(info, list):
            return conversation_dict

        for key, _d in info.items():
            conversation_dict[key] = DnDConversation(
                id = _d.get("id"),
                text = _d.get("text"),
                answers= _d.get("answers")
            )
        return conversation_dict

class DnDCheck:
    def __init__(
            self,
            skill_type: Optional[DnDSkillType],
            pass_number: int,
            success_outcome: Dict[str,DnDEventOutcome],
            fail_outcome: Dict[str,DnDEventOutcome]
        ) -> None:
        self.skill_type = skill_type
        self.pass_number = pass_number
        self.success_outcome = success_outcome
        self.fail_outcome = fail_outcome

    def roll_skill(self, cat: Cat) -> bool:
        rolled_number = randint(1,20) # d20 roll
        print("ROLLED NUMBER: ", rolled_number , "; modifier: ", cat.dnd_skills.skills[self.skill_type])
        modifier = cat.dnd_skills.skills[self.skill_type]
        final_number = rolled_number + modifier # modifier added
        print("FINISHED ROLLED NUMBER: ", final_number, ", needed number: ", self.pass_number)

        final_event = self.chosen_success
        if self.pass_number > final_number:
            print("NO success")
            final_event = self.chosen_failure
        else:
            print("SUCCESS!")
        return final_event.execute_outcome(self, cat) + (rolled_number,) + (modifier,) + (self.pass_number,)

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
            new_cat: List[str] = None,
            roles: Dict[DnDEventRole, List[str]] = None,
            checks: Dict[str, DnDCheck] = None
        ) -> None:
        self.event_id = event_id
        self.start_event = start_event
        self.constraints = constraints
        self.conversations = conversations if conversations else {}
        self.current_conv_id = current_conversation_id
        self.tags = tags if tags else []
        self.start_cooldown = start_cooldown if start_cooldown else []
        self.decide_cooldown = decide_cooldown if decide_cooldown else []
        self.change = change if change else {}
        self.new_cat = new_cat if new_cat else []
        self.roles = roles if roles else {}
        self.checks = checks if checks else {}

        self.current_conversation = None
        self.get_current_conversation()

    def _check_constraints(self) -> bool:
        return True

    def continue_conversation(self, chosen_answer) -> None:
        """Handles to switch to the new conversation."""
        if not chosen_answer:
            logging.error(f"DnD Error! - nothing was chosen as answer")
            return
        if not self.current_conv_id:
            logging.error(f"DnD Error! - the next id is missing")
            return
        if self.current_conv_id not in self.conversations.keys():
            logging.error(f"DnD ERROR! - the conversation with the key {self.current_conv_id} is missing in event {self.event_id}")
            return
        upcoming_id = self.conversations[self.current_conv_id].get_next_id(chosen_answer)
        if not upcoming_id:
            logging.error(f"DnD Error! - the next id is not set for the answer '{chosen_answer}'")
            return
        if upcoming_id not in self.conversations.keys():
            logging.error(f"DnD ERROR! - the conversation with the key {upcoming_id} is missing in event {self.event_id}")
            return
        self.current_conv_id = upcoming_id
        self.current_conversation = self.get_current_conversation()

    def get_current_conversation(self) -> None:
        """Set the text and answers for the current conversation in values."""
        if not self.current_conv_id:
            logging.error(f"DnD Error! - the next id is missing")
            return
        if self.current_conv_id not in self.conversations:
            logging.error(f"DnD ERROR! - the conversation with the key {self.current_conv_id} is missing in event {self.event_id}")
            return
        self.current_conversation = self.conversations[self.current_conv_id]

    @staticmethod
    def generate_from_info(info: Dict[str, dict]) -> Dict[str,'DnDEvent']:
        """Factory method generates a list of DnDConversation objects based on the Dict."""
        event_dict = {}

        if not isinstance(info, list):
            return event_dict

        for key, value in info.items():
            event_dict[key] = DnDConversation(
                event_id = key,
                start_event = value.get("start_event"),
                constraints = value.get("constraints"),
                conversations = DnDConversation.generate_from_info(value.get("conversations")),
                current_conversation = value.get("current_conversation"),
                tags = value.get("tags"),
                start_cooldown = value.get("start_cooldown"),
                decide_cooldown = value.get("decide_cooldown"),
                change = value.get("change"),
                new_cat = value.get("new_cat"),
                roles = value.get("roles"),
                checks = value.get("checks"),
            )
        return event_dict


        """Returns a list of all events which can be a trigger for a story to unfold."""
        trigger_events = []

        for key, value in self.EVENTS_DICT.items():
            if value.start_event:
                trigger_events.append(value)

        return trigger_events