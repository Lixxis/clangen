from scripts.dnd.dnd_types import DnDSkillType, DnDEventRole
from typing import List, Dict, Optional, Union
from scripts.cat.cats import Cat
from random import randint


class DnDEventOutcome:
    def __init__(
            self, next_id = "",
            success:bool = True,
            text: str = None, 
            weight: int = 20, 
            exp: int = 0, 
            stat_trait: List[str] = None,
            stat_skill: List[str] = None,
            can_have_stat: List[str] = None,
            dead_cats: List[str] = None,
            lost_cats: List[str] = None,
            injury: List[Dict] = None,
            history_reg_death: str = None,
            history_leader_death: str = None,
            history_scar: str = None,
            new_cat: List[List[str]] = None,
            herbs: List[str] = None,
            prey: List[str] = None,
            outsider_rep: Union[int, None] = None,
            other_clan_rep: Union[int, None] = None,
            relationship_effects: List[dict] = None,
            relationship_constaints: List[str] = None,
            outcome_art: Union[str, None] = None,
            outcome_art_clean: Union[str, None] = None,
            stat_cat: Cat = None
        ) -> None:
        pass

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
            constraint: Dict[str, str] = None,
            text: List[str] = None,
            tags: List[str] = None,
            change: Dict[str, str] = None,
            new_cat: List[str] = None,
            roles: Dict[DnDEventRole, List[str]] = None,
            checks: Dict[str, DnDCheck] = None
        ) -> None:
        self.event_id = event_id
        self.constraint = constraint
        self.text = text
        self.tags = tags
        change = change
        new_cat = new_cat
        roles = roles
        checks = checks

class DnDStory:
    def __init__(
            self,
            story_id,
            current_event_id,
            start_cooldown: List[int] | int = None,
            decide_cooldown: List[int] | int = None,
            repeat_cooldown: List[int] | int = None,
            roles: Dict[DnDEventRole, List[str]] = None,
        ) -> None:
        self.story_id = story_id
        self.current_event_id = current_event_id
        self.start_cooldown = randint(start_cooldown[0],start_cooldown[1]) if isinstance(start_cooldown, list) else start_cooldown
        self.decide_cooldown = randint(decide_cooldown[0],decide_cooldown[1]) if isinstance(decide_cooldown, list) else decide_cooldown
        self.repeat_cooldown = randint(repeat_cooldown[0],repeat_cooldown[1]) if isinstance(repeat_cooldown, list) else repeat_cooldown
        self.roles = roles
    
    def add_role(self, role: DnDEventRole, cat_id: str):
        """Add a cat id to a role for this ongoing story."""
        if role in self.roles.keys():
            self.roles[role].append(cat_id)
        else:
            self.roles[role] = [cat_id]

    def skip_moon(self):
        if self.start_cooldown != None and self.start_cooldown:
            self.start_cooldown -= 1
        else:
            print("trigger event")

        if self.decide_cooldown != None and self.decide_cooldown:
            self.decide_cooldown -= 1
        else:
            print("decide the event")