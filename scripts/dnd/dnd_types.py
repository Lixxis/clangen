import logging
from enum import Enum
from typing import List, Dict

class LinageType(Enum):
    CAT = "cat"
    ELF = "elf"
    DWARF = "dwarf"
    ORC = "orc"
    DRAGONBORN = "dragonborn"
    GENASI = "genasi"

class CatSubLinageType(Enum):
    TABAXI = "tabaxi"
    LEONIN = "leonin"

class ElfSubLinageType(Enum):
    HIGH_ELF = "high elf"
    WOOD_ELF = "wood elf"
    DARK_ELF = "dark elf (drow)"
    SEA_ELF = "sea elf"
    ASTRAL_ELF = "astral elf"
    ELADRIN = "eladrin"

class DwarfSubLinageType(Enum):
    HILL_DWARF = "hill dwarf"
    MOUNTAIN_DWARF = "mountain dwarf"
    DUERGAR = "duergar"

class OrcSubLinageType(Enum):
    HILL_ORC = "hill orc"
    MOUNTAIN_ORC = "mountain orc"
    
class DragonbornSubLinageType(Enum):
    BLACK_DRAGON = "black dragon"
    BLUE_DRAGON = "blue dragon"
    BRASS_DRAGON = "brass dragon"
    BRONZE_DRAGON = "bronze dragon"
    COPPER_DRAGON = "copper dragon"
    GOLD_DRAGON = "gold dragon"
    GREEN_DRAGON = "green dragon"
    RED_DRAGON = "red dragon"
    SILVER_DRAGON = "silver dragon"
    WHITE_DRAGON = "white dragon"

class GenasiSubLinageType(Enum):
    AIR = "air"
    WATER = "water"
    FIRE = "fire"
    EARTH = "earth"

class StatType(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

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
    SLEIGHT_OF_PAW = "sleight of paw"
    STEALTH = "stealth"
    SURVIVAL = "survival"

class ClassType(Enum):
    BRUTE = "Brute"
    SILVER_TONGUE = "Silver tongue"
    CHOSEN = "Chosen of the StarClan"
    BLOOD_OLD = "Blood of the Old"
    SKILLED_WARRIOR = "Skilled Warrior"
    WISDOM = "Wisdom of the Paws"
    PROTECTOR = "Protector of StarClan"
    BLOOD_CHOSEN = "Blood of the Chosen One"
    KNOWLEDGE = "Knowledge Seeker"
    SWORN = "Sworn One"
    SHADOW = "Shadow Stalker"

class DnDEventRole(Enum):
    CLIENT = "client"
    PARTICIPANT = "participant"
    ALLY = "ally"
    ENEMY = "enemy"
    ANTAGONIST = "antagonist"
    KILL_TARGET = "kill target"
    SEARCH_TARGET = "search target"
    PRIOR_TARGET = "prior target"

def transform_roles_json_to_dict(json_data: Dict[str,List[str]]) -> Dict[DnDEventRole, List[str]]:
    """
    Transform the information of a loaded story with the data into a dictionary, which can be used in a DnDStory.
    """
    transformed_dict = {}
    for key in json_data.keys():
        fitting_role = [role for role in DnDEventRole if role.value == key]
        if fitting_role:
            transformed_dict[fitting_role[0]] = json_data[key]
        else:
            logging.error(f"DnD Error! loaded role '{key}' does not fit any DnDEventRole type.")
    return transformed_dict

def transform_roles_dict_to_json(dictionary: Dict[DnDEventRole, List[str]]) -> Dict[str,List[str]]:
    """
    Transform the dictionary to another form to be able to save it as such.
    """
    transformed_dict = {}
    for key in dictionary.keys():
        transformed_dict[key.value] = dictionary[key]
    return transformed_dict