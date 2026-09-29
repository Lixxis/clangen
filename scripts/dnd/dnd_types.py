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

    @classmethod
    def from_value(cls, value):
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            normalized = value.strip()
            for member in cls:
                if member.value == normalized:
                    return member
                if member.value.lower() == normalized.lower():
                    return member
            raise ValueError(f"Unknown ClassType value: {value!r}")
        raise TypeError(f"Unsupported ClassType value: {value!r}")
