"""
Skyrim weapon damage calculations and reference constants.

Formula sources:
https://en.uesp.net/wiki/Skyrim:Weapons
https://en.uesp.net/wiki/Skyrim:Damage
https://en.uesp.net/wiki/Skyrim:Smithing
https://en.uesp.net/wiki/Skyrim:One-handed
https://en.uesp.net/wiki/Skyrim:Two-handed
"""

# -----------------------------
# UI / reference constants
# -----------------------------

WEAPON_DATA = {
    "One-handed": {
        "skill_name": "One-handed",
        "perk_name": "Armsman",
        "power_attack_multiplier": 2.0,
        "sneak_multiplier": 6.0,
    },
    "Two-handed": {
        "skill_name": "Two-handed",
        "perk_name": "Barbarian",
        "power_attack_multiplier": 2.5,
        "sneak_multiplier": 3.0,
    },
    "Dagger": {
        "skill_name": "One-handed",
        "perk_name": "Armsman",
        "power_attack_multiplier": 2.0,
        # Assassin's Blade replaces normal sneak later
        "sneak_multiplier": 15.0,
    },
}

SEEKER_OF_MIGHT_MULTIPLIER = 1.10  # +10%
WEAPON_PERK_BONUS = 0.20  # 20% per rank
MIN_SKILL = 15
MAX_SKILL = 100

# -----------------------------
# Core multipliers
# -----------------------------

def skill_multiplier(skill_level: int) -> float:
    """
    Weapon skill damage multiplier.

    UESP:
    Damage multiplier = 1 + 0.5 x (Skill / 100)

    https://en.uesp.net/wiki/Skyrim:Damage
    """
    return 1 + 0.5 * (skill_level / MAX_SKILL)


def weapon_perk_multiplier(perk_rank: int) -> float:
    """
    Armsman / Barbarian / Overdraw perk multiplier.

    Each rank adds 20% damage.

    UESP:
    https://en.uesp.net/wiki/Skyrim:One-handed#Armsman
    https://en.uesp.net/wiki/Skyrim:Two-handed#Barbarian
    https://en.uesp.net/wiki/Skyrim:Archery#Overdraw
    """
    return 1 + (WEAPON_PERK_BONUS * perk_rank)


def fortify_multiplier(enchantment_bonus: float, potion_bonus: float) -> float:
    """
    Fortify One-handed / Two-handed / Archery effects.

    Enchantments and potions stack additively.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Fortify_One-handed
    https://en.uesp.net/wiki/Skyrim:Fortify_Two-handed
    https://en.uesp.net/wiki/Skyrim:Fortify_Archery
    """
    return 1 + enchantment_bonus + potion_bonus


def seeker_of_might_multiplier(enabled: bool) -> float:
    """
    Seeker of Might bonus.

    +10% damage to combat skills.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Black_Book:_The_Sallow_Regent
    """
    return SEEKER_OF_MIGHT_MULTIPLIER if enabled else 1.0


# -----------------------------
# Smithing / tempering
# -----------------------------

def tempering_bonus(
    base_damage: float,
    smithing_level: int,
    has_perk: bool,
    enchantment_bonus: float,
    potion_bonus: float,
    seeker_of_might: bool,
) -> float:
    """
    Weapon improvement (tempering) bonus.

    Approximates UESP behavior closely enough for player calculators.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Smithing
    https://en.uesp.net/wiki/Skyrim:Damage#Weapon_Improvement
    """
    if smithing_level <= 0:
        return 0.0

    perk_multiplier = 1.5 if has_perk else 1.0

    return (
        base_damage
        * (smithing_level / 200)
        * perk_multiplier
        * fortify_multiplier(enchantment_bonus, potion_bonus)
        * seeker_of_might_multiplier(seeker_of_might)
    )


# -----------------------------
# Final damage calculations
# -----------------------------

def calculate_displayed_damage(
    base_damage: float,
    skill_level: int,
    perk_rank: int,
    fortify_enchantment: float,
    fortify_potion: float,
    seeker_of_might: bool,
    tempering: bool,
    smithing_level: int = 0,
    smithing_perk: bool = False,
    smithing_enchantment: float = 0.0,
    smithing_potion: float = 0.0,
    smithing_seeker: bool = False,
) -> float:
    """
    Displayed weapon damage shown in inventory.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Damage
    """
    improvement = (
        tempering_bonus(
            base_damage,
            smithing_level,
            smithing_perk,
            smithing_enchantment,
            smithing_potion,
            smithing_seeker,
        )
        if tempering
        else 0.0
    )

    return (
        (base_damage + improvement)
        * skill_multiplier(skill_level)
        * weapon_perk_multiplier(perk_rank)
        * fortify_multiplier(fortify_enchantment, fortify_potion)
        * seeker_of_might_multiplier(seeker_of_might)
    )


def power_attack_damage(displayed_damage: float, weapon_type: str) -> float:
    """
    Power attack damage.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Power_Attack
    """
    return displayed_damage * WEAPON_DATA[weapon_type]["power_attack_multiplier"]


def sneak_attack_damage(displayed_damage: float, weapon_type: str) -> float:
    """
    Sneak attack damage.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Sneak#Damage
    """
    return displayed_damage * WEAPON_DATA[weapon_type]["sneak_multiplier"]


def dual_wield_power_attack_damage(displayed_damage: float) -> float:
    """
    Dual wield power attack damage.

    Approximated combined damage multiplier.

    UESP:
    https://en.uesp.net/wiki/Skyrim:Dual_Wielding
    """
    return displayed_damage * 3.0
