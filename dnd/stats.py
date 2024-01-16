import random

class Stat:
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

    def __init__(self, str = None, dex = None, con = None, int = None, cha = None):
        if str:
            self.str = str
        else:
            self.str = random.randint(8, 15)
        if dex:
            self.dex = dex
        else:
            self.dex = random.randint(8, 15)
        if con:
            self.con = con
        else:
            self.con = random.randint(8, 15)
        if int:
            self.int = int
        else:
            self.int = random.randint(8, 15)
        if cha:
            self.cha = cha
        else:
            self.cha = random.randint(8, 15)

    def get_stat_dict(self):
        return {
            "str": self.str,
            "dex": self.dex,
            "con": self.con,
            "int": self.int,
            "cha": self.cha
        }

    @property
    def str(self):
        return self._str

    @str.setter
    def str(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._str = value

    def inc_str(self):
        self.str += 1

    @property
    def dex(self):
        return self._dex

    @dex.setter
    def dex(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._dex = value

    def inc_dex(self):
        self.dex += 1

    @property
    def con(self):
        return self._con

    @con.setter
    def con(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._con = value

    def inc_con(self):
        self.con += 1

    @property
    def int(self):
        return self._int

    @int.setter
    def int(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._int = value

    def inc_int(self):
        self.int += 1

    @property
    def cha(self):
        return self._cha

    @cha.setter
    def cha(self, value):
        if value < 8:
            value = 8
        if value > 15:
            value = 15
        self._cha = value

    def inc_cha(self):
        self.cha += 1
