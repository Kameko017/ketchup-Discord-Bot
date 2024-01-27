import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import youtubeAPI
import threading
import time
import asyncio

def run():
    load_dotenv()
    DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
    YOUTUBEID = os.getenv("YOUTUBE_ID")
    
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents,command_prefix="!!")
    
    @bot.event
    async def on_ready():
        print("bot is ready!")
        try:
            await bot.tree.sync()
        except Exception as e:
            print("An error occurred while syncing: ", e)
            
    @bot.tree.command()
    async def setup(interaction: discord.Interaction,
                    intervals:int =  30, 
                    __show_subscriber:bool = True,
                    __show_view:bool = False,
                    __subscriber_channel:discord.VoiceChannel = None,
                    __view_channel:discord.VoiceChannel = None,
                    __category: discord.CategoryChannel = None ):
        global intervalsTime
        global subscriber_channel
        global view_channel
        global show_subscriber
        global show_view
        show_subscriber = __show_subscriber
        show_view = __show_view
        intervalsTime = intervals
        await interaction.response.send_message("執行中...")
        youtubeAPI.setup(YOUTUBEID)
        if __category == None:
            category = await guild.create_category("資料",overwrites={guild.default_role:discord.PermissionOverwrite(connect=False,view_channel=True)})
        else:
            category = __category
        if __show_subscriber :
            if __subscriber_channel == None:
                subscriber_channel =  await guild.create_voice_channel("訂閱數: None",category=category)
            else:
                subscriber_channel = __subscriber_channel
        if __show_view :
            if __subscriber_channel == None:
                view_channel = await guild.create_voice_channel("觀看數: None",category=category)
            else:
                view_channel = __view_channel
    
    async def request_function():
        global exit_flag
        global subscriberCount,viewCount
        subscriberCount = 0
        viewCount = 0
        while not exit_flag:
            request = youtubeAPI.request()
            new_subscriber_count = request[0]
            new_view_count = request[1]
            if new_subscriber_count != subscriberCount or new_view_count != viewCount:
                subscriberCount = new_subscriber_count
                viewCount = new_view_count
                print(subscriberCount)
                print(viewCount)
                await asyncio.gather(edit_channel(subscriberCount, viewCount))
            await asyncio.sleep(intervalsTime)

            
    async def edit_channel(subscriberCount,viewCount):
        if show_subscriber :
            await subscriber_channel.edit(name=f"訂閱數: {subscriberCount}")
        if show_view :
            await view_channel.edit(name=f"觀看數: {viewCount}")
    
   
            
    @bot.command(pass_context=True)
    async def getID(message: discord.Message) -> None:
        global guild
        guild = message.guild
        print(guild)
    
    @bot.hybrid_command()
    async def start_request(ctx):
        global exit_flag
        exit_flag = False
        global request_thread
        loop = asyncio.get_event_loop()
        request_thread = threading.Thread(target=lambda: loop.run_until_complete(request_function()))
        request_thread.start()
        await ctx.send("Start request",ephemeral = True) 
        asyncio.create_task(request_function())
        
        
    @bot.hybrid_command()
    async def end_request(ctx):
        global exit_flag
        exit_flag = True
        await ctx.send("end request",ephemeral = True)
        request_thread.join()
    
    
    bot.run(token=DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run() 