import discord
from discord.ext import commands
import Setting
import os

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents,command_prefix="!!")
    @bot.event
    async def on_ready():
        await load() 
        try:
            bot.tree.copy_global_to(guild=Setting.guild)
            await bot.tree.sync(guild=Setting.guild)
        except Exception as e:
            print("An error occurred while syncing: ", e)   
        print("bot is ready!")
    
    async def load():
        for filename in os.listdir("./cogs"):
            if filename.endswith("py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"load {filename[:-3]} Cog")
    
    @bot.command(name="sync") 
    async def sync(ctx):
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    
    bot.run(token=Setting.DISCORD_API_TOKEN)
    
if __name__ == "__main__":
    run() 