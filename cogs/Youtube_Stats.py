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
    
    @app_commands.command()
    @app_commands.guilds(int(Setting.GUILD_ID))
    async def setup_stats(self,
                    interaction_parameter: discord.Interaction,
                    intervals_parameter:int, 
                    show_subscriber_parameter:bool = True,
                    show_view_parameter:bool = False,
                    subscriber_channel_parameter:discord.VoiceChannel = None,
                    view_channel_parameter:discord.VoiceChannel = None,
                    category_parameter: discord.CategoryChannel = None ):
        global subscriber_channel
        global view_channel
        global show_subscriber
        global show_view
        show_subscriber = show_subscriber_parameter
        show_view = show_view_parameter
        self.intervalsTime = intervals_parameter
        await interaction_parameter.response.send_message("執行中...",ephemeral=True)
        youtubeAPI.setup(Setting.YOUTUBE_ID)
        if category_parameter is None:
            category = await Setting.guild.create_category("資料", overwrites={Setting.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)})
        else:
            category = category_parameter
        if show_subscriber_parameter:
            if subscriber_channel_parameter is None:
                subscriber_channel = await Setting.guild.create_voice_channel("訂閱數: None", category=category)
            else:
                subscriber_channel = subscriber_channel_parameter
        if show_view_parameter:
            if subscriber_channel_parameter is None:
                view_channel = await Setting.guild.create_voice_channel("觀看數: None", category=category)
            else:
                view_channel = view_channel_parameter
        await interaction_parameter.followup.send("設置完成！",ephemeral = True)
    
        
    @tasks.loop(seconds=intervalsTime)
    async def request_function(self):
        global subscriberCount,viewCount
        request = youtubeAPI.request()
        new_subscriber_count = request[0]
        new_view_count = request[1]
        if new_subscriber_count != subscriberCount or new_view_count != viewCount:
            print (time.asctime( time.localtime(time.time()) ))
            print(f"subscriber:{new_subscriber_count} ,view:{new_view_count}   (old:subscriber:{subscriberCount} ,view:{viewCount})")
            subscriberCount = new_subscriber_count
            viewCount = new_view_count
            
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

    
    