from random import choice
from typing import Dict
from scripts.dnd.dnd_types import LinageType

from scripts.game_structure.game_essentials import game


class Linage:
    """Represent a race/linage of a cat."""
    def __init__(self, linage_distribution: Dict[str,int] = None):
        if linage_distribution == None:
            linage_distribution = game.dnd_config["linage_distribution"]

        to_choose = []
        for linage in LinageType:
            to_choose.extend([linage] * linage_distribution[linage.value])
        self.linage_type = choice(to_choose)
