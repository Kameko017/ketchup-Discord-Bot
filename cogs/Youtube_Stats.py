import discord
from discord import app_commands
from discord.ext import commands,tasks
import youtubeAPI
import Setting
import time

class YoutubeStats(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    intervalsTime = 60
    subscriber_channel : discord.VoiceChannel
    view_channel : discord.VoiceChannel
    show_subscriber = True
    subscriberCount,viewCount = 0,0
    old_subscriberCount,old_viewCount = 0,0
    show_view  = True
    
    @app_commands.command(name="設置youyube狀態")
    @app_commands.describe(subscriber_channel_name="ex. \" 訂閱數: \"",view_channel_name="ex. \" 觀看數: \"")
    @app_commands.rename(intervals_parameter="間隔時間",youtube_id="頻道id",show_subscriber_parameter="是否顯示訂閱數",show_view_parameter="是否顯示觀看數",subscriber_channel_parameter="訂閱數頻道",view_channel_parameter="觀看數頻道",subscriber_channel_name="訂閱數頻道名字",view_channel_name = "觀看數頻道名字")
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
        self.show_subscriber = show_subscriber_parameter
        self.show_view = show_view_parameter
        self.intervalsTime = intervals_parameter
        await interaction_parameter.response.send_message("執行中...",ephemeral=True)
        youtubeAPI.setup(youtube_id)
        if show_subscriber_parameter:
            if subscriber_channel_parameter is None:
                self.subscriber_channel = await Setting.guild.create_voice_channel(f"{subscriber_channel_name}0")
            else:
                self.subscriber_channel = subscriber_channel_parameter
        if show_view_parameter:
            if subscriber_channel_parameter is None:
                self.view_channel = await Setting.guild.create_voice_channel(f"{view_channel_name}: 0")
            else:
                self.view_channel = view_channel_parameter
        if subscriber_channel_parameter.category is None or view_channel_parameter.category is None:
            category = await Setting.guild.create_category("資料", overwrites={Setting.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)})
            await self.subscriber_channel.edit(category=category)
            await self.view_channel.edit(category=category)
        await interaction_parameter.followup.send("設置完成！",ephemeral = True)
       
    @tasks.loop(seconds=intervalsTime)
    async def request_function(self):
        request = youtubeAPI.request()
        new_subscriber_count = request[0]
        new_view_count = request[1]
        if (new_subscriber_count != self.subscriberCount or new_view_count != self.viewCount) and (new_subscriber_count !=  self.old_subscriberCount or new_view_count != self.old_viewCount):
            print (time.asctime( time.localtime(time.time()) ))
            print(f"subscriber:{new_subscriber_count} ,view:{new_view_count}   (original:subscriber:{self.subscriberCount} ,view:{self.viewCount}) (old:{self.old_subscriberCount},last_viewCount:{self.old_viewCount})")
            self.old_subscriberCount,self.old_viewCount = self.subscriberCount,self.viewCount
            self.subscriberCount,self.viewCount = new_subscriber_count,new_view_count
            
            if self.show_subscriber :
                await self.subscriber_channel.edit(name=f"訂閱數: {self.subscriberCount}")
            if self.show_view :
                await self.view_channel.edit(name=f"觀看數: {self.viewCount}")
            
    @app_commands.command(name="開始更新youyube狀態")
    async def start_request(self,interaction: discord.Interaction):
        if self.subscriber_channel == None:
            await interaction.response.send_message("尚未設置, 請使用 /設置youyube狀態 指令後再開啟更新",ephemeral = True)
            return
        self.request_function.start()
        await interaction.response.send_message("Start!",ephemeral = True)
    @app_commands.command(name="停止更新youtube狀態")
    async def end_request(self,interaction: discord.Interaction): 
        self.request_function.stop()
        await interaction.response.send_message("Stop!",ephemeral = True)
    
async def setup(bot):
    await bot.add_cog(YoutubeStats(bot))

    
    