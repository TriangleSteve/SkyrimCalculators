
import streamlit as st
from functions import (
    calculate_displayed_damage,
    power_attack_damage,
    sneak_attack_damage,
    dual_wield_power_attack_damage,
    WEAPON_DATA,
    MIN_SKILL,
    MAX_SKILL,
)

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Skyrim Weapon Damage Calculator", layout="centered")

st.title("Skyrim Weapon Damage Calculator")
st.markdown(
    "Calculate displayed and effective weapon damage based on skills, perks, and buffs."
)

st.divider()


# Weapon inputs
st.header("Weapon")

weapon_type = st.selectbox(
    "Weapon Type",
    WEAPON_DATA.keys(),
)

label = st.text(weapon_type)
skill_name = WEAPON_DATA[weapon_type]["skill_name"]
perk_name = WEAPON_DATA[weapon_type]["perk_name"]

base_damage = st.number_input(
    "Weapon Base Damage (found on [UESP Weapon Reference](https://en.uesp.net/wiki/Skyrim:Weapons), e.g. Dragonbone Mace = 17)",
    min_value=1,
    max_value=35,
    step=1,
    value=18
)

st.divider()


# Skills
st.header("Weapon Proficiency")

skill_level = st.slider(
    f"{skill_name} Skill Level",
    min_value=MIN_SKILL,
    max_value=MAX_SKILL,
    value=MAX_SKILL,
)

skill_perk_bonus = st.slider(
    f"{perk_name} Perk Rank",
    min_value=0,
    max_value=5,
    value=5,
    help="Placeholder for Armsman / Barbarian, etc.",
)

skill_enchantment_bonus = st.number_input(
    f"Sum of Fortify {skill_name} Enchantments (%)",
    min_value=0,
    value=120,
) / 100

skill_potion_bonus = st.number_input(
    f"Fortify {skill_name} Potion (%)",
    min_value=0,
    value=50,
) / 100

skill_seeker_of_might = st.checkbox("Seeker of Might (+10% damage)")

st.divider()


# Perks & buffs
st.header("Smithing")

tempering = st.checkbox("Include weapon improvement (tempering)", value=False)

if tempering:
    smithing_level = st.slider(
        "Smithing Skill Level",
        min_value=MIN_SKILL,
        max_value=MAX_SKILL,
        value=MAX_SKILL,
    )

    smithing_perk_bonus = st.checkbox("Has associated smithing perk (e.g. Daedric for Dragonbone weapons)")

    smithing_enchantment_bonus = st.number_input(
        "Smithing Enchantments (%)",
        min_value=0,
        value=75,
    ) / 100

    smithing_potion_bonus = st.number_input(
        "Smithing Potion (%)",
        min_value=0,
        value=50,
    ) / 100

    smithing_seeker_of_might = st.checkbox("Seeker of Might (+10% smithing)")
else:
    smithing_level = 0
    smithing_perk_bonus = False
    smithing_enchantment_bonus = 0
    smithing_potion_bonus = 0
    smithing_seeker_of_might = False

st.divider()

# -----------------------------
# Calculations
# -----------------------------

displayed_damage = calculate_displayed_damage(
    base_damage=base_damage,
    skill_level=skill_level,
    perk_rank=skill_perk_bonus,
    fortify_enchantment=skill_enchantment_bonus,
    fortify_potion=skill_potion_bonus,
    seeker_of_might=skill_seeker_of_might,
    tempering=tempering,
    smithing_level=smithing_level,
    smithing_perk=smithing_perk_bonus,
    smithing_enchantment=smithing_enchantment_bonus,
    smithing_potion=smithing_potion_bonus,
    smithing_seeker=smithing_seeker_of_might,
)

power_attack = power_attack_damage(displayed_damage, weapon_type)
sneak_attack = sneak_attack_damage(displayed_damage, weapon_type)
dual_wield = dual_wield_power_attack_damage(displayed_damage)


# -----------------------------
# Output
# -----------------------------

st.header("Results")

st.metric(f"Displayed Weapon Damage", f"{displayed_damage:.1f}")
st.metric("Power Attack Damage", f"{power_attack:.1f}")
st.metric("Sneak Attack Damage", f"{sneak_attack:.1f}")
st.metric("Dual-Wield Power Attack Damage", f"{dual_wield:.1f}")

st.caption("All formulas are placeholders and will be replaced with UESP-accurate values.")
