
from enum import Enum

from scripts.dnd.dnd_stats import StatType, Stats


class DnDSkillType(Enum):
    ACROBATICS = "acrobatics"
    ANIMAL_HANDLING = "animal handling"
    ARCANA = "arcana"
    ATHLETICS = "athletics"
    DECEPTION = "deception"
    HISTORY = "history"
    INSIGHT = "insight"
    INTIMIDATION = "intimidation"
    INVESTIGATION = "investigation"
    MEDICINE = "medicine"
    NATURE = "nature"
    PERCEPTION = "perception"
    PERFORMANCE = "performance"
    PERSUASION = "persuasion"
    RELIGION = "religion"
    SLEIGHT_OF_HAND = "sleight of hand"
    STEALTH = "stealth"
    SURVIVAL = "survival"
    

class DnDSkills:
    """Represents the dnd skills for one cat."""
    skill_based = {
        StatType.STRENGTH: [
            DnDSkillType.ATHLETICS,
        ],
        StatType.DEXTERITY: [
            DnDSkillType.ACROBATICS,
            DnDSkillType.SLEIGHT_OF_HAND,
            DnDSkillType.STEALTH,
        ],
        StatType.CONSTITUTION: [],
        StatType.INTELLIGENCE: [
            DnDSkillType.ARCANA,
            DnDSkillType.HISTORY,
            DnDSkillType.INVESTIGATION,
            DnDSkillType.NATURE,
            DnDSkillType.PERSUASION,
            DnDSkillType.RELIGION,
        ],
        StatType.WISDOM: [
            DnDSkillType.ANIMAL_HANDLING,
            DnDSkillType.INSIGHT,
            DnDSkillType.MEDICINE,
            DnDSkillType.PERCEPTION,
            DnDSkillType.SURVIVAL,
        ],
        StatType.CHARISMA: [
            DnDSkillType.DECEPTION,
            DnDSkillType.INTIMIDATION,
            DnDSkillType.PERFORMANCE,
        ],
    }

    def __init__(self, stats = None):
        self.skills = {
            DnDSkillType.ACROBATICS: 0,
            DnDSkillType.ANIMAL_HANDLING: 0,
            DnDSkillType.ARCANA: 0,
            DnDSkillType.ATHLETICS: 0,
            DnDSkillType.DECEPTION: 0,
            DnDSkillType.HISTORY: 0,
            DnDSkillType.INSIGHT: 0,
            DnDSkillType.INTIMIDATION: 0,
            DnDSkillType.INVESTIGATION: 0,
            DnDSkillType.MEDICINE: 0,
            DnDSkillType.NATURE: 0,
            DnDSkillType.PERCEPTION: 0,
            DnDSkillType.PERFORMANCE: 0,
            DnDSkillType.PERSUASION: 0,
            DnDSkillType.RELIGION: 0,
            DnDSkillType.SLEIGHT_OF_HAND: 0,
            DnDSkillType.STEALTH: 0,
            DnDSkillType.SURVIVAL: 0
        }
        self.proficiency = []
        if stats:
            self.update_skills(stats)

    def set_proficiency(self, skill_type: DnDSkillType):
        if skill_type not in self.proficiency:
            self.proficiency.append(skill_type)
            self.skills[skill_type] += 1

    def remove_proficiency(self, skill_type: DnDSkillType):
        if skill_type in self.proficiency:
            self.proficiency.remove(skill_type)
            self.skills[skill_type] -= 1

    def get_proficiency_list(self):
        return [skill.value for skill in self.proficiency]

    def load_proficiency_list(self, list):
        for skill_value in list:
            keys = [key for key in DnDSkillType if key.value == skill_value]
            if keys:
                self.proficiency.append(keys[0])
                self.skills[keys[0]] += 1

    def update_skills(self, stats: Stats):
        # set all the skills according to the connected stats
        for stat_type in self.skill_based.keys():
            modifier = stats.modifier[stats._stats[stat_type]]
            for skill_type in self.skill_based[stat_type]:
                self.skills[skill_type] = modifier
        # add the proficiency bonus
        for proficiency_type in self.proficiency:
            self.skills[proficiency_type] += 1
        return