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
    BRUTE = "Brute" #Babarian
    SILVER_TONGUE = "Silver" # Bard
    CHOSEN = "Chosen" #Cleric
    BLOOD_OLD = "Blood_Old" #Druid
    SKILLED_WARRIOR = "Skilled" #Fighter
    WISDOM = "Wisdom" #Monk
    PROTECTOR = "Protector" #Paladin
    BLOOD_CHOSEN = "Blood_Chosen" #Sorcerer
    KNOWLEDGE = "Knowledge" #Wizard
    SHADOW = "Shadow" #Rouge
    SWORN = "Sworn" #Warlock
    EXPLORER = "Explorer" #Ranger
