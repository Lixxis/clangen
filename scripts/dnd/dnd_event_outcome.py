#!/usr/bin/env python3
# -*- coding: ascii -*-
import re
import pygame
import ujson
import random
from random import choice, randint, choices, sample
from typing import List, Dict, Union, Optional, TYPE_CHECKING
from os.path import exists as path_exists

if TYPE_CHECKING:
    from scripts.dnd.dnd_event import DnDEvent
    from scripts.patrol.patrol import Patrol

from scripts.cat.history import History
from scripts.utility import (
    change_clan_relations,
    change_clan_reputation,
    change_relationship_values,
    create_new_cat
)
from scripts.dnd.dnd_types import gather_cat_objects
from scripts.game_structure.game_essentials import game
from scripts.cat.skills import SkillPath
from scripts.cat.cats import Cat, ILLNESSES, INJURIES, PERMANENT, BACKSTORIES
from scripts.cat.pelts import Pelt
from scripts.cat.names import Name
from scripts.cat_relations.relationship import Relationship
from scripts.clan_resources.freshkill import ADDITIONAL_PREY, PREY_REQUIREMENT, HUNTER_EXP_BONUS, HUNTER_BONUS, \
    FRESHKILL_ACTIVE

HERBS = None
with open("resources/dicts/herbs.json", "r", encoding="utf-8") as read_file:
    HERBS = ujson.loads(read_file.read())

