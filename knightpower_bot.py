import discord
from discord import app_commands
from discord.ext import commands
import os

from knightpower_calc import (
    state_power as calc_state_power,
    talent_bonus as calc_talent_bonus,
    lover_ballroom as calc_lover_ballroom,
    lover_greeting as calc_lover_greeting,
)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} is online with slash commands.')

@bot.tree.command(name="state_power", description="Calculate Knight State Power")
@app_commands.describe(
    talent_stars="Number of talent stars",
    knight_level="Knight's level",
    book_bonus="Book bonus value"
)
async def state_power(interaction: discord.Interaction, talent_stars: float, knight_level: float, book_bonus: float):
    sp = calc_state_power(talent_stars, knight_level, book_bonus)
    await interaction.response.send_message(f"State Power: {sp:.2f}")

@bot.tree.command(name="talent_bonus", description="Calculate Knight Talent Bonus")
@app_commands.describe(
    talent_stars="Number of talent stars",
    level="Knight's level"
)
async def talent_bonus(interaction: discord.Interaction, talent_stars: float, level: int):
    sp_bonus = calc_talent_bonus(talent_stars, level)
    await interaction.response.send_message(f"Knight Talent Bonus: {sp_bonus:.2f}")

@bot.tree.command(name="lover_ballroom", description="Calculate Lover Power from Ballroom")
@app_commands.describe(
    charm="Lover's charm value"
)
async def lover_ballroom(interaction: discord.Interaction, charm: float):
    lp_d = calc_lover_ballroom(charm)
    await interaction.response.send_message(f"Ballroom Lover Power: {lp_d:.2f}")

@bot.tree.command(name="lover_greeting", description="Calculate Lover Power from Greeting")
@app_commands.describe(
    charm="Lover's charm value"
)
async def lover_greeting(interaction: discord.Interaction, charm: float):
    lp_g = calc_lover_greeting(charm)
    await interaction.response.send_message(f"Greeting Lover Power: {lp_g:.2f}")

# Run the bot using the token from environment variables
bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    print("Error: BOT_TOKEN environment variable not set.")
else:
    bot.run(bot_token)
