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
            if linage.value in linage_distribution:
                to_choose.extend([linage] * linage_distribution[linage.value])
        self.linage_type = choice(to_choose)
        self.combined_linages = {}
        self.main_linage = None

    def new_linage(self, parent1 = None, parent2 = None):
        """Make a percentage combination out of the parents."""
        self.combined_linages = {}
        # create default sub linage distribution
        if parent1:
            p1_linage = parent1.dnd_linage
            for sub_linage in p1_linage.combined_linages.keys():
                if parent2:
                    self.combined_linages[sub_linage] = p1_linage.combined_linages[sub_linage] / 2
                else:
                    self.combined_linages[sub_linage] = p1_linage.combined_linages[sub_linage]
        if parent2:
            p2_linage = parent2.dnd_linage
            for sub_linage in p2_linage.combined_linages.keys():
                if parent2:
                    self.combined_linages[sub_linage] = p2_linage.combined_linages[sub_linage] / 2
                else:
                    self.combined_linages[sub_linage] = p2_linage.combined_linages[sub_linage]
        
