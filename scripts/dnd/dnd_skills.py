from scripts.cat.skills import SkillPath
from scripts.dnd.dnd_stats import Stats
from scripts.dnd.dnd_types import StatType, DnDSkillType, LinageType, ClassType
from scripts.game_structure.game_essentials import game


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

    class_proficiency_dict = {
        ClassType.BRUTE : 			[DnDSkillType.ATHLETICS, DnDSkillType.SURVIVAL, DnDSkillType.INTIMIDATION],
        ClassType.SILVER_TONGUE : 	[DnDSkillType.PERFORMANCE, DnDSkillType.DECEPTION, DnDSkillType.PERSUASION],
        ClassType.CHOSEN : 			[DnDSkillType.RELIGION, DnDSkillType.MEDICINE, DnDSkillType.INSIGHT],
        ClassType.BLOOD_OLD : 		[DnDSkillType.NATURE, DnDSkillType.SURVIVAL, DnDSkillType.ANIMAL_HANDLING],
        ClassType.SKILLED_WARRIOR :	[DnDSkillType.ACROBATICS, DnDSkillType.ATHLETICS, DnDSkillType.INTIMIDATION],
        ClassType.WISDOM : 			[DnDSkillType.ACROBATICS, DnDSkillType.RELIGION, DnDSkillType.INSIGHT],
        ClassType.PROTECTOR : 		[DnDSkillType.ATHLETICS, DnDSkillType.RELIGION, DnDSkillType.HISTORY],
        ClassType.BLOOD_CHOSEN : 	[DnDSkillType.ARCANA, DnDSkillType.HISTORY, DnDSkillType.SLEIGHT_OF_PAW],
        ClassType.KNOWLEDGE : 		[DnDSkillType.ARCANA, DnDSkillType.PERCEPTION, DnDSkillType.HISTORY],
        ClassType.SWORN : 			[DnDSkillType.ARCANA, DnDSkillType.HISTORY, DnDSkillType.PERSUASION],
        ClassType.SHADOW : 			[DnDSkillType.STEALTH, DnDSkillType.SLEIGHT_OF_PAW, DnDSkillType.INVESTIGATION],
    }

    class_prof_description = {
        ClassType.BRUTE :
        f"<b>'Barbarian' - {ClassType.BRUTE.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.BRUTE][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.BRUTE][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.BRUTE][2].value}",
        ClassType.SILVER_TONGUE :
        f"<b>'Bard' - {ClassType.SILVER_TONGUE.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.SILVER_TONGUE][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.SILVER_TONGUE][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.SILVER_TONGUE][2].value}",
        ClassType.CHOSEN :
        f"<b>'Cleric' - {ClassType.CHOSEN.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.CHOSEN][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.CHOSEN][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.CHOSEN][2].value}",
        ClassType.BLOOD_OLD :
        f"<b>'Druid' - {ClassType.BLOOD_OLD.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.BLOOD_OLD][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.BLOOD_OLD][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.BLOOD_OLD][2].value}",
        ClassType.SKILLED_WARRIOR :
        f"<b>'Fighter' - {ClassType.SKILLED_WARRIOR.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.SKILLED_WARRIOR][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.SKILLED_WARRIOR][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.SKILLED_WARRIOR][2].value}",
        ClassType.WISDOM :
        f"<b>'Monk' - {ClassType.WISDOM.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.WISDOM][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.WISDOM][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.WISDOM][2].value}",
        ClassType.PROTECTOR :
        f"<b>'Paladin' - {ClassType.PROTECTOR.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.PROTECTOR][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.PROTECTOR][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.PROTECTOR][2].value}",
        ClassType.BLOOD_CHOSEN :
        f"<b>'Sorcerer' - {ClassType.BLOOD_CHOSEN.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.BLOOD_CHOSEN][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.BLOOD_CHOSEN][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.BLOOD_CHOSEN][2].value}",
        ClassType.KNOWLEDGE :
        f"<b>'Wizard' - {ClassType.KNOWLEDGE.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.KNOWLEDGE][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.KNOWLEDGE][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.KNOWLEDGE][2].value}",
        ClassType.SWORN :
        f"<b>'Warlock' - {ClassType.SWORN.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.SWORN][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.SWORN][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.SWORN][2].value}",
        ClassType.SHADOW :
        f"<b>'Rogue' - {ClassType.SHADOW.value}</b> <br>Bonuses: <br>" + 
        f"- level 2 {class_proficiency_dict[ClassType.SHADOW][0].value} <br>" + 
        f"- level 8 {class_proficiency_dict[ClassType.SHADOW][1].value} <br>" + 
        f"- level 14 {class_proficiency_dict[ClassType.SHADOW][2].value}",
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
        self.class_proficiency = []
        self.used_class = {}
        if stats:
            self.update_skills(stats)

    def get_display_text(self, with_base = False, bold_skills = None):
        dnd_skill_string = ""
        skills_to_bold = bold_skills if bold_skills else []
        for skill, modifier in self.skills.items():
            mod_str = "+"
            if modifier < 0:
                mod_str = ""
            if (skill in self.proficiency or skill in self.class_proficiency) and len(skills_to_bold) < 1:
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

            if (skill in self.proficiency or skill in self.class_proficiency) and len(skills_to_bold) < 1:
                dnd_skill_string += "</b>"
            elif skill in skills_to_bold:
                dnd_skill_string += "</b>"
        return dnd_skill_string

    def set_proficiency(self, skill_type: DnDSkillType):
        if skill_type not in self.proficiency:
            self.proficiency.append(skill_type)
            self.skills[skill_type] += game.dnd_config["proficiency_bonus"]

    def remove_proficiency(self, skill_type: DnDSkillType):
        if skill_type in self.proficiency:
            self.proficiency.remove(skill_type)
            self.skills[skill_type] -= game.dnd_config["proficiency_bonus"]

    def update_class_proficiency(self, dnd_class: ClassType, current_level):
        if not dnd_class or not current_level:
            return
        level_nr = int(current_level.split(" ")[1])
        if dnd_class == ClassType.BLOOD_CHOSEN and "level 0" not in self.used_class:
            self.used_class["level 0"] = dnd_class
            self.class_proficiency.append(self.class_proficiency_dict[dnd_class][0])
            self.skills[self.class_proficiency_dict[dnd_class][0]] += 1
        if "level 2" not in self.used_class and level_nr >= 2:
            self.used_class["level 2"] = dnd_class
            self.class_proficiency.append(self.class_proficiency_dict[dnd_class][0])
            self.skills[self.class_proficiency_dict[dnd_class][0]] += 1
        if "level 8" not in self.used_class and level_nr >= 8:
            self.used_class["level 8"] = dnd_class
            self.class_proficiency.append(self.class_proficiency_dict[dnd_class][1])
            self.skills[self.class_proficiency_dict[dnd_class][1]] += 1
        if "level 14" not in self.used_class and level_nr >= 14:
            self.used_class["level 14"] = dnd_class
            self.class_proficiency.append(self.class_proficiency_dict[dnd_class][2])
            self.skills[self.class_proficiency_dict[dnd_class][2]] += 1

    def get_proficiency_list(self):
        return [skill.value for skill in self.proficiency]

    def get_class_proficiency(self):
        return_dict = {}
        for key, value in self.used_class.items():
            return_dict[key] = value.value
        return return_dict

    def load_class_proficiency(self, object):
        for level, dnd_class_name in object.items():
            dnd_class = [c for c in ClassType if c.value == dnd_class_name]
            if dnd_class:
                self.used_class[level] = dnd_class[0]
                index = 0
                if level == "level 8":
                    index = 1
                elif level == "level 14":
                    index = 2
                self.class_proficiency.append(self.class_proficiency_dict[dnd_class[0]][index])
                self.skills[self.class_proficiency_dict[dnd_class[0]][index]] += game.dnd_config["proficiency_bonus"]

    def load_proficiency_list(self, list):
        for skill_value in list:
            keys = [key for key in DnDSkillType if key.value == skill_value]
            if keys:
                self.proficiency.append(keys[0])
                self.skills[keys[0]] += game.dnd_config["proficiency_bonus"]

    def update_skills(self, cat_stats: Stats):
        # set all the skills according to the connected stats
        for stat_type in self.skill_based.keys():
            modifier = cat_stats.modifier[cat_stats.stats[stat_type]]
            for skill_type in self.skill_based[stat_type]:
                self.skills[skill_type] = modifier
        # add the proficiency bonus
        for proficiency_type in self.proficiency:
            self.skills[proficiency_type] += game.dnd_config["proficiency_bonus"]
        # add the proficiency bonus
        for proficiency_type in self.class_proficiency:
            self.skills[proficiency_type] += game.dnd_config["proficiency_bonus"]
