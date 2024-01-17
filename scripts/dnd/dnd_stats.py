from enum import Enum
import random

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

    def __init__(self, str = None, dex = None, con = None, int = None, wis = None, cha = None):
        self._stats = {
            StatType.STRENGTH: str if str else random.randint(8,15),
            StatType.DEXTERITY: dex if dex else random.randint(8,15),
            StatType.CONSTITUTION: con if con else random.randint(8,15),
            StatType.INTELLIGENCE: int if int else random.randint(8,15),
            StatType.WISDOM: wis if wis else random.randint(8,15),
            StatType.CHARISMA: cha if cha else random.randint(8,15)
        }

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
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.STRENGTH] = value

    def inc_str(self):
        self.str += 1

    @property
    def dex(self):
        return self._stats[StatType.DEXTERITY]

    @dex.setter
    def dex(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.DEXTERITY] = value

    def inc_dex(self):
        self.dex += 1

    @property
    def con(self):
        return self._stats[StatType.CONSTITUTION]

    @con.setter
    def con(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.CONSTITUTION] = value

    def inc_con(self):
        self.con += 1

    @property
    def int(self):
        return self._stats[StatType.INTELLIGENCE]

    @int.setter
    def int(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.INTELLIGENCE] = value

    def inc_int(self):
        self.int += 1

    @property
    def wis(self):
        return self._stats[StatType.WISDOM]

    @wis.setter
    def wis(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.WISDOM] = value

    def inc_wis(self):
        self.wis += 1

    @property
    def cha(self):
        return self._stats[StatType.CHARISMA]

    @cha.setter
    def cha(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._stats[StatType.CHARISMA] = value

    def inc_cha(self):
        self.cha += 1
