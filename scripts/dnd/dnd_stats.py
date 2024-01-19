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
        15: 2
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
