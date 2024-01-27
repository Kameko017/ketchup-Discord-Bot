import discord
from discord import app_commands
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtubeAPI

def run():
    load_dotenv()
    DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
    YOUTUBEID = os.getenv("YOUTUBE_ID")
    GUILD_ID = os.getenv("GUILD_ID")
    
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents,command_prefix="!!")
    
    global intervalsTime
    intervalsTime = 30
    @bot.event
    async def on_ready():
        global guild 
        guild =  discord.Object(id=GUILD_ID)
        try:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        except Exception as e:
            print("An error occurred while syncing: ", e)   
        print("bot is ready!")

    @bot.tree.command()
    async def setup(interaction: discord.Interaction,
                    intervals:int =  30, 
                    __show_subscriber:bool = True,
                    __show_view:bool = False,
                    __subscriber_channel:discord.VoiceChannel = None,
                    __view_channel:discord.VoiceChannel = None,
                    __category: discord.CategoryChannel = None ):
        global subscriber_channel
        global view_channel
        global show_subscriber
        global show_view
        show_subscriber = __show_subscriber
        show_view = __show_view
        intervalsTime = intervals
        await interaction.response.send_message("執行中...",ephemeral=True)
        youtubeAPI.setup(YOUTUBEID)
        if __category is None:
            category = await guild.create_category("資料", overwrites={guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)})
        else:
            category = __category
        if __show_subscriber:
            if __subscriber_channel is None:
                subscriber_channel = await guild.create_voice_channel("訂閱數: None", category=category)
            else:
                subscriber_channel = __subscriber_channel
        if __show_view:
            if __subscriber_channel is None:
                view_channel = await guild.create_voice_channel("觀看數: None", category=category)
            else:
                view_channel = __view_channel
        await interaction.followup.send("設置完成！",ephemeral = True)
    
    @tasks.loop(seconds=intervalsTime)
    async def request_function():
        subscriberCount = 0
        viewCount = 0
        request = youtubeAPI.request()
        new_subscriber_count = request[0]
        new_view_count = request[1]
        if new_subscriber_count != subscriberCount or new_view_count != viewCount:
            subscriberCount = new_subscriber_count
            viewCount = new_view_count
            print(subscriberCount)
            print(viewCount)
            await edit_channel(subscriberCount=subscriberCount,viewCount=viewCount)

    async def edit_channel(subscriberCount,viewCount):
        if show_subscriber :
            await subscriber_channel.edit(name=f"訂閱數: {subscriberCount}")
        if show_view :
            await view_channel.edit(name=f"觀看數: {viewCount}")
    
    @bot.hybrid_command()
    async def start_request(ctx):
        request_function.start()
        await ctx.send("Start!",ephemeral = True)
    @bot.hybrid_command()
    async def end_request(ctx): 
        request_function.stop()
        await ctx.send("Stop!",ephemeral = True)
    
    
    bot.run(token=DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run() 