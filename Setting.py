import os
from dotenv import load_dotenv
import discord

load_dotenv()
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
guild =  discord.Object(id=GUILD_ID)