import pytest

from functions import (
    calculate_displayed_damage,
    power_attack_damage,
    sneak_attack_damage,
)


def test_base_damage_no_bonuses():
    damage = calculate_displayed_damage(
        base_damage=10,
        skill_level=15,
        perk_rank=0,
        fortify_enchantment=0.0,
        fortify_potion=0.0,
        seeker_of_might=False,
        tempering=False,
    )

    assert damage == pytest.approx(10.75, rel=1e-2)
    # 10 × (1 + 0.5 × 0.15) = 10.75


def test_skill_100_no_perks():
    damage = calculate_displayed_damage(
        base_damage=10,
        skill_level=100,
        perk_rank=0,
        fortify_enchantment=0.0,
        fortify_potion=0.0,
        seeker_of_might=False,
        tempering=False,
    )

    assert damage == pytest.approx(15.0, rel=1e-2)


def test_skill_100_armsman_5():
    damage = calculate_displayed_damage(
        base_damage=10,
        skill_level=100,
        perk_rank=5,
        fortify_enchantment=0.0,
        fortify_potion=0.0,
        seeker_of_might=False,
        tempering=False,
    )

    assert damage == pytest.approx(30.0, rel=1e-2)


def test_one_handed_power_attack():
    base_damage = 30.0
    power_damage = power_attack_damage(
        base_damage,
        weapon_type="One-handed",
    )

    assert power_damage == pytest.approx(60.0, rel=1e-2)


def test_sneak_attack_one_handed():
    base_damage = 30.0
    sneak_damage = sneak_attack_damage(
        base_damage,
        weapon_type="One-handed",
    )

    assert sneak_damage == pytest.approx(180.0, rel=1e-2)
