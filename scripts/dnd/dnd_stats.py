import copy
import random

from scripts.dnd.dnd_types import StatType, LinageType
from scripts.game_structure.game_essentials import game

class Stats:
    """Represents the dnd stats for one cat."""
    modifier = {
        8: -1,
        9: -1,
        10: 0,
        11: 0,
        12: 1,
        13: 1,
        14: 2,
        15: 2,
        16: 3,
        17: 3,
        18: 3,
        19: 4,
        20: 4,
        21: 4,
        22: 5,
        23: 5,
        24: 5,
        25: 6,
    }

    linage_proficiency = {
        LinageType.CAT : [StatType.CHARISMA],
        LinageType.ELF : [StatType.INTELLIGENCE],
        LinageType.DWARF : [StatType.WISDOM],
        LinageType.ORC : [StatType.STRENGTH, StatType.CONSTITUTION]
    }

    def __init__(self, str = 0, dex = 0, con = 0, int = 0, wis = 0, cha = 0):
        self.genetic_stats = {
            StatType.STRENGTH: str,
            StatType.DEXTERITY: dex,
            StatType.CONSTITUTION: con,
            StatType.INTELLIGENCE: int,
            StatType.WISDOM: wis,
            StatType.CHARISMA: cha
        }
        # stats are used for all checks, those are get the linage buffs added
        self.stats = {
            StatType.STRENGTH: str,
            StatType.DEXTERITY: dex,
            StatType.CONSTITUTION: con,
            StatType.INTELLIGENCE: int,
            StatType.WISDOM: wis,
            StatType.CHARISMA: cha
        }
        self.linage = None
        self.init_array()

    def init_array(self):
        "Handles the initialization with the array method"
        array = copy.deepcopy(game.dnd_config["start_array"])
        if self.genetic_stats[StatType.STRENGTH] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.STRENGTH] = stat
            array.remove(stat)
        if self.genetic_stats[StatType.DEXTERITY] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.DEXTERITY] = stat
            array.remove(stat)
        if self.genetic_stats[StatType.CONSTITUTION] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.CONSTITUTION] = stat
            array.remove(stat)
        if self.genetic_stats[StatType.INTELLIGENCE] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.INTELLIGENCE] = stat
            array.remove(stat)
        if self.genetic_stats[StatType.WISDOM] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.WISDOM] = stat
            array.remove(stat)
        if self.genetic_stats[StatType.CHARISMA] == 0:
            stat = random.choice(array)
            self.genetic_stats[StatType.CHARISMA] = stat
            array.remove(stat)

    def update_stats(self, linage = None):
        "Adding the linage buffs to the stats which are used to get outcome and stuff"
        if linage:
            self.linage = linage
        for stat_type in self.stats.keys():
            linage_buff = 1 if stat_type in self.linage_proficiency[self.linage] else 0
            self.stats[stat_type] = self.genetic_stats[stat_type] + linage_buff

    def get_stat_dict(self):
        "Returns the genetic stats for save purpose."
        return {
            "str": self.genetic_stats[StatType.STRENGTH],
            "dex": self.genetic_stats[StatType.DEXTERITY],
            "con": self.genetic_stats[StatType.CONSTITUTION],
            "int": self.genetic_stats[StatType.INTELLIGENCE],
            "wis": self.genetic_stats[StatType.WISDOM],
            "cha": self.genetic_stats[StatType.CHARISMA]
        }

    def get_display_text(self, linage_bold = False):
        "Returns a html string which describe the stats"
        return_text = ""
        strength = self.stats[StatType.STRENGTH ]
        mod_str = "+" if self.modifier[strength] >= 0 else ""
        if StatType.STRENGTH in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>strength: " + str(strength) + " (" + mod_str + str(self.modifier[strength]) + ")</b><br>"
        else:
            return_text += "strength: " + str(strength) + " (" + mod_str + str(self.modifier[strength]) + ")<br>"
        dexterity = self.stats[StatType.DEXTERITY]
        mod_str = "+" if self.modifier[dexterity] >= 0 else ""
        if StatType.DEXTERITY in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>dexterity: " + str(dexterity) + " (" + mod_str + str(self.modifier[dexterity]) + ")</b><br>"
        else:
            return_text += "dexterity: " + str(dexterity) + " (" + mod_str + str(self.modifier[dexterity]) + ")<br>"
        constitution = self.stats[StatType.CONSTITUTION]
        mod_str = "+" if self.modifier[constitution] >= 0 else ""
        if StatType.CONSTITUTION in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>constitution: " + str(constitution) + " (" + mod_str + str(self.modifier[constitution]) + ")</b><br>"
        else:
            return_text += "constitution: " + str(constitution) + " (" + mod_str + str(self.modifier[constitution]) + ")<br>"
        intelligence = self.stats[StatType.INTELLIGENCE]
        mod_str = "+" if self.modifier[intelligence] >= 0 else ""
        if StatType.INTELLIGENCE in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>intelligence: " + str(intelligence) + " (" + mod_str + str(self.modifier[intelligence]) + ")</b><br>"
        else:
            return_text += "intelligence: " + str(intelligence) + " (" + mod_str + str(self.modifier[intelligence]) + ")<br>"
        wisdom = self.stats[StatType.WISDOM]
        mod_str = "+" if self.modifier[wisdom] >= 0 else ""
        if StatType.WISDOM in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>wisdom: " + str(wisdom) + " (" + mod_str + str(self.modifier[wisdom]) + ")</b><br>"
        else:
            return_text += "wisdom: " + str(wisdom) + " (" + mod_str + str(self.modifier[wisdom]) + ")<br>"
        charisma = self.stats[StatType.CHARISMA]
        mod_str = "+" if self.modifier[charisma] >= 0 else ""
        if StatType.CHARISMA in self.linage_proficiency[self.linage] and linage_bold:
            return_text += "<b>charisma: " + str(charisma) + " (" + mod_str + str(self.modifier[charisma]) + ")</b><br>"
        else:
            return_text += "charisma: " + str(charisma) + " (" + mod_str + str(self.modifier[charisma]) + ")<br>"
        return return_text

    def inheritance(self, parent1 = None, parent2 = None):
        "Handles the inheritance of stats of parents."
        possible_inheritance = [s_type for s_type in StatType]
        if parent1:
            inh_stats1 = random.choice(possible_inheritance)
            stat1 = parent1.dnd_stats.genetic_stats[inh_stats1]
            possible_inheritance.remove(inh_stats1)
            inh_stats2 = random.choice(possible_inheritance)
            stat2 = parent1.dnd_stats.genetic_stats[inh_stats2]
            if stat1 > game.dnd_config["max_inheritance"]:
                stat1 = game.dnd_config["max_inheritance"]
            if stat2 > game.dnd_config["max_inheritance"]:
                stat2 = game.dnd_config["max_inheritance"]
            #print(f"INHERITING1: {inh_stats1} - {stat1} - prev: {self.genetic_stats[inh_stats1]}")
            #print(f"INHERITING1: {inh_stats2} - {stat2} - prev: {self.genetic_stats[inh_stats2]}")
            self.genetic_stats[inh_stats1] = stat1
            self.genetic_stats[inh_stats2] = stat2
        if parent2:
            inh_stats1 = random.choice(possible_inheritance)
            stat1 = parent1.dnd_stats.genetic_stats[inh_stats1]
            possible_inheritance.remove(inh_stats1)
            inh_stats2 = random.choice(possible_inheritance)
            stat2 = parent1.dnd_stats.genetic_stats[inh_stats2]
            if stat1 > game.dnd_config["max_inheritance"]:
                stat1 = game.dnd_config["max_inheritance"]
            if stat2 > game.dnd_config["max_inheritance"]:
                stat2 = game.dnd_config["max_inheritance"]
            #print(f"INHERITING2: {inh_stats1} - {stat1} - prev: {self.genetic_stats[inh_stats1]}")
            #print(f"INHERITING2: {inh_stats2} - {stat2} - prev: {self.genetic_stats[inh_stats2]}")
            self.genetic_stats[inh_stats1] = stat1
            self.genetic_stats[inh_stats2] = stat2
