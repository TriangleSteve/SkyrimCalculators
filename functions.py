"""
Skyrim weapon damage calculations and reference constants.

Formula sources:
https://en.uesp.net/wiki/Skyrim:Weapons
https://en.uesp.net/wiki/Skyrim:Damage
https://en.uesp.net/wiki/Skyrim:Smithing
"""

# -----------------------------
# UI / reference constants
# -----------------------------

WEAPON_DATA = {
    "One-handed": {
        "skill_name": "One-handed",
        "perk_name": "Armsman",
        "power_name": "Savage Strike",
        "sneak_multiplier": 6.0,
    },
    "Two-handed": {
        "skill_name": "Two-handed",
        "perk_name": "Barbarian",
        "power_name": "Devastating Blow",
        "sneak_multiplier": 2.0,
    },
    "Archery": {
        "skill_name": "Archery",
        "perk_name": "Overdraw",
        "power_name": "",
        "sneak_multiplier": 3.0
    },
    "Dagger": {
        "skill_name": "One-handed",
        "perk_name": "Armsman",
        "power_name": "Savage Strike",
        "sneak_multiplier": 15.0,
    },
}

SEEKER_OF_MIGHT_MULTIPLIER = 1.10  # +10%
WEAPON_PERK_BONUS = 0.20  # 20% per rank
MIN_SKILL = 15
MAX_SKILL = 100

# -----------------------------
# Smithing / tempering
# -----------------------------

def calculate_tempering_bonus(
    smithing_level: int,
    has_perk: bool,
    enchantment_bonus: float,
    potion_bonus: float,
    seeker_of_might: bool,
    is_chest: bool = False
) -> float:
    effective_skill = (
        (smithing_level - 13.29) 
        * (1 + (1 if has_perk else 0)) 
        * (1 + enchantment_bonus) 
        * (1 + potion_bonus) 
        * (SEEKER_OF_MIGHT_MULTIPLIER if seeker_of_might else 1.0)
        + 13.29
    )

    quality_level = (effective_skill + 38) * 3 / 103

    return (3.6 * quality_level.__floor__() - 1.6) * (1 if is_chest else 0.5)


def calculate_displayed_damage(
    base_damage: int,
    ammo_damage: int,
    skill_level: int,
    perk_rank: int,
    fortify_enchantment: float,
    fortify_potion: float,
    seeker_of_might: bool,
    temper_improvement: float
) -> float:
    displayed_damage =  (
        (base_damage + temper_improvement)
        * (1 + skill_level / 200) # skill_multiplier
        * (1 + WEAPON_PERK_BONUS * perk_rank) # weapon_perk_multiplier
        * (1 + fortify_enchantment)
        * (1 + fortify_potion)
        * (SEEKER_OF_MIGHT_MULTIPLIER if seeker_of_might else 1.0)
        + ammo_damage
    )
    return displayed_damage

# -----------------------------
# Attack damage
# -----------------------------

def power_attack_damage(displayed_damage: float, weapon_type: str, has_power_perk: bool) -> float:
    damage = (
        displayed_damage 
        * (2 if weapon_type != "Archery" else 1)     # Power attack multiplier
        * (1 + (0.25 if has_power_perk else 0))
    )
    return damage


def sneak_attack_damage(displayed_damage: float, weapon_type: str, has_gloves: bool = False) -> float:
    damage = (
        displayed_damage 
        * WEAPON_DATA[weapon_type]["sneak_multiplier"] 
        * (2 if has_gloves else 1)
    )
    return damage

# TODO Add dual power attacks
