# Skyrim Weapon Damage Calculator

A static, mobile-friendly Skyrim weapon damage calculator designed for GitHub Pages.

## Stack

- HTML
- JavaScript
- Pico CSS via CDN
- Small custom CSS layer
- No server, Python runtime, or build step required


## How to use

1. Choose the weapon type and enter its base damage. Archery also lets you enter ammunition damage.
2. Set your relevant weapon skill, perk rank, enchantment bonuses, potion bonus, and any optional combat perks or buffs.
3. Turn on **weapon improvement (tempering)** if the weapon has been smithed, then enter the smithing skill and bonuses that applied.
4. The sticky **Displayed Damage** value at the top updates automatically as you change inputs.
5. The **Damage** section shows the underlying calculated damage plus normal, power, sneak, and power-sneak attack totals.
6. Expand **Compare & Export** if you want to save multiple builds during the current session and download them together as a CSV file.

## Run locally

Open `index.html` directly in a browser, or serve the folder with any simple static web server.

## GitHub Pages

1. Push the files in this folder to the repository branch you want to publish.
2. Open the repository on GitHub.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Select the branch and the root (`/`) folder.
6. Save.

The app is fully client-side. Saved comparison rows live only in the current browser tab until exported to CSV.

## Source and contributions

The source code is available at [github.com/TriangleSteve/SkyrimCalculators](https://github.com/TriangleSteve/SkyrimCalculators/). Forks, stars, issues, and pull requests are welcome.

## AI use disclosure

AI assistance was used to help convert the original Python/Streamlit implementation into this static HTML, CSS, and JavaScript version. The calculator logic and behavior were adapted from the original app and reviewed during the conversion.
