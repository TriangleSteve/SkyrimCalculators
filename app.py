
import streamlit as st
import pandas as pd
from functions import (
    calculate_displayed_damage,
    calculate_tempering_bonus,
    power_attack_damage,
    sneak_attack_damage,
    WEAPON_DATA,
    MIN_SKILL,
    MAX_SKILL,
)

# Initialize storage
if "damage_results" not in st.session_state:
    st.session_state.damage_results = []

# -----------------------------
# Streamlit UI
# -----------------------------

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.set_page_config(
    page_title="Skyrim Weapon Damage Calculator", 
    layout="centered",
    page_icon=":abacus:",
    )

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

skill_name = WEAPON_DATA[weapon_type]["skill_name"]
perk_name = WEAPON_DATA[weapon_type]["perk_name"]
power_perk_name = WEAPON_DATA[weapon_type]["power_name"]

base_damage = st.number_input(
    "Weapon Base Damage (found on [UESP Weapon Reference](https://en.uesp.net/wiki/Skyrim:Weapons#One-handed_Weapons), e.g. Dragonbone Mace = 17)",
    min_value=1,
    max_value=35,
    step=1,
    value=18
)
if weapon_type == "Archery":
    ammo_damage = st.number_input(
        "Ammo Damage (found on [UESP Ammunition](https://en.uesp.net/wiki/Skyrim:Ammunition#Arrows), e.g. Dragonbone Arrows = 25)",
        min_value=4,
        max_value=35,
        step=1,
        value=24
    )
else:
    ammo_damage = 0

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
)
if weapon_type != "Dagger":
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
else:
    skill_enchantment_bonus = 0
    skill_potion_bonus = 0

if weapon_type != "Archery":
    has_power_perk = st.checkbox(f"{power_perk_name} perk (25% standing power attack bonus with {skill_name})")
    has_gloves = st.checkbox(f"Using sneak multiplier gloves (e.g. Cicero's gloves)")
else:
    has_power_perk = False
    has_gloves = False

skill_seeker_of_might = st.checkbox("Seeker of Might (+10% damage)")


# TODO add dual wield logic/calculations
# if weapon_type in ("One-handed", "Dagger"):
#     use_dual = st.checkbox("Calculate dual wield damage", value=False)

#     if use_dual:
#         dual_perk = st.checkbox("Dual Savagery perk", value=False)
#         secondary_damage = st.number_input(
#             "Enter displayed damage for left hand weapon (e.g. offhand Dragonbone dagger with One-handed 100 + Armsman 5 = 36)",
#             min_value=0.0,
#             value=39.0,
#             format="%0.1f"
#             )


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
    
    # Calculate the improvement from smithing
    temper_improvement = calculate_tempering_bonus(
        smithing_level,
        smithing_perk_bonus,
        smithing_enchantment_bonus,
        smithing_potion_bonus,
        smithing_seeker_of_might
    )
else:
    smithing_level = 0
    smithing_perk_bonus = False
    smithing_enchantment_bonus = 0
    smithing_potion_bonus = 0
    smithing_seeker_of_might = False
    temper_improvement = 0


st.divider()

# -----------------------------
# Calculate final damage outputs
# -----------------------------

displayed_damage = calculate_displayed_damage(
    base_damage=base_damage,
    ammo_damage=ammo_damage,
    skill_level=skill_level,
    perk_rank=skill_perk_bonus,
    fortify_enchantment=skill_enchantment_bonus,
    fortify_potion=skill_potion_bonus,
    seeker_of_might=skill_seeker_of_might,
    temper_improvement=temper_improvement
)

power_attack = power_attack_damage(displayed_damage, weapon_type, has_power_perk)
sneak_attack = sneak_attack_damage(displayed_damage, weapon_type, has_gloves)
power_sneak_attack = sneak_attack_damage(power_attack, weapon_type, has_gloves)

damage_df = pd.DataFrame({
     "Normal Attack":[displayed_damage, round(power_attack, 1)], 
     "Sneak Attack":[round(sneak_attack, 1), round(power_sneak_attack, 1)]
    }, index=["Normal Attack", "Power Attack"])

# -----------------------------
# Output
# -----------------------------

st.header("Results")

st.metric(f"Displayed Weapon Damage", round(displayed_damage))
st.table(damage_df.style.format("{:.1f}"))

# -----------------------------
# Session saves/download
# -----------------------------

st.divider()

st.header("Export")

st.caption("Save any number of outputs to the browser session and download them in a single CSV for comparison and reference. Export will include all inputs/outputs as columns.")

weapon_output_name = st.text_input("(Optional) add an easy to remember name (e.g. Dragonbone Sword max without potions/enchanting)")
if st.button("Save to session"):
    st.session_state.damage_results.append({
        "Name": weapon_output_name,
        "Weapon Type": weapon_type,
        "Base Damage": base_damage,
        "Ammo Damage (if applicable)": ammo_damage,
        "Skill Level": skill_level,
        "Weapon Perk Rank (e.g. Armsman)": skill_perk_bonus,
        "Fortify Skill Enchantments": skill_enchantment_bonus,
        "Fortify Skill Potion": skill_potion_bonus,
        "Using power attack perk (e.g. Savage Strike)": has_power_perk,
        "Using sneak multiplier gloves": has_gloves,
        "Seeker of Might damage boost": skill_seeker_of_might,
        "Include Smithing improvement": tempering,
        "Smithing Skill": smithing_level,
        "Smithing Perk": smithing_perk_bonus,
        "Smithing Enchantments": smithing_enchantment_bonus,
        "Smithing Potion": smithing_potion_bonus,
        "Smithing Seeker of Might bonus": smithing_seeker_of_might,
        "Smithing Improvement Amount": temper_improvement,
        "Displayed Damage": displayed_damage.__floor__(),
        "Actual Damage": displayed_damage,
        "Power Attack Damage": power_attack,
        "Sneak Attack Damage": sneak_attack,
        "Power Sneak Attack Damage": power_sneak_attack
    })

if st.session_state.damage_results:
    damage_download_df = pd.DataFrame(st.session_state.damage_results)
    st.table(damage_download_df[["Name","Weapon Type","Displayed Damage"]])

    st.download_button(
        label="Download CSV",
        data=damage_download_df.to_csv(index=False),
        file_name="results.csv",
        mime="text/csv"
    )
