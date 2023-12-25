# pylint: disable=line-too-long
"""

TODO: Docs


"""

  # pylint: enable=line-too-long

from scripts.game_structure.game_essentials import game
from scripts.cat.skills import SkillPath


def medical_cats_condition_fulfilled(all_cats,
                                     amount_per_med,
                                     give_clanmembers_covered=False):
    """
    returns True if the player has enough meds for the whole clan

    set give_clanmembers_covered to True to return the int of clanmembers that the meds can treat
    """
    
    fulfilled = False
    
    medical_cats = [i for i in all_cats if not i.dead and not i.outside and not
                                            i.not_working() and i.status in 
                                            ["medicine cat", 
                                             "medicine cat apprentice"]]
    full_med = [i for i in medical_cats if i.status == "medicine cat"]
    apprentices = [i for i in medical_cats if i.status == "medicine cat apprentice"]
    
    total_exp = 0
    for cat in medical_cats:
        total_exp += cat.experience 
    total_exp = total_exp * 0.003
    
    # Determine the total med number. Med cats with certain skill counts 
    # as "more" of a med cat.  Only full medicine cat can have their skills have effect
    total_med_number = len(apprentices) / 2
    for cat in full_med:
        if cat.skills.meets_skill_requirement(SkillPath.HEALER, 3):
            total_med_number += 2
        elif cat.skills.meets_skill_requirement(SkillPath.HEALER, 2):
            total_med_number += 1.75
        elif cat.skills.meets_skill_requirement(SkillPath.HEALER, 2):
            total_med_number += 1.5
        else:
            total_med_number += 1
        
    
    adjust_med_number = total_med_number + total_exp

    can_care_for = int(adjust_med_number * (amount_per_med + 1))

    relevant_cats = list(
        filter(lambda c: not c.dead and not c.outside, all_cats))

    if give_clanmembers_covered is True:
        return can_care_for
    if can_care_for >= len(relevant_cats):
        fulfilled = True
    return fulfilled


def get_amount_cat_for_one_medic(clan):
    """Returns """
    amount = 10
    if clan and clan.game_mode == 'cruel season':
        amount = 7
    return amount


# ---------------------------------------------------------------------------- #
#                                    Illness                                   #
# ---------------------------------------------------------------------------- #


class Illness:
    """
    If a cat gets sick one instance of this class is created and added to the cat.
    """

    def __init__(self,
                 name: str,
                 moon_start: int,
                 severity: str,
                 mortality: int,
                 infectiousness: int,
                 duration: int,
                 medicine_duration: int,
                 medicine_mortality: int,
                 risks: list = None,
                 event_triggered: bool =False):
        self.name = name
        self.severity = severity
        self.mortality = mortality
        self.infectiousness = infectiousness
        self.duration = duration
        self.medicine_duration = medicine_duration
        self.medicine_mortality = medicine_mortality
        self.risks = risks if risks else []
        self.moon_start = moon_start
        self.event_triggered = event_triggered

        self.current_duration = duration
        self.current_mortality = mortality

        #amount_per_med = get_amount_cat_for_one_medic(game.clan)
        #if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(),
        #                                    amount_per_med):
        #    self.current_duration = medicine_duration
        #    self.current_mortality = medicine_mortality

    @property
    def current_duration(self):
        """
        The current duration of this illness with respect if the clan has enough medicine cats.
        """
        return self._current_duration

    @current_duration.setter
    def current_duration(self, value):
        """
        If a the current duration is set, check if the clan has enough medicine cats and the bonus can be applied.
        """
        amount_per_med = get_amount_cat_for_one_medic(game.clan)
        if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(),
                                            amount_per_med):
            if value > self.medicine_duration:
                value = self.medicine_duration

        self._current_duration = value

    @property
    def current_mortality(self):
        """
        The current mortality of this illness with respect if the clan has enough medicine cats.
        """
        return self._current_mortality

    @current_mortality.setter
    def current_mortality(self, value):
        """
        If a the current mortality is set, check if the clan has enough medicine cats and the bonus can be applied.
        """
        amount_per_med = get_amount_cat_for_one_medic(game.clan)
        if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(),
                                            amount_per_med):
            if value < self.medicine_mortality:
                value = self.medicine_mortality

        self._current_mortality = value

    def __getitem__(self, key):
        """Allows you to treat this like a dictionary if you want."""
        return getattr(self, key)

