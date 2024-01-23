import copy
from enum import Enum
import random

from scripts.game_structure.game_essentials import game

class StatType(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

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

    def __init__(self, str = 0, dex = 0, con = 0, int = 0, wis = 0, cha = 0):
        self._stats = {
            StatType.STRENGTH: str,
            StatType.DEXTERITY: dex,
            StatType.CONSTITUTION: con,
            StatType.INTELLIGENCE: int,
            StatType.WISDOM: wis,
            StatType.CHARISMA: cha
        }
        array = copy.deepcopy(game.dnd_config["start_array"])
        if self._stats[StatType.STRENGTH] == 0:
            stat = random.choice(array)
            self._stats[StatType.STRENGTH] = stat
            array.remove(stat)
        if self._stats[StatType.DEXTERITY] == 0:
            stat = random.choice(array)
            self._stats[StatType.DEXTERITY] = stat
            array.remove(stat)
        if self._stats[StatType.CONSTITUTION] == 0:
            stat = random.choice(array)
            self._stats[StatType.CONSTITUTION] = stat
            array.remove(stat)
        if self._stats[StatType.INTELLIGENCE] == 0:
            stat = random.choice(array)
            self._stats[StatType.INTELLIGENCE] = stat
            array.remove(stat)
        if self._stats[StatType.WISDOM] == 0:
            stat = random.choice(array)
            self._stats[StatType.WISDOM] = stat
            array.remove(stat)
        if self._stats[StatType.CHARISMA] == 0:
            stat = random.choice(array)
            self._stats[StatType.CHARISMA] = stat
            array.remove(stat)

    def get_stat_dict(self):
        return {
            "str": self.str,
            "dex": self.dex,
            "con": self.con,
            "int": self.int,
            "wis": self.wis,
            "cha": self.cha
        }

    def inheritance(self, parent1 = None, parent2 = None):
        "Handles the inheritance of stats of parents."
        possible_inheritance = [s_type for s_type in StatType]
        if parent1:
            inh_stats1 = random.choice(possible_inheritance)
            stat1 = parent1.dnd_stats._stats[inh_stats1]
            possible_inheritance.remove(inh_stats1)
            inh_stats2 = random.choice(possible_inheritance)
            stat2 = parent1.dnd_stats._stats[inh_stats2]
            if stat1 > game.dnd_config["max_inheritance"]:
                stat1 = game.dnd_config["max_inheritance"]
            if stat2 > game.dnd_config["max_inheritance"]:
                stat2 = game.dnd_config["max_inheritance"]
            #print(f"INHERITING1: {inh_stats1} - {stat1} - prev: {self._stats[inh_stats1]}")
            #print(f"INHERITING1: {inh_stats2} - {stat2} - prev: {self._stats[inh_stats2]}")
            self._stats[inh_stats1] = stat1
            self._stats[inh_stats2] = stat2
        if parent2:
            inh_stats1 = random.choice(possible_inheritance)
            stat1 = parent1.dnd_stats._stats[inh_stats1]
            possible_inheritance.remove(inh_stats1)
            inh_stats2 = random.choice(possible_inheritance)
            stat2 = parent1.dnd_stats._stats[inh_stats2]
            if stat1 > game.dnd_config["max_inheritance"]:
                stat1 = game.dnd_config["max_inheritance"]
            if stat2 > game.dnd_config["max_inheritance"]:
                stat2 = game.dnd_config["max_inheritance"]
            #print(f"INHERITING2: {inh_stats1} - {stat1} - prev: {self._stats[inh_stats1]}")
            #print(f"INHERITING2: {inh_stats2} - {stat2} - prev: {self._stats[inh_stats2]}")
            self._stats[inh_stats1] = stat1
            self._stats[inh_stats2] = stat2

    @property
    def str(self):
        return self._stats[StatType.STRENGTH]

    @str.setter
    def str(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.STRENGTH] = value

    def inc_str(self):
        self.str += 1

    @property
    def dex(self):
        return self._stats[StatType.DEXTERITY]

    @dex.setter
    def dex(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.DEXTERITY] = value

    def inc_dex(self):
        self.dex += 1

    @property
    def con(self):
        return self._stats[StatType.CONSTITUTION]

    @con.setter
    def con(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.CONSTITUTION] = value

    def inc_con(self):
        self.con += 1

    @property
    def int(self):
        return self._stats[StatType.INTELLIGENCE]

    @int.setter
    def int(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.INTELLIGENCE] = value

    def inc_int(self):
        self.int += 1

    @property
    def wis(self):
        return self._stats[StatType.WISDOM]

    @wis.setter
    def wis(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.WISDOM] = value

    def inc_wis(self):
        self.wis += 1

    @property
    def cha(self):
        return self._stats[StatType.CHARISMA]

    @cha.setter
    def cha(self, value):
        if value < game.dnd_config["min_stat"]:
            value = game.dnd_config["min_stat"]
        if value > game.dnd_config["max_stat"]:
            value = game.dnd_config["max_stat"]
        self._stats[StatType.CHARISMA] = value

    def inc_cha(self):
        self.cha += 1
