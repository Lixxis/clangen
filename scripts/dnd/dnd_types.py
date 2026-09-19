from enum import Enum

class LinageType(Enum):
    CAT = "cat"
    ELF = "elf"
    DWARF = "dwarf"
    ORC = "orc"

class ElfSubLinageType(Enum):
    HIGH_ELF = "high elf"

class StatType(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

class DnDSkillType(Enum):
    ACROBATICS = "acrobatics"
    ANIMAL_HANDLING = "animal handling"
    ARCANA = "arcana"
    ATHLETICS = "athletics"
    DECEPTION = "deception"
    HISTORY = "history"
    INSIGHT = "insight"
    INTIMIDATION = "intimidation"
    INVESTIGATION = "investigation"
    MEDICINE = "medicine"
    NATURE = "nature"
    PERCEPTION = "perception"
    PERFORMANCE = "performance"
    PERSUASION = "persuasion"
    RELIGION = "religion"
    SLEIGHT_OF_PAW = "sleight of paw"
    STEALTH = "stealth"
    SURVIVAL = "survival"

class ClassType(Enum):
    BRUTE = "Brute"
    SILVER_TONGUE = "Silver tongue"
    CHOSEN = "Chosen of the StarClan"
    BLOOD_OLD = "Blood of the Old"
    SKILLED_WARRIOR = "Skilled Warrior"
    WISDOM = "Wisdom of the Paws"
    PROTECTOR = "Protector of StarClan"
    BLOOD_CHOSEN = "Blood of the Chosen One"
    KNOWLEDGE = "Knowledge Seeker"
    SHADOW = "Shadow Stalker"
