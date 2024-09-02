from random import choice
from enum import Enum
from typing import List, Dict, Any

from scripts.game_structure.game_essentials import game

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

def transform_roles_dict_to_json(dictionary: Dict[DnDEventRole, List[str]]) -> Dict[str,List[str]]:
    """
    Transform the dictionary to another form to be able to save it as such.
    """
    transformed_dict = {}
    for key in dictionary.keys():
        transformed_dict[key] = dictionary[key]
    return transformed_dict

def create_cat_dict(Cat, wandering_cats, new_cats = []) -> Dict[str, Any]:
    """Create the dictionary which is used for the pronoun replacement."""
    cat_dict = {}
    if str(game.clan.current_story_id) not in game.clan.stories.keys():
        return cat_dict
    current_story = game.clan.stories[str(game.clan.current_story_id)]
    for role_key, cat_id_list in current_story.roles.items():
        fitting_role = [role.value for role in DnDEventRole if role.value == role_key]
        if fitting_role:
            fitting_role = fitting_role[0]
        for idx in range(len(cat_id_list)):
            cat_id = cat_id_list[idx]
            cat = Cat.fetch_cat(cat_id)
            if cat:
                abbr = fitting_role.replace(" ", "_")
                cat_dict[f"{abbr}:{idx}"] = (str(cat.name), choice(cat.pronouns))
            else:
                print(f"ERROR DnD: cat with the id {cat_id}, could not be found.")
    for idx in range(len(new_cats)):
        cat_dict[f"n_c:{idx}"] = (str(new_cats[idx].name), choice(new_cats[idx].pronouns))
    for index in range(len(wandering_cats)):
        cat = wandering_cats[index]
        cat_dict[f"c:{index}"] = (str(cat.name), choice(cat.pronouns))
    return cat_dict