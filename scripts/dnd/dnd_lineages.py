from random import choice
from typing import Dict
from scripts.dnd.dnd_types import LinageType

from scripts.game_structure import constants


class Lineage:
    """Represent a race/lineage of a cat."""
    def __init__(self, lineage_distribution: Dict[str,int] = None):
        if lineage_distribution == None:
            lineage_distribution = constants.DND_CONFIG["lineage_distribution"]

        to_choose = []
        for lineage in LinageType:
            if lineage.value in lineage_distribution:
                to_choose.extend([lineage] * lineage_distribution[lineage.value])
        self.lineage_type = choice(to_choose)
