from enum import Enum
from random import choice

from scripts.game_structure.game_essentials import game

class LinageType(Enum):
    CAT = "cat"
    HIGH_ELF = "high elf"
    DWARF = "dwarf"
    ORC = "orc"

class Linage:
    """Represent a race/linage of a cat."""
    def __init__(self, linage_type: LinageType = None):
        self.linage_type = linage_type
        if self.linage_type == None:
            linage_distribution = game.dnd_config["linage_distribution"]
            to_choose = []
            for linage in LinageType:
                to_choose.extend([linage] * linage_distribution[linage.value])
            self.linage_type = choice(to_choose)