class DnDEventOutcome:
    def __init__(
            self,
            text: List[str]  = None,
            exp: List[int] = None, 
            dead_cats: List[str] = None,
            lost_cats: List[str] = None,
            injury: List[Dict] = None,
            history_reg_death: str = None,
            history_leader_death: str = None,
            history_scar: str = None,
            new_cat: List[List[str]] = None,
            herbs: List[str] = None,
            prey: List[str] = None,
            outsider_rep: Union[int, None] = None,
            other_clan_rep: Union[int, None] = None,
            relationship_effects: List[dict] = None,
            relationship_constraints: List[str] = None,
            outcome_art: Union[str, None] = None,
            outcome_art_clean: Union[str, None] = None,
            next_id: Optional[str] = None,
            roles: Optional[Dict] = None,
            joining_cats: Optional[list] = None,
        ) -> None:
        self.text = text if text is not None else []
        self.exp = exp if exp is not None else game.dnd_config["default_exp_factors_success"]
        self.dead_cats = dead_cats if dead_cats is not None else []
        self.lost_cats = lost_cats if lost_cats is not None else []
        self.injury = injury if injury is not None else []
        self.history_reg_death = history_reg_death if history_reg_death is not None else \
                                 "died on an adventure."
        self.history_leader_death = history_leader_death if history_leader_death is not None else \
                                    "died on an adventure."
        self.history_scar = history_scar if history_scar is not None else "was scarred on an adventure."
        self.new_cat = new_cat if new_cat is not None else []
        self.herbs = herbs if herbs is not None else []
        self.prey = prey if prey is not None else []
        self.outsider_rep = outsider_rep
        self.other_clan_rep = other_clan_rep
        self.relationship_effects = relationship_effects if relationship_effects is not None else []
        self.relationship_constraints = relationship_constraints if relationship_constraints is not None else []
        self.outcome_art = outcome_art
        self.outcome_art_clean = outcome_art_clean
        self.next_id = next_id
        self.roles = roles
        self.joining_cats = joining_cats if joining_cats is not None else []

    def execute_outcome(self, event: "DnDEvent", pass_number: int, was_success: bool) -> None:
        """ 
        Excutes the outcome. Returns a tuple with the final outcome text, the results text, and any outcome art
        format: (Outcome text, results text, outcome art (might be None))
        """
        results = []
        # This must be done before text processing so that the new cat's pronouns are generated first
        results.append(self._handle_new_cats(event))
        
        # This order is important. 
        results.append(self._handle_death(event))
        results.append(self._handle_lost(event))
        results.append(self._handle_condition_and_scars(event))
        results.append(self._handle_relationship_changes(event))
        results.append(self._handle_rep_changes(event))
        results.append(self._handle_other_clan_relations(event))
        results.append(self._handle_prey(event))
        results.append(self._handle_herbs(event))
        results.append(self._handle_exp(event, pass_number, was_success))
        results.append(self._handle_mentor_app(event))
        results.append(self._handle_joining_cats(event))
        
        # Filter out empty results strings
        results = [x for x in results if x]
        
        print("PATROL END -----------------------------------------------------")
        
        return results

    def get_outcome_art(self):
        """Return outcome art, if not None. Return's None if there is no outcome art, or if outcome art can't be found.  """
        root_dir = "resources/images/patrol_art/dnd/"
        
        if game.settings.get("gore") and self.outcome_art_clean:
            file_name = self.outcome_art_clean
        else:
            file_name = self.outcome_art

        if not isinstance(file_name, str) or not path_exists(f"{root_dir}{file_name}.png"):
            return None
            
        return pygame.image.load(f"{root_dir}{file_name}.png")

    def _handle_exp(self, event:'DnDEvent', pass_number: int, was_success: bool) -> str:
        """Handle giving exp """
        
        if game.clan.game_mode == 'classic':
            gm_modifier = 1
        elif game.clan.game_mode == 'expanded':
            gm_modifier = 0.75
        elif game.clan.game_mode == 'cruel season':
            gm_modifier = 0.5
        else:
            gm_modifier = 1

        if "master" in [x.experience_level for x in event.wandering_cats]:
            max_boost = 10
        else:
            max_boost = 0

        if self.exp == game.dnd_config["default_exp_factors_success"]:
            if was_success:
                self.exp = [round(pass_number * factor) for factor in game.dnd_config["default_exp_factors_success"]]
            else:
                self.exp = [round(pass_number * factor) for factor in game.dnd_config["default_exp_factors_fail"]]

        print("possible exp: ", self.exp)
        patrol_exp = self.exp[len(event.wandering_cats)-1]
        gained_exp = (patrol_exp + max_boost) * gm_modifier
        app_exp = round(gained_exp * game.dnd_config["app_exp_debuff"])
        print("gained_exp, warrior: ", gained_exp, " app: ", app_exp)

        for cat in event.wandering_cats:
            if cat.status in ["apprentice", "medicine cat apprentice"]:
                cat.experience = cat.experience + app_exp
            else:
                cat.experience = cat.experience + gained_exp
        return ""

    def _handle_death(self, event:'DnDEvent') -> str:
        """Handle killing cats """
        
        if not self.dead_cats:
            return ""
        
        #body_tags = ("body", "no_body")
        #leader_lives = ("all_lives", "some_lives")
        
        cats_to_kill = gather_cat_objects(Cat, self.dead_cats, event)
        if not cats_to_kill:
            print(f"Something was indicated in dead_cats, but no cats were indicated: {self.dead_cats}")
            return ""
        
        body = True
        if "no_body" in self.dead_cats:
            body=False
        
        results = []
        for _cat in cats_to_kill:
            if _cat.status == "leader":
                if "all_lives" in self.dead_cats:
                    game.clan.leader_lives = 0
                    results.append(f"{_cat.name} lost all of their lives.")
                elif "some_lives" in self.dead_cats:
                    lives_lost = random.randint(1, max(1, game.clan.leader_lives - 1))
                    game.clan.leader_lives -= lives_lost
                    if lives_lost == 1:
                        results.append(f"{_cat.name} lost one life.")
                    else:
                        results.append(f"{_cat.name} lost {lives_lost} lives.")
                else:
                    game.clan.leader_lives -= 1
                    results.append(f"{_cat.name} lost one life.")
            else:
                results.append(f"{_cat.name} died.")
            
            
            # Kill Cat
            self.__handle_death_history(_cat, event)
            _cat.die(body)
            
        return " ".join(results)

    def _handle_lost(self, event:'DnDEvent') -> str:
        """ Handle losing cats """
        
        if not self.lost_cats:
            return ""
        
        cats_to_lose = gather_cat_objects(Cat, self.lost_cats, event)
        if not cats_to_lose:
            print(f"Something was indicated in lost_cats, but no cats were indicated: {self.lost_cats}")
            return ""
        
        
        results = []
        for _cat in cats_to_lose:
            results.append(f"{_cat.name} has been lost.")
            _cat.gone()
            #_cat.greif(body=False)
            
        return " ".join(results)
    
    def _handle_condition_and_scars(self, event:'DnDEvent') -> str:
        """ Handle injuring cats, or giving scars """
        
        if not self.injury:
            return ""
        
        results = []
        condition_lists = {
            "battle_injury": ["claw-wound", "mangled leg", "mangled tail", "torn pelt", "cat bite"],
            "minor_injury": ["sprain", "sore", "bruises", "scrapes"],
            "blunt_force_injury": ["broken bone", "broken back", "head damage", "broken jaw"],
            "hot_injury": ["heat exhaustion", "heat stroke", "dehydrated"],
            "cold_injury": ["shivering", "frostbite"],
            "big_bite_injury": ["bite-wound", "broken bone", "torn pelt", "mangled leg", "mangled tail"],
            "small_bite_injury": ["bite-wound", "torn ear", "torn pelt", "scrapes"],
            "beak_bite": ["beak bite", "torn ear", "scrapes"],
            "rat_bite": ["rat bite", "torn ear", "torn pelt"],
            "sickness": ["greencough", "redcough", "whitecough", "yellowcough"]
        }
        
        for block in self.injury:
            cats = gather_cat_objects(Cat, block.get("cats", ()), event)
            injury = block.get("injuries", ())
            scars = block.get("scars", ())
            
            if not (cats and injury):
                print(f"something is wrong with injury - {block}")
                continue
            
            possible_injuries = []
            for _tag in injury:
                if _tag in condition_lists:
                    possible_injuries.extend(condition_lists[_tag])
                elif _tag in INJURIES or _tag in ILLNESSES or _tag in PERMANENT:
                    possible_injuries.append(_tag)
            
            lethal = True
            if "non_lethal" in injury:
                lethal = False
            
            # Injury or scar the cats
            results = []
            for _cat in cats:
                if game.clan and game.clan.game_mode == "classic":
                    if self.__handle_scarring(_cat, scars, event):
                        results.append(f"{_cat.name} was scarred.")
                    continue
                
                # Non-classic, give condition
                if not possible_injuries:
                    continue
                
                old_injuries = list(_cat.injuries.keys())
                old_illnesses = list(_cat.illnesses.keys())
                old_perm_cond = list(_cat.permanent_condition.keys())
                give_injury = choice(possible_injuries)
                if give_injury in INJURIES:
                    _cat.get_injured(give_injury, lethal=lethal)
                elif give_injury in ILLNESSES:
                    _cat.get_ill(give_injury, lethal=lethal)
                elif give_injury in PERMANENT:
                    _cat.get_permanent_condition(give_injury)
                else:
                    print("WARNING: No Conditions to Give")
                    continue
                
                given_conditions = []
                given_conditions.extend([x for x in _cat.injuries.keys() if x not in old_injuries])
                given_conditions.extend([x for x in _cat.illnesses.keys() if x not in old_illnesses])
                given_conditions.extend([x for x in _cat.permanent_condition.keys() if x not in old_perm_cond])
                # History is also ties to "no_results"  
                if not block.get("no_results"):
                    for given_condition in given_conditions:
                        self.__handle_condition_history(_cat, given_condition, event)
                    combined_conditions = ", ".join(given_conditions)
                    results.append(f"{_cat.name} got: {combined_conditions}.")
                else:
                    # If no results are shown, assume the cat didn't get the patrol history. Default override. 
                    self.__handle_condition_history(_cat, give_injury, event, default_overide=True)
                    
                
        return " ".join(results)
    
    def _handle_relationship_changes(self, event:'DnDEvent') -> str:
        """ Handle any needed changes in relationship """
        
        possible_values = ("romantic", "platonic", "dislike", "comfort", "jealous", "trust", "respect")
                    
        for block in self.relationship_effects:
            cats_from = block.get("cats_from", ())
            cats_to = block.get("cats_to", ())
            amount = block.get("amount")
            values = [x for x in block.get("values", ()) if x in possible_values]
            
            # Gather actual cat objects:
            cats_from_ob = gather_cat_objects(Cat, cats_from, event)
            cats_to_ob = gather_cat_objects(Cat, cats_to, event)
            
            # Remove any "None" that might have snuck in
            if None in cats_from_ob:
                cats_from_ob.remove(None)
            if None in cats_to_ob:
                cats_to_ob.remove(None)
            
            # Check to see if value block
            if not (cats_to_ob and cats_from_ob and values and isinstance(amount, int)):
                print(f"Relationship block incorrectly formatted: {block}")
                continue
            
            # Hate this, but I don't want to re-write change_relationship_values
            romantic_love = 0
            platonic_like = 0
            dislike = 0
            comfortable = 0
            jealousy = 0
            admiration = 0
            trust = 0
            if "romantic" in values:
                romantic_love = amount
            if "platonic" in values:
                platonic_like = amount
            if "dislike" in values:
                dislike = amount
            if "comfort" in values:
                comfortable = amount
            if "jealous" in values:
                jealousy = amount
            if "trust" in values:
                trust = amount
            if "respect" in values:
                admiration = amount
            
            # Get log
            log1 = None
            log2 = None
            if block.get("log"):
                log = block.get("log")    
                if isinstance(log, str):
                    log1 = log
                elif isinstance(log, list):
                    if len(log) >= 2:
                        log1 = log[0]
                        log2 = log[1]
                    elif len(log) == 1:
                        log1 = log[0]
                else:
                    print(f"something is wrong with relationship log: {log}")
            
            
            change_relationship_values(
                cats_from_ob,
                cats_to_ob,
                romantic_love,
                platonic_like,
                dislike,
                admiration,
                comfortable,
                jealousy,
                trust,
                log = log1
            )
            
            if block.get("mutual"):
                change_relationship_values(
                    cats_to_ob,
                    cats_from_ob,
                    romantic_love,
                    platonic_like,
                    dislike,
                    admiration,
                    comfortable,
                    jealousy,
                    trust,
                    log = log2
                )
            
        return ""
            
    def _handle_rep_changes(self, event:'DnDEvent') -> str:
        """ Handles any changes in outsider rep"""

        if not isinstance(self.outsider_rep, int):
            return ""
        
        change_clan_reputation(self.outsider_rep * 10)
        if self.outsider_rep > 0:
            insert = "improved"
        elif self.outsider_rep == 0:
            insert = "remained neutral"
        else:
            insert = "worsened"
            
        return f"Your Clan's reputation towards Outsiders has {insert}."
    
    def _handle_other_clan_relations(self, event:'DnDEvent') -> str:
        """ Handles relations changes with other clans"""
        
        if not isinstance(self.other_clan_rep, int) or event.other_clan \
                is None:
            return ""
        
        change_clan_relations(event.other_clan, self.other_clan_rep)
        if self.other_clan_rep > 0:
            insert = "improved"
        elif self.other_clan_rep == 0:
            insert = "remained neutral"
        else:
            insert = "worsened"
            
        return f"Relations with {event.other_clan} have {insert}."
    
    def _handle_herbs(self, event:'DnDEvent') -> str:
        """ Handle giving herbs """
        
        if not self.herbs or game.clan.game_mode == "classic":
            return ""
        
        large_bonus = False
        if "many_herbs" in self.herbs:
            large_bonus = True
        
        # Determine which herbs get picked
        specfic_herbs = [x for x in self.herbs if x in HERBS]
        if "random_herbs" in self.herbs:
            specfic_herbs += random.sample(HERBS, k=choices([1, 2, 3], [6, 5, 1], k=1)[0])
            
        # Remove duplicates
        specfic_herbs = list(set(specfic_herbs))
        
        if not specfic_herbs:
            print(f"{self.herbs} - gave no herbs to give")
            return ""
        
        patrol_size_modifier = int(len(event.wandering_cats) * .5)
        for _herb in specfic_herbs:
            if large_bonus:
                amount_gotten = 4
            else:
                amount_gotten = choices([1, 2, 3], [2, 3, 1], k=1)[0]

            amount_gotten = int(amount_gotten * patrol_size_modifier)
            amount_gotten = max(1, amount_gotten)
            
            if _herb in game.clan.herbs:
                game.clan.herbs[_herb] += amount_gotten
            else:
                game.clan.herbs[_herb] = amount_gotten

        plural_herbs_list = ['cobwebs', 'oak leaves']
        
        if len(specfic_herbs) == 1 and specfic_herbs[0] not in plural_herbs_list:
            insert = f"{specfic_herbs[0]} was"
        elif len(specfic_herbs) == 1 and specfic_herbs[0] in plural_herbs_list:
            insert = f"{specfic_herbs[0]} were"
        elif len(specfic_herbs) == 2:
            if str(specfic_herbs[0]) == str(specfic_herbs[1]):
                insert = f"{specfic_herbs[0]} was"
            else:
                insert = f"{specfic_herbs[0]} and {specfic_herbs[1]} were"
        else:
            insert = f"{', '.join(specfic_herbs[:-1])}, and {specfic_herbs[-1]} were"

        insert = re.sub("[_]", " ", insert)
        
        game.herb_events_list.append(f"{insert.capitalize()} gathered on a patrol.")
        return f"{insert.capitalize()} gathered."
        
    def _handle_prey(self, event:'DnDEvent') -> str:
        """ Handle giving prey """
        
        if not FRESHKILL_ACTIVE:
            return ""
        
        if not self.prey or game.clan.game_mode == "classic":
            return ""

        basic_amount = PREY_REQUIREMENT["warrior"]
        if game.clan.game_mode == 'expanded':
            basic_amount += ADDITIONAL_PREY
        prey_types = {
            "very_small": basic_amount / 2,
            "small": basic_amount,
            "medium": basic_amount * 1.8,
            "large": basic_amount * 2.4,
            "huge": basic_amount * 3.2
        }
        
        used_tag = None
        for tag in self.prey:
            basic_amount = prey_types.get(tag)
            if basic_amount is not None:
                used_tag = tag
                break
        else:
            print(f"{self.prey} - no prey amount tags in prey property")
            return ""
        
        total_amount = 0
        highest_hunter_tier = 0
        for cat in event.wandering_cats:
            total_amount += basic_amount
            if cat.skills.primary.path == SkillPath.HUNTER and cat.skills.primary.tier > 0: 
                level = cat.experience_level
                tier = cat.skills.primary.tier
                if tier > highest_hunter_tier:
                    highest_hunter_tier = tier
                total_amount += int(HUNTER_EXP_BONUS[level] * (HUNTER_BONUS[str(tier)] / 10 + 1))
            elif cat.skills.secondary and cat.skills.secondary.path == SkillPath.HUNTER and cat.skills.secondary.tier > 0:
                level = cat.experience_level
                tier = cat.skills.secondary.tier
                if tier > highest_hunter_tier:
                    highest_hunter_tier = tier
                total_amount += int(HUNTER_EXP_BONUS[level] * (HUNTER_BONUS[str(tier)] / 10 + 1))
        
        # additional hunter buff for expanded mode
        if game.clan.game_mode == "expanded" and highest_hunter_tier:
            total_amount = int(total_amount * (HUNTER_BONUS[str(highest_hunter_tier)] / 20 + 1))

        results = ""
        if total_amount > 0:
            amount_text = used_tag
            if "_" in amount_text:
                amount_text = amount_text.replace("_", " ")

            total_amount = round(total_amount, 2)
            print(f"PREY ADDED: {total_amount}")
            game.freshkill_event_list.append(f"{total_amount} pieces of prey were caught on a patrol.")
            game.clan.freshkill_pile.add_freshkill(total_amount)
            results = f"A {amount_text} amount of prey is brought to camp."
            
        return results

    def _handle_new_cats(self, event:'DnDEvent') -> str:
        """ Handles creating a new cat. Add any new cats to patrol.new_cats """
        
        if not self.new_cat:
            return ""
        
        results = []
        for i, attribute_list in enumerate(self.new_cat):
            
            event.new_cats.append(self.__create_new_cat_block(i, attribute_list,  
                                                               event)) 
            
            for cat in event.new_cats[-1]:
                if cat.dead:
                    results.append(f"{cat.name}'s ghost now wanders.")
                elif cat.outside:
                    results.append(f"The patrol met {cat.name}.")
                else:
                    results.append(f"{cat.name} joined the Clan.")
            
        # Check to see if any young litters joined with alive parents.
        # If so, see if recovering from birth condition is needed
        # and give the condition
        for sub in event.new_cats:
            if sub[0].moons < 3:
                # Search for parent
                for sub_sub in event.new_cats:
                    if sub_sub[0] != sub[0] and (sub_sub[0].gender == "female" or game.clan.clan_settings['same sex birth']) \
                            and sub_sub[0].ID in (sub[0].parent1, sub[0].parent2) and not (sub_sub[0].dead or sub_sub[0].outside):
                        sub_sub[0].get_injured("recovering from birth")
                        break # Break - only one parent ever gives birth
                
                
        return " ".join(results)

    def _handle_joining_cats(self, event:'DnDEvent') -> str:
        """Handles that cats are joining the clan."""
        results = []
        if self.joining_cats:
            cats_to_join = gather_cat_objects(
                Cat,
                abbr_list = self.joining_cats,
                event=event
            )
            for invited_cat in cats_to_join:
                invited_cat.outside = False
                if invited_cat.status.lower() in [
                        "kittypet",
                        "loner",
                        "rogue",
                        "former clancat",
                        "exiled",
                    ]:
                    if "guided" in invited_cat.backstory and invited_cat.status != "exiled":
                        invited_cat.backstory = "outsider1"
                    if invited_cat.backstory in BACKSTORIES["backstory_categories"]["healer_backstories"]:
                        invited_cat.status = "medicine cat"
                    elif invited_cat.age in ["newborn", "kitten"]:
                        invited_cat.status = invited_cat.age
                        if not invited_cat.name.suffix:
                            invited_cat.name = Name(
                                invited_cat.status,
                                invited_cat.name.prefix,
                                invited_cat.name.suffix,
                                invited_cat.pelt.colour,
                                invited_cat.pelt.name,
                                invited_cat.pelt.tortiepattern,
                                game.clan.biome,
                            )
                            invited_cat.name.give_suffix(
                                pelt=None,
                                biome=game.clan.biome,
                                tortiepattern=None,
                            )
                            invited_cat.specsuffix_hidden = False

                    elif invited_cat.age == "senior":
                        invited_cat.status = "elder"
                    elif invited_cat.age == "adolescent":
                        invited_cat.status = "apprentice"
                        invited_cat.update_mentor()
                    else:
                        invited_cat.status = "warrior"
                results.append(f"{invited_cat.name} joined the Clan.")
        return " ".join(results)

    def __create_new_cat_block(self, i:int, attribute_list: List[str], event:'DnDEvent') -> List[Cat]: 
        """Creates a single new_cat block """
        
        thought = choice(["Is looking around the camp with wonder", "Is getting used to their new home"])
        
        # GATHER BIO PARENTS
        parent1 = None
        parent2 = None
        for tag in attribute_list:
            match = re.match(r"parent:([,0-9]+)", tag)
            if not match:
                continue
            
            parent_indexes = match.group(1).split(",")
            if not parent_indexes:
                continue
            
            parent_indexes = [int(index) for index in parent_indexes]
            for index in parent_indexes:
                if index >= i:
                    continue
                
                if parent1 is None:
                    parent1 = event.new_cats[index][0]
                else:
                    parent2 = event.new_cats[index][0]
            break
        
        # GATHER MATES
        in_wandering_cats = {
            "p_l": event.patrol_leader,
            "r_c": event.patrol_random_cat,
        }
        if self.stat_cat:
            in_wandering_cats["s_c"] = self.stat_cat
        give_mates = []
        for tag in attribute_list:
            match = re.match(r"mate:([_,0-9a-zA-Z]+)", tag)
            if not match:
                continue
            
            mate_indexes = match.group(1).split(",")
            
            # TODO: make this less ugly
            for index in mate_indexes:
                if index in in_wandering_cats:
                    if in_wandering_cats[index] in ("apprentice", "medicine cat apprentice"):
                        print("Can't give apprentices mates")
                        continue
                    
                    give_mates.append(in_wandering_cats[index])
                        
                try:
                    index = int(index)
                except ValueError:
                    print(f"mate-index not correct: {index}")
                    continue
                
                if index >= i:
                    continue
                
                give_mates.extend(event.new_cats[index])
        
        give_romance = []
        for tag in attribute_list:
            match = re.match(r"romance:([_,0-9a-zA-Z]+)", tag)
            if not match:
                continue
            
            romance_indexes = match.group(1).split(",")
            
            # TODO: make this less ugly
            for index in romance_indexes:
                if index in in_wandering_cats:
                    if in_wandering_cats[index] in ("apprentice", "medicine cat apprentice"):
                        print("Can't romance apprentices")
                        continue
                    
                    give_romance.append(in_wandering_cats[index])
                        
                try:
                    index = int(index)
                except ValueError:
                    print(f"romance-index not correct: {index}")
                    continue
                
                if index >= i:
                    continue
                
                give_romance.extend(event.new_cats[index])
        
        # DETERMINE GENDER
        if "male" in attribute_list:
            gender = "male"
        elif "female" in attribute_list:
            gender = "female"
        elif "can_birth" in attribute_list and not game.clan.clan_settings["same sex birth"]:
            gender = "female"
        else:
            gender = None
        
        # WILL THE CAT GET A NEW NAME?
        if "new_name" in attribute_list:
            new_name = True
        elif "old_name" in attribute_list:
            new_name = False
        else:
            new_name = choice([True, False])
        
        # STATUS - must be handled before backstories. 
        status = None
        for _tag in attribute_list:
            match = re.match(r"status:(.+)", _tag)
            if not match:
                continue
            
            if match.group(1) in ("newborn", "kitten", "elder", "apprentice", "warrior", 
                                  "mediator apprentice", "mediator", "medicine cat apprentice", 
                                  "medicine cat"):
                status = match.group(1)
                break
        
        # SET AGE
        age = None
        for _tag in attribute_list:
            match = re.match(r"age:(.+)", _tag)
            if not match:
                continue
            
            if match.group(1) in Cat.age_moons:
                age = randint(Cat.age_moons[match.group(1)][0], Cat.age_moons[match.group(1)][1])
                break
            
            # Set same as first mate.
            if match.group(1) == "mate" and give_mates:
                age = randint(Cat.age_moons[give_mates[0].age][0], 
                              Cat.age_moons[give_mates[0].age][1])
                break

            if match.group(1) == "romance" and give_romance:
                age = randint(Cat.age_moons[give_romance[0].age][0], 
                              Cat.age_moons[give_romance[0].age][1])
                break
                
            if match.group(1) == "has_kits":
                age = randint(19, 120)
                break
                
        
        # CAT TYPES AND BACKGROUND
        if "kittypet" in attribute_list:
            cat_type = "kittypet"
        elif "rogue" in attribute_list:
            cat_type = "rogue"
        elif "loner" in attribute_list:
            cat_type = "loner"
        elif "clancat" in attribute_list:
            cat_type = "former Clancat"
        else:
            cat_type = choice(['kittypet', 'loner', 'former Clancat'])
        
        # LITTER
        litter = False
        if "litter" in attribute_list:
            litter = True
            if status not in ("kitten", "newborn"):
                status = "kitten"
        
        # CHOOSE DEFAULT BACKSTORY BASED ON CAT TYPE, STATUS.
        if status in ("kitten", "newborn"):
            chosen_backstory = choice(BACKSTORIES["backstory_categories"]["abandoned_backstories"])
        elif status == "medicine cat" and cat_type == "former Clancat":
            chosen_backstory = choice(["medicine_cat", "disgraced1"])
        elif status == "medicine cat":
            chosen_backstory = choice(["wandering_healer1", "wandering_healer2"])
        else:
            if cat_type == "former Clancat":
                x = "former_clancat"
            else:
                x = cat_type
            chosen_backstory = choice(BACKSTORIES["backstory_categories"].get(f"{x}_backstories", ["outsider1"]))
        
        # OPTION TO OVERRIDE DEFAULT BACKSTORY
        for _tag in attribute_list:
            match = re.match(r"backstory:(.+)", _tag)
            if match:
                stor = [x for x in match.group(1).split(",") if x in BACKSTORIES["backstories"]]
                if not stor:
                    continue
                
                chosen_backstory = choice(stor)
                break
        
        # KITTEN THOUGHT
        if status in ("kitten", "newborn"):
            thought = "Is snuggled safe in the nursery"
        
        # MEETING - DETERMINE IF THIS IS AN OUTSIDE CAT
        outside = False
        if "meeting" in attribute_list:
            outside = True
            status = cat_type
            new_name = False
            thought = "Is wondering about the new cats they just met"
            
        # IS THE CAT DEAD?
        alive = True
        if "dead" in attribute_list:
            alive = False
            thought = "Explores a new starry world"
        
           
        # Now, it's time to generate the new cat
        # This is a bit of a pain, but I can't re-write this function
        new_cats = create_new_cat(Cat,
                                Relationship,
                                new_name=new_name,
                                loner=cat_type in ["loner", "rogue"],
                                kittypet=cat_type == "kittypet",
                                other_clan=cat_type == 'former Clancat',
                                kit=False if litter else status in ["kitten", "newborn"],  # this is for singular kits, litters need this to be false
                                litter=litter,
                                backstory=chosen_backstory,
                                status=status,
                                age=age,
                                gender=gender,
                                thought=thought,
                                alive=alive,
                                outside=outside,
                                parent1=parent1.ID if parent1 else None,
                                parent2=parent2.ID if parent2 else None  
                                 )
        
        # Add relations to biological parents, if needed
        # Also relations to cat generated in the same block - they are littermates
        # Also make mates
        # DON'T ADD RELATION TO CATS IN THE PATROL
        # That is done in the relationships block of the patrol, to give control for writing. 
        for n_c in new_cats:
            
            # Set Mates
            for inter_cat in give_mates:
                if n_c == inter_cat or n_c.ID in inter_cat.mate:
                    continue
                
                # This is some duplicate work, since this trigger inheritance re-calcs
                # TODO: Optimize
                n_c.set_mate(inter_cat)
            
            #Relations to cats in the same block (littermates)
            for inter_cat in new_cats:
                if n_c == inter_cat:
                    continue
                
                y = random.randrange(0, 20)
                start_relation = Relationship(n_c, inter_cat, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                n_c.relationships[inter_cat.ID] = start_relation
                
            # Relations to bio parents. 
            for par in (parent1, parent2):
                if not par:
                    continue
                
                y = random.randrange(0, 20)
                start_relation = Relationship(par, n_c, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                par.relationships[n_c.ID] = start_relation
                
                y = random.randrange(0, 20)
                start_relation = Relationship(n_c, par, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                n_c.relationships[par.ID] = start_relation
                
            # Update inheritance
            n_c.create_inheritance_new_cat() 
                
        return new_cats
                 
    def _handle_mentor_app(self, event:'DnDEvent') -> str:
        """Handles mentor inflence on apprentices """
        for cat in event.wandering_cats:
            if Cat.fetch_cat(cat.mentor) in event.wandering_cats:
                affect_personality = cat.personality.mentor_influence(Cat.fetch_cat(cat.mentor))
                affect_skills = cat.skills.mentor_influence(Cat.fetch_cat(cat.mentor))
                if affect_personality:
                    History.add_facet_mentor_influence(cat, affect_personality[0], affect_personality[1], affect_personality[2])
                    print(str(cat.name), affect_personality)
                if affect_skills:
                    History.add_skill_mentor_influence(cat, affect_skills[0], affect_skills[1], affect_skills[2])
                    print(str(cat.name), affect_skills)
        
        return ""
    
    # ---------------------------------------------------------------------------- #
    #                                   HELPERS                                    #
    # ---------------------------------------------------------------------------- #
    
    def _add_death_history(self, cat:Cat):
        """Adds death history for a cat """
        
    def _add_potential_history(self, cat:Cat, condition):
        """Add potential history for a condition"""

    def __handle_scarring(self, cat:Cat, scar_list:str, patrol:'Patrol') -> str:
        """Add scar and scar history. Returns scar given """
        
        if len(cat.pelt.scars) >= 4:
            return None
        
        scar_list = [x for x in scar_list if x in Pelt.scars1 + Pelt.scars2 + Pelt.scars3 
                                             and x not in cat.pelt.scars]
        
        if not scar_list:
            return None
        
        chosen_scar = choice(scar_list)
        cat.pelt.scars.append(chosen_scar)
        
        history_text = self.history_scar
        if history_text and isinstance(history_text, str):
            # I'm not 100% sure which one is supposed to be which...
            history_text = history_text if "m_c" not in history_text else history_text.replace("m_c", str(cat.name))
            history_text = history_text if "r_c" not in history_text else history_text.replace("r_c", str(patrol.patrol_random_cat.name))
            history_text = history_text if "o_c_n" not in history_text else history_text.replace("o_c_n", f"{str(patrol.other_clan.name)}Clan")
            
            History.add_scar(cat, history_text)
        else:
            print("WARNING: Scar occured, but scar history is missing")
        
        return chosen_scar
    
    def __handle_condition_history(self, cat:Cat, condition:str, patrol:'Patrol', default_overide=False) -> None:
        """Handles adding potentional history to a cat. default_overide will use the default text for the condition. """
        
        if not (self.history_leader_death and self.history_reg_death and self.history_scar):
            print("WARNING: Injury occured, but some death or scar history is missing.")
        
        final_death_history = None
        if cat.status == "leader":
            if self.history_leader_death:
                final_death_history = self.history_leader_death
        else:
            final_death_history = self.history_reg_death
        
        history_scar = self.history_scar
        
        if default_overide:
            final_death_history = None
            history_scar = None
        
        if final_death_history and isinstance(final_death_history, str):
            final_death_history = final_death_history if "o_c_n" not in final_death_history else final_death_history.replace("o_c_n", f"{str(patrol.other_clan.name)}Clan")
        
        if history_scar and isinstance(history_scar, str):
            history_scar = history_scar if "o_c_n" not in history_scar else history_scar.replace("o_c_n", f"{str(patrol.other_clan.name)}Clan")
        
        
        History.add_possible_history(cat, condition=condition, death_text=final_death_history, scar_text=history_scar)
        
    def __handle_death_history(self, cat: Cat, patrol:'Patrol') -> None:
        """ Handles adding death history, for dead cats. """
        
        if not (self.history_leader_death and self.history_reg_death):
            print("WARNING: Death occured, but some death history is missing.")
        
        final_death_history = None
        if cat.status == "leader":
            if self.history_leader_death:
                final_death_history = self.history_leader_death
        else:
            final_death_history = self.history_reg_death
            
        if not final_death_history:
            final_death_history = "m_c died on patrol."
        
        if final_death_history and isinstance(final_death_history, str):
            final_death_history = final_death_history.replace("o_c_n", f"{str(patrol.other_clan.name)}Clan")
        
        History.add_death(cat, death_text=final_death_history)

    @staticmethod
    def generate_from_info(info: List[dict]) -> List['DnDEventOutcome']:
        """Factory method generates a list of DnDEventOutcome objects based on the dicts."""
        conversation_list = []

        for _d in info:
            conversation_list.append(
                DnDEventOutcome(
                    text=_d.get("text"),
                    exp=_d.get("exp"),
                    dead_cats=_d.get("dead_cats"),
                    lost_cats=_d.get("lost_cats"),
                    injury=_d.get("injury"),
                    history_leader_death=_d["history_text"].get("lead_death") if \
                                        isinstance(_d.get("history_text"), dict) else None,
                    history_reg_death=_d["history_text"].get("reg_death") if  
                                    isinstance(_d.get("history_text"), dict) else None,
                    history_scar=_d["history_text"].get("scar") if  
                                isinstance(_d.get("history_text"), dict) else None,
                    new_cat=_d.get("new_cat"),
                    herbs=_d.get("herbs"),
                    prey=_d.get("prey"),
                    outsider_rep=_d.get("outsider_rep"),
                    other_clan_rep=_d.get("other_clan_rep"),
                    relationship_effects=_d.get("relationships"),
                    relationship_constraints=_d.get("relationship_constraints"),
                    outcome_art=_d.get("art"),
                    outcome_art_clean=_d.get("art_clean"),
                    next_id=_d.get("next_id"),
                    roles=_d.get("roles"),
                    joining_cats=_d.get("joining_cats")
                )
            )
        return conversation_list
