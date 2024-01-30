import discord
from discord import app_commands
from discord.ext import commands,tasks
import youtubeAPI
import Setting
import time

class YoutubeStats(commands.Cog):
    global intervalsTime
    intervalsTime = 60
    
    global subscriberCount,viewCount
    subscriberCount = 0
    viewCount = 0
    
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="設置狀態")
    @app_commands.describe(subscriber_channel_name="ex. \" 訂閱數: \"",view_channel_name="ex. \" 觀看數: \"")
    @app_commands.rename(intervals_parameter="間隔時間",youtube_id="頻道id",show_subscriber_parameter="顯示訂閱數",show_view_parameter="顯示觀看數",subscriber_channel_parameter="顯示訂閱數頻道",view_channel_parameter="顯示觀看數頻道",subscriber_channel_name="訂閱數頻道名字",view_channel_name = "觀看數頻道名字")
    async def setup_stats(self,
                    interaction_parameter: discord.Interaction,
                    intervals_parameter:int, 
                    youtube_id:str,
                    subscriber_channel_parameter:discord.VoiceChannel = None,
                    view_channel_parameter:discord.VoiceChannel = None,
                    show_subscriber_parameter:bool = True,
                    show_view_parameter:bool = True,
                    subscriber_channel_name:str = "訂閱數: ",
                    view_channel_name:str = "觀看數: "):
        global subscriber_channel
        global view_channel
        global show_subscriber
        global show_view
        show_subscriber = show_subscriber_parameter
        show_view = show_view_parameter
        self.intervalsTime = intervals_parameter
        await interaction_parameter.response.send_message("執行中...",ephemeral=True)
        youtubeAPI.setup(youtube_id)
        if subscriber_channel_parameter.category is None:
            category = await Setting.guild.create_category("資料", overwrites={Setting.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)})
        else:
            category = subscriber_channel_parameter.category
        if show_subscriber_parameter:
            if subscriber_channel_parameter is None:
                subscriber_channel = await Setting.guild.create_voice_channel(f"{subscriber_channel_name}0", category=category)
            else:
                subscriber_channel = subscriber_channel_parameter
        if show_view_parameter:
            if subscriber_channel_parameter is None:
                view_channel = await Setting.guild.create_voice_channel(f"{view_channel_name}: 0", category=category)
            else:
                view_channel = view_channel_parameter
        await interaction_parameter.followup.send("設置完成！",ephemeral = True)
       
    @tasks.loop(seconds=intervalsTime)
    async def request_function(self):
        global subscriberCount,viewCount
        last_subscriberCount,last_viewCount = 0,0
        request = youtubeAPI.request()
        new_subscriber_count = request[0]
        new_view_count = request[1]
        if (new_subscriber_count != subscriberCount or new_view_count != viewCount) and (last_subscriberCount != subscriberCount or last_viewCount != new_subscriber_count):
            print (time.asctime( time.localtime(time.time()) ))
            print(f"subscriber:{new_subscriber_count} ,view:{new_view_count}   (old:subscriber:{subscriberCount} ,view:{viewCount}) (last_subscriberCount:{last_subscriberCount},last_viewCount:{last_viewCount})")
            last_subscriberCount,last_viewCount = subscriberCount,viewCount
            subscriberCount,viewCount = new_subscriber_count,new_view_count
            
            if show_subscriber :
                await subscriber_channel.edit(name=f"訂閱數: {subscriberCount}")
            if show_view :
                await view_channel.edit(name=f"觀看數: {viewCount}")
            
    @app_commands.command()
    async def start_request(self,interaction: discord.Interaction):
        self.request_function.start()
        await interaction.response.send_message("Start!",ephemeral = True)
    @app_commands.command()
    async def end_request(self,interaction: discord.Interaction): 
        self.request_function.stop()
        await interaction.response.send_message("Stop!",ephemeral = True)
    
async def setup(bot):
    await bot.add_cog(YoutubeStats(bot))

    
    