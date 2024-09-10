import re

from random import choice
from enum import Enum
from typing import List, Dict, Any
from random import choice, randint, sample

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

def create_cat_dict(Cat, wandering_cats, new_cats = [], random_cat = None) -> Dict[str, Any]:
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
    if random_cat:
        cat_dict["r_c"] = (str(random_cat.name), choice(random_cat.pronouns))
    return cat_dict

def gather_cat_objects(
        Cat,
        abbr_list: List[str],
        event
) -> list:
    """
    gathers cat objects from list of abbreviations used within an event format block
    :param Cat Cat: Cat class
    :param list[str] abbr_list: The list of abbreviations, supports "m_c", "r_c", "p_l", "s_c", "app1", "app2", "clan",
    "some_clan", "patrol", "multi", "n_c{index}"
    :param event: the controlling class of the event (e.g. Patrol, HandleShortEvents), default None
    passing a full event class, then be aware that you can only include "m_c" as a cat abbreviation in your rel block.
    The other cat abbreviations will not work.
    :return: list of cat objects
    """
    out_set = set()
    print("type: ", abbr_list)

    for abbr in abbr_list:
        print("abbr; ", abbr)
        if ":" in abbr:
            cat_info = abbr.split(":")
            cat_role_location = cat_info[0]
            cat_index = int(cat_info[1])
            cat = None
            if cat_role_location == "n_c":
                cat = event.new_cats[cat_index][0]
            else:
                cat_role_location = cat_role_location.replace("_", " ")
                old_fitting_role = [role for role in DnDEventRole if role.value == cat_role_location]
                if len(old_fitting_role) > 0:
                    story = game.clan.stories[str(game.clan.current_story_id)]
                    if old_fitting_role[0].value in story.roles.keys():
                        cat_id = story.roles[old_fitting_role[0].value][cat_index]
                        cat = Cat.fetch_cat(cat_id)
                    else:
                        print("ERROR: ", story.roles)
            if cat:
                out_set.add(cat)
        elif abbr == "r_c":
            out_set.add(event.random_cat)
        elif abbr == "clan":
            out_set.update([x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)])
        elif abbr == "some_clan":  # 1 / 8 of clan cats are affected
            clan_cats = [x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)]
            out_set.update(sample(clan_cats, randint(1, round(len(clan_cats) / 8))))
        elif abbr == "patrol":
            out_set.update(event.wandering_cats)
        elif abbr == "multi":
            cat_num = randint(1, max(1, len(event.wandering_cats) - 1))
            out_set.update(sample(event.wandering_cats, cat_num))
        elif re.match(r"n_c:[0-9]+", abbr):
            index = re.match(r"n_c:([0-9]+)", abbr).group(1)
            index = int(index)
            if index < len(event.new_cats):
                out_set.update(event.new_cats[index])

    return list(out_set)