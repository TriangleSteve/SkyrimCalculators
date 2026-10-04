const WEAPON_DATA = {
  "One-handed": { skillName: "One-handed", perkName: "Armsman", powerName: "Savage Strike", sneakMultiplier: 6.0 },
  "Two-handed": { skillName: "Two-handed", perkName: "Barbarian", powerName: "Devastating Blow", sneakMultiplier: 2.0 },
  "Archery": { skillName: "Archery", perkName: "Overdraw", powerName: "", sneakMultiplier: 3.0 },
  "Dagger": { skillName: "One-handed", perkName: "Armsman", powerName: "Savage Strike", sneakMultiplier: 15.0 }
};

const SEEKER_OF_MIGHT_MULTIPLIER = 1.10;
const WEAPON_PERK_BONUS = 0.20;
const savedResults = [];

const $ = (id) => document.getElementById(id);
const numberValue = (id) => Number($(id).value) || 0;
const checked = (id) => $(id).checked;

function calculateTemperingBonus(smithingLevel, hasPerk, enchantmentBonus, potionBonus, seekerOfMight, isChest = false) {
  const effectiveSkill =
    (smithingLevel - 13.29) *
      (1 + (hasPerk ? 1 : 0)) *
      (1 + enchantmentBonus) *
      (1 + potionBonus) *
      (seekerOfMight ? SEEKER_OF_MIGHT_MULTIPLIER : 1.0) +
    13.29;

  const qualityLevel = (effectiveSkill + 38) * 3 / 103;
  return (3.6 * Math.floor(qualityLevel) - 1.6) * (isChest ? 1 : 0.5);
}

function calculateDisplayedDamage(baseDamage, ammoDamage, skillLevel, perkRank, fortifyEnchantment, fortifyPotion, seekerOfMight, temperImprovement) {
  return (
    (baseDamage + temperImprovement) *
      (1 + skillLevel / 200) *
      (1 + WEAPON_PERK_BONUS * perkRank) *
      (1 + fortifyEnchantment) *
      (1 + fortifyPotion) *
      (seekerOfMight ? SEEKER_OF_MIGHT_MULTIPLIER : 1.0) +
    ammoDamage
  );
}

function powerAttackDamage(displayedDamage, weaponType, hasPowerPerk) {
  return displayedDamage * (weaponType !== "Archery" ? 2 : 1) * (1 + (hasPowerPerk ? 0.25 : 0));
}

function sneakAttackDamage(displayedDamage, weaponType, hasGloves = false) {
  return displayedDamage * WEAPON_DATA[weaponType].sneakMultiplier * (hasGloves ? 2 : 1);
}

function getInputsAndResults() {
  const weaponType = $("weaponType").value;
  const isArchery = weaponType === "Archery";
  const isDagger = weaponType === "Dagger";
  const tempering = checked("tempering");

  const baseDamage = numberValue("baseDamage");
  const ammoDamage = isArchery ? numberValue("ammoDamage") : 0;
  const skillLevel = numberValue("skillLevel");
  const perkRank = numberValue("perkRank");
  const enchantmentBonus = isDagger ? 0 : numberValue("enchantmentBonus") / 100;
  const potionBonus = isDagger ? 0 : numberValue("potionBonus") / 100;
  const hasPowerPerk = !isArchery && checked("powerPerk");
  const hasGloves = !isArchery && checked("gloves");
  const seekerOfMight = checked("seekerMight");

  const smithingLevel = tempering ? numberValue("smithingLevel") : 0;
  const smithingPerk = tempering && checked("smithingPerk");
  const smithingEnchantment = tempering ? numberValue("smithingEnchantment") / 100 : 0;
  const smithingPotion = tempering ? numberValue("smithingPotion") / 100 : 0;
  const smithingSeeker = tempering && checked("smithingSeeker");
  const temperImprovement = tempering
    ? calculateTemperingBonus(smithingLevel, smithingPerk, smithingEnchantment, smithingPotion, smithingSeeker)
    : 0;

  const displayedDamage = calculateDisplayedDamage(
    baseDamage, ammoDamage, skillLevel, perkRank, enchantmentBonus, potionBonus, seekerOfMight, temperImprovement
  );
  const powerAttack = powerAttackDamage(displayedDamage, weaponType, hasPowerPerk);
  const sneakAttack = sneakAttackDamage(displayedDamage, weaponType, hasGloves);
  const powerSneakAttack = sneakAttackDamage(powerAttack, weaponType, hasGloves);

  return {
    weaponType, baseDamage, ammoDamage, skillLevel, perkRank, enchantmentBonus, potionBonus,
    hasPowerPerk, hasGloves, seekerOfMight, tempering, smithingLevel, smithingPerk,
    smithingEnchantment, smithingPotion, smithingSeeker, temperImprovement,
    displayedDamage, powerAttack, sneakAttack, powerSneakAttack
  };
}

function updateWeaponFields() {
  const weaponType = $("weaponType").value;
  const data = WEAPON_DATA[weaponType];
  const isArchery = weaponType === "Archery";
  const isDagger = weaponType === "Dagger";

  $("skillLevelLabel").textContent = `${data.skillName} Skill Level`;
  $("perkRankLabel").textContent = `${data.perkName} Perk Rank`;
  $("enchantmentLabel").textContent = `Sum of Fortify ${data.skillName} Enchantments (%)`;
  $("potionLabel").textContent = `Fortify ${data.skillName} Potion (%)`;
  $("powerPerkLabel").textContent = `${data.powerName} perk (25% standing power attack bonus with ${data.skillName})`;

  $("ammoDamageField").classList.toggle("hidden", !isArchery);
  $("enchantmentField").classList.toggle("hidden", isDagger);
  $("potionField").classList.toggle("hidden", isDagger);
  $("powerPerkField").classList.toggle("hidden", isArchery);
  $("glovesField").classList.toggle("hidden", isArchery);
}

function updateResults() {
  updateWeaponFields();
  $("smithingFields").classList.toggle("hidden", !checked("tempering"));
  $("skillLevelValue").textContent = $("skillLevel").value;
  $("perkRankValue").textContent = $("perkRank").value;
  $("smithingLevelValue").textContent = $("smithingLevel").value;

  const r = getInputsAndResults();
  $("displayedDamage").textContent = Math.round(r.displayedDamage);
  $("stickyDamage").textContent = Math.round(r.displayedDamage);
  $("stickyWeapon").textContent = r.weaponType;
  $("actualDamage").textContent = `${r.displayedDamage.toFixed(1)} actual calculated damage`;
  $("normalAttack").textContent = r.displayedDamage.toFixed(1);
  $("powerAttack").textContent = r.powerAttack.toFixed(1);
  $("sneakAttack").textContent = r.sneakAttack.toFixed(1);
  $("powerSneakAttack").textContent = r.powerSneakAttack.toFixed(1);
}

function renderSavedResults() {
  const tbody = $("savedResults");
  tbody.replaceChildren();
  savedResults.forEach((result) => {
    const row = document.createElement("tr");
    [result.Name, result["Weapon Type"], result["Displayed Damage"]].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    });
    tbody.appendChild(row);
  });

  const hasResults = savedResults.length > 0;
  $("savedResultsWrap").classList.toggle("hidden", !hasResults);
  $("downloadCsv").disabled = !hasResults;
  $("clearResults").disabled = !hasResults;
}

function saveResult() {
  const r = getInputsAndResults();
  savedResults.push({
    "Name": $("resultName").value.trim(),
    "Weapon Type": r.weaponType,
    "Base Damage": r.baseDamage,
    "Ammo Damage (if applicable)": r.ammoDamage,
    "Skill Level": r.skillLevel,
    "Weapon Perk Rank (e.g. Armsman)": r.perkRank,
    "Fortify Skill Enchantments": r.enchantmentBonus,
    "Fortify Skill Potion": r.potionBonus,
    "Using power attack perk (e.g. Savage Strike)": r.hasPowerPerk,
    "Using sneak multiplier gloves": r.hasGloves,
    "Seeker of Might damage boost": r.seekerOfMight,
    "Include Smithing improvement": r.tempering,
    "Smithing Skill": r.smithingLevel,
    "Smithing Perk": r.smithingPerk,
    "Smithing Enchantments": r.smithingEnchantment,
    "Smithing Potion": r.smithingPotion,
    "Smithing Seeker of Might bonus": r.smithingSeeker,
    "Smithing Improvement Amount": r.temperImprovement,
    "Displayed Damage": Math.floor(r.displayedDamage),
    "Actual Damage": r.displayedDamage,
    "Power Attack Damage": r.powerAttack,
    "Sneak Attack Damage": r.sneakAttack,
    "Power Sneak Attack Damage": r.powerSneakAttack
  });
  renderSavedResults();
}

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}

function downloadCsv() {
  if (!savedResults.length) return;
  const headers = Object.keys(savedResults[0]);
  const rows = [headers.join(","), ...savedResults.map((row) => headers.map((h) => csvEscape(row[h])).join(","))];
  const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "results.csv";
  link.click();
  URL.revokeObjectURL(url);
}

document.querySelectorAll("input, select").forEach((el) => {
  el.addEventListener("input", updateResults);
  el.addEventListener("change", updateResults);
});

$("saveResult").addEventListener("click", saveResult);
$("downloadCsv").addEventListener("click", downloadCsv);
$("clearResults").addEventListener("click", () => {
  savedResults.length = 0;
  renderSavedResults();
});

updateResults();
renderSavedResults();