# ---------------------------------------------------------------------------- #
#                                   Injuries                                   #
# ---------------------------------------------------------------------------- #


class Injury:
    """
    If a cat gets hurts one instance of this class is created and added to the cat.
    """

    def __init__(self,
                 name: str,
                 moon_start: int,
                 severity: str,
                 mortality: int,
                 duration: int,
                 medicine_duration: int,
                 complication: (str|None) = None,
                 risks: list = None,
                 illness_infectiousness: list = None,
                 also_got: list = None,
                 cause_permanent: list = None,
                 event_triggered: bool =False):
        self.name = name
        self.moon_start = moon_start
        self.severity = severity
        self.duration = duration
        self.medicine_duration = medicine_duration
        self.mortality = mortality
        self.complication = complication
        self.risks = risks if risks else []
        self.illness_infectiousness = illness_infectiousness if illness_infectiousness else []
        self.also_got = also_got if also_got else []
        self.cause_permanent = cause_permanent if cause_permanent else []
        self.event_triggered = event_triggered

        self.current_duration = duration
        self.current_mortality = mortality

        #amount_per_med = get_amount_cat_for_one_medic(game.clan)
        #if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(),
        #                                    amount_per_med):
        #    self.current_duration = medicine_duration

    @property
    def current_duration(self):
        """
        The current mortality of this illness with respect to the used herbs and medicine cat knowledge.
        """
        return self._current_duration

    @current_duration.setter
    def current_duration(self, value):
        """
        If a the current duration is set, check if the clan has enough medicine cats and the bonus can be applied.
        """
        amount_per_med = get_amount_cat_for_one_medic(game.clan)
        if medical_cats_condition_fulfilled(game.cat_class.all_cats.values(),
                                            amount_per_med):
            if value > self.medicine_duration:
                value = self.medicine_duration

        self._current_duration = value

    @property
    def current_mortality(self):
        """
        If a the current mortality is set, check if the clan has enough medicine cats and the bonus can be applied.
        """
        return self._current_mortality

    @current_mortality.setter
    def current_mortality(self, value):
        """
        If a the current mortality is set, check if the clan has enough medicine cats and the bonus can be applied.
        """
        self._current_mortality = value

    def __getitem__(self, key):
        """Allows you to treat this like a dictionary if you want."""
        return getattr(self, key)

# ---------------------------------------------------------------------------- #
#                             Permanent Conditions                             #
# ---------------------------------------------------------------------------- #


class PermanentCondition:
    """
    If a cat gets a permanent condition one instance of this class is created and added to the cat.
    """

    def __init__(self,
                 name: str,
                 moon_start: int,
                 moons_until: int,
                 severity: str,
                 mortality: int = 0,
                 born_with: bool = False,
                 complication: (str|None) = None,
                 risks: list = None,
                 illness_infectiousness: list = None,
                 event_triggered: bool = False):
        self.name = name
        self.moon_start = moon_start
        self.moons_until = moons_until
        self.severity = severity
        self.mortality = mortality
        self.born_with = born_with
        self.complication = complication
        self.risks = risks if risks else []
        self.illness_infectiousness = illness_infectiousness if illness_infectiousness else []
        self.new = event_triggered

        self.current_mortality = mortality

    # severity level determines retirement:
    # severe - auto retire, major - chance retire, minor - no retire
    # congenital determines if a cat can be born with it or not: never, sometimes, always

    # moons_until is used if you want a delay between when the cat
    # contracts the condition and when the cat presents that condition

    def __getitem__(self, key):
        """Allows you to treat this like a dictionary if you want."""
        return getattr(self, key)
