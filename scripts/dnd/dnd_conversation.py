from typing import List, Dict, Optional

class DnDConversation:
    def __init__(self, id, text, answers) -> None:
        self.id = id
        self.text = text
        self.answers = answers
    
    def get_text(self, amount_of_cats) -> str:
        "Returns the text of this conversation based on the amount of cats in the patrol."
        if len(self.text) >= amount_of_cats:
            return self.text[amount_of_cats-1]
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

        for key, _d in info.items():
            conversation_dict[key] = DnDConversation(
                id = _d.get("id"),
                text = _d.get("text"),
                answers= _d.get("answers")
            )
        return conversation_dict
