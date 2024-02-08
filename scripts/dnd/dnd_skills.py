from scripts.cat.skills import SkillPath
from scripts.dnd.dnd_stats import Stats
from scripts.dnd.dnd_types import StatType, DnDSkillType, LinageType


class DnDSkills:
    """Represents the dnd skills for one cat."""
    skill_based = {
        StatType.STRENGTH: [
            DnDSkillType.ATHLETICS,
        ],
        StatType.DEXTERITY: [
            DnDSkillType.ACROBATICS,
            DnDSkillType.SLEIGHT_OF_PAW,
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

    skill_mapping = {
        SkillPath.TEACHER: DnDSkillType.HISTORY,
        SkillPath.HUNTER: DnDSkillType.SURVIVAL,
        SkillPath.FIGHTER: DnDSkillType.ATHLETICS,
        SkillPath.RUNNER: DnDSkillType.ACROBATICS,
        SkillPath.CLIMBER: DnDSkillType.ATHLETICS,
        SkillPath.SWIMMER: DnDSkillType.ACROBATICS,
        SkillPath.SPEAKER: DnDSkillType.DECEPTION,
        SkillPath.MEDIATOR: DnDSkillType.PERSUASION,
        SkillPath.CLEVER: DnDSkillType.INVESTIGATION,
        SkillPath.INSIGHTFUL: DnDSkillType.INSIGHT,
        SkillPath.SENSE: DnDSkillType.PERCEPTION,
        SkillPath.KIT: DnDSkillType.PERFORMANCE,
        SkillPath.STORY: DnDSkillType.PERFORMANCE,
        SkillPath.LORE: DnDSkillType.HISTORY,
        SkillPath.CAMP: DnDSkillType.SLEIGHT_OF_PAW,
        SkillPath.HEALER: DnDSkillType.MEDICINE,
        SkillPath.STAR: DnDSkillType.RELIGION,
        SkillPath.DARK: DnDSkillType.INTIMIDATION,
        SkillPath.OMEN: DnDSkillType.NATURE,
        SkillPath.DREAM: DnDSkillType.RELIGION,
        SkillPath.CLAIRVOYANT: DnDSkillType.ARCANA,
        SkillPath.PROPHET: DnDSkillType.ANIMAL_HANDLING,
        SkillPath.GHOST: DnDSkillType.STEALTH,
    }

    linage_proficiency = {
        LinageType.CAT : {
            "amount": 2,
            "prof":[
                {"skill": DnDSkillType.SURVIVAL, "chance": 20}
            ]
        },
        LinageType.ELF : {
            "amount": 2,
            "prof":[
                {"skill": DnDSkillType.SURVIVAL, "chance": 20}
            ]
        },
        LinageType.DWARF : {
            "amount": 2,
            "prof":[
                {"skill": DnDSkillType.SURVIVAL, "chance": 20}
            ]
        },
        LinageType.ORC : {
            "amount": 2,
            "prof":[
                {"skill": DnDSkillType.SURVIVAL, "chance": 20}
            ]
        }
    }

    backstory_categories_proficiency = {
        "loner_backstories": {
            "chance": 1,
            "proficiency": [],
        },
        "rogue_backstories": {
            "chance": 1,
            "proficiency": [],
        },
        "kittypet_backstories": {
            "chance": 1,
            "proficiency": [],
        },
        "former_clancat_backstories": {
            "chance": 1,
            "proficiency": [],
        },
        "healer_backstories": {
            "chance": 1,
            "proficiency": [],
        }
    }

    special_backstories_proficiency = {
        "guided1": {
            "chance": 1,
            "proficiency": [],
        },
        "guided2": {
            "chance": 1,
            "proficiency": [],
        },
        "guided3": {
            "chance": 1,
            "proficiency": [],
        },
        "guided4": {
            "chance": 1,
            "proficiency": [],
        },
        "disgraced1": {
            "chance": 1,
            "proficiency": [],
        },
        "disgraced2": {
            "chance": 1,
            "proficiency": [],
        },
        "disgraced3": {
            "chance": 1,
            "proficiency": [],
        },
        "medicine_cat": {
            "chance": 1,
            "proficiency": [],
        },
        "refugee3": {
            "chance": 1,
            "proficiency": [],
        },
        "refugee4": {
            "chance": 1,
            "proficiency": [],
        },
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
            DnDSkillType.SLEIGHT_OF_PAW: 0,
            DnDSkillType.STEALTH: 0,
            DnDSkillType.SURVIVAL: 0
        }
        self.proficiency = []
        if stats:
            self.update_skills(stats)

    def get_display_text(self, with_base = False, bold_skills = None):
        dnd_skill_string = ""
        skills_to_bold = bold_skills if bold_skills else []
        for skill, modifier in self.skills.items():
            mod_str = "+"
            if modifier < 0:
                mod_str = ""
            if skill in self.proficiency and len(skills_to_bold) < 1:
                dnd_skill_string += "<b>"
            elif skill in skills_to_bold:
                dnd_skill_string += "<b>"
            dnd_skill_string += f"{skill.value} (" + mod_str + str(modifier) + ") "

            if with_base:
                for base, value_list in self.skill_based.items():
                    if skill in value_list:
                        dnd_skill_string += f" - <i>{base.value} based </i><br>"
            else:
                dnd_skill_string += "<br>"

            if skill in self.proficiency and len(skills_to_bold) < 1:
                dnd_skill_string += "</b>"
            elif skill in skills_to_bold:
                dnd_skill_string += "</b>"
        return dnd_skill_string

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
            modifier = stats.modifier[stats.genetic_stats[stat_type]]
            for skill_type in self.skill_based[stat_type]:
                self.skills[skill_type] = modifier
        # add the proficiency bonus
        for proficiency_type in self.proficiency:
            self.skills[proficiency_type] += 1
