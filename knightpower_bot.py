
import os
import json
import discord
from discord.ext import commands
from discord import app_commands

from knightpower_calc import (
    state_power as calc_state_power,
    talent_bonus as calc_talent_bonus,
    lover_ballroom as calc_lover_ballroom,
    lover_greeting as calc_lover_greeting,
)

# Load Knight list JSON
with open("knight_list.json", "r") as f:
    KNIGHT_MAP = {entry["name"].lower(): entry["stars"] for entry in json.load(f)}

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online with slash commands.")

# Slash Commands
@bot.tree.command(name="state_power", description="Calculate Knight State Power")
@app_commands.describe(talent_stars="Number of talent stars", knight_level="Knight's level", book_bonus="Book bonus value")
async def state_power(interaction: discord.Interaction, talent_stars: float, knight_level: float, book_bonus: float):
    result = calc_state_power(talent_stars, knight_level, book_bonus)
    await interaction.response.send_message(f"State Power: {result:.2f}")

@bot.tree.command(name="talent_bonus", description="Calculate Knight Talent Bonus")
@app_commands.describe(talent_stars="Number of talent stars", level="Knight's level")
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

@bot.tree.command(name="knight", description="Calculate power using saved knight name, level, and book bonus")
@app_commands.describe(name="Knight's name", level="Knight's level", book_bonus="Book bonus")
async def knight(interaction: discord.Interaction, name: str, level: float, book_bonus: float):
    key = name.lower()
    if key not in KNIGHT_MAP:
        await interaction.response.send_message(f"Knight '{name}' not found.")
        return

    stars = KNIGHT_MAP[key]
    result = calc_state_power(stars, level, book_bonus)
    await interaction.response.send_message(
        f"**{name}** — Stars: {stars}, Level: {level}, Book Bonus: {book_bonus}\n**State Power:** {result:.2f}"
    )

# Start bot
bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    print("Error: BOT_TOKEN environment variable not set.")
else:
    bot.run(bot_token)
