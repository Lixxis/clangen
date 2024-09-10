from typing import Dict, Optional
from random import randint

from scripts.cat.cats import Cat
from scripts.dnd.dnd_types import DnDSkillType
from scripts.dnd.dnd_event_outcome import DnDEventOutcome
from scripts.game_structure.game_essentials import game

class DnDCheck:
    def __init__(
            self,
            skill_type: Optional[DnDSkillType],
            pass_number: Optional[int],
            success_outcome: Dict[str, DnDEventOutcome],
            fail_outcome: Dict[str, DnDEventOutcome],
            duplicate: str | None = None
        ) -> None:
        self.skill_type = skill_type
        self.pass_number = pass_number if pass_number else game.dnd_config["default_pass_number"]
        self.success_outcome = success_outcome
        self.fail_outcome = fail_outcome
        self.duplicate = duplicate

    def roll_skill(self, cat: Optional[Cat] = None) -> tuple:
        rolled_number = randint(1, 20) # d20 roll
        modifier = 0
        print("DICE - rolled number: ", rolled_number)
        if self.skill_type and cat:
            print("; modifier: ", cat.dnd_skills.skills[self.skill_type])
            modifier = cat.dnd_skills.skills[self.skill_type]
        final_number = rolled_number + modifier
        print("DICE - finished rolled number: ", final_number, ", needed number: ", self.pass_number)

        final_outcome = None
        outcome_key = None
        success = final_number >= self.pass_number
        #success = True
        outcome_number = final_number if rolled_number not in [1,20] else rolled_number
        critical = outcome_number == rolled_number
        if success:
            print("DICE - SUCCESS!")
            outcome_key = "gen"
            if str(outcome_number) in self.success_outcome.keys():
                outcome_key = str(outcome_number)
            final_outcome = self.success_outcome[outcome_key]
        else:
            print("DICE - NO success!")
            outcome_key = "gen"
            if str(outcome_number) in self.fail_outcome.keys():
                outcome_key = str(outcome_number)
            final_outcome = self.fail_outcome[outcome_key]

        print("DICE - outcome_key", outcome_key)

        return success, critical, final_outcome, final_outcome

    @staticmethod
    def generate_from_info(info: Dict[str, dict]) -> Dict[str, 'DnDCheck']:
        """Factory method generates a list of DnDCheck objects based on the dicts."""
        check_dict = {}
        for key, _d in info.items():
            skill = _d.get("id")
            skill = [skill for skill in DnDSkillType if skill.name == skill]
            if len(skill) > 0:
                skill = skill[0]
            else:
                skill = None
            success_outcome = {}
            if _d.get("success"):
                for outcome_key, outcome_value in _d.get("success").items():
                    success_outcome[outcome_key] = DnDEventOutcome.generate_from_info([outcome_value])[0]
            fail_outcome = {}
            if _d.get("fail"):
                for outcome_key, outcome_value in _d.get("fail").items():
                    fail_outcome[outcome_key] = DnDEventOutcome.generate_from_info([outcome_value])[0]
            check_dict[key] = DnDCheck(
                skill_type = skill,
                pass_number = _d.get("pass"),
                success_outcome=success_outcome,
                fail_outcome=fail_outcome,
                duplicate=_d.get("duplicate")
            )
        return check_dict
