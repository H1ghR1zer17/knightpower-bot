import os
import json
import discord
from discord.ext import commands
from discord import app_commands
from math import sqrt

from knightpower_calc import (
    state_power as calc_state_power,
    talent_bonus as calc_talent_bonus,
    lover_ballroom as calc_lover_ballroom,
    lover_greeting as calc_lover_greeting,
)

# Load knight_list.json using an absolute path
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "knight_list.json")
    with open(file_path, "r") as f:
        KNIGHT_LIST = json.load(f)
        print(f"✅ Loaded {len(KNIGHT_LIST)} knights from {file_path}")
except Exception as e:
    print(f"❌ Failed to load knight_list.json: {e}")
    KNIGHT_LIST = []

KNIGHT_MAP = {entry["name"].lower(): entry["stars"] for entry in KNIGHT_LIST}
KNIGHT_NAMES = [entry["name"] for entry in KNIGHT_LIST]

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ {bot.user} is online with {len(synced)} slash commands.")

# ───── Slash Commands ─────

@bot.tree.command(name="state_power", description="Calculate Knight State Power")
@app_commands.describe(
    talent_stars="Number of talent stars",
    knight_level="Knight's level",
    book_bonus="Book bonus value"
)
async def state_power(interaction: discord.Interaction, talent_stars: float, knight_level: float, book_bonus: float):
    result = calc_state_power(talent_stars, knight_level, book_bonus)
    await interaction.response.send_message(f"State Power: {result:.2f}")

@bot.tree.command(name="talent_bonus", description="Calculate Knight Talent Bonus")
@app_commands.describe(
    talent_stars="Number of talent stars",
    level="Knight's level"
)
async def talent_bonus(interaction: discord.Interaction, talent_stars: float, level: int):
    result = calc_talent_bonus(talent_stars, level)
    await interaction.response.send_message(f"Knight Talent Bonus: {result:.2f}")

@bot.tree.command(name="lover_ballroom", description="Calculate Lover Power from Ballroom")
@app_commands.describe(charm="Lover's charm value")
async def lover_ballroom(interaction: discord.Interaction, charm: float):
    result = calc_lover_ballroom(charm)
    await interaction.response.send_message(f"Ballroom Lover Power: {result:.2f}")

@bot.tree.command(name="lover_greeting", description="Calculate Lover Power from Greeting")
@app_commands.describe(charm="Lover's charm value")
async def lover_greeting(interaction: discord.Interaction, charm: float):
    result = calc_lover_greeting(charm)
    await interaction.response.send_message(f"Greeting Lover Power: {result:.2f}")

@bot.tree.command(name="knight", description="Calculate power using knight name, level, book bonus, and SP values")
@app_commands.describe(
    name="Select a knight",
    level="Knight's level",
    book_bonus="Book bonus value",
    current_sp="Your current total state power",
    sp="Manual SP input (optional)"
)
async def knight(
    interaction: discord.Interaction,
    name: str,
    level: float,
    book_bonus: float,
    current_sp: float,
    sp: float
):
    key = name.lower()
    if key not in KNIGHT_MAP:
        await interaction.response.send_message(f"Knight '{name}' not found.")
        return

    stars = KNIGHT_MAP[key]
    calculated_sp = calc_state_power(stars, level, book_bonus)
    potential_sp = current_sp + calculated_sp

    await interaction.response.send_message(
        f"**{name}** — Stars: {stars}, Level: {level}, Book Bonus: {book_bonus}\n"
        f"Calculated SP: {calculated_sp:.2f}\n"
        f"Manual SP Input: {sp:.2f}\n"
        f"Current SP: {current_sp:.2f}\n"
        f"**SP Potential:** {potential_sp:.2f}"
    )

# Autocomplete for /knight
@knight.autocomplete("name")
async def knight_name_autocomplete(interaction: discord.Interaction, current: str):
    matches = [
        app_commands.Choice(name=name, value=name)
        for name in KNIGHT_NAMES
        if current.lower() in name.lower()
    ]
    return matches[:25]

# ───── Run Bot ─────
bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    print("❌ BOT_TOKEN not found in environment variables.")
else:
    bot.run(bot_token)
