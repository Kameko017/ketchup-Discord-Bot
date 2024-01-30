from discord.ext import commands
from discord import app_commands
import discord
import time
import datetime 
from typing import Union

class Antispam (commands.Cog):
    def __init__(self,bot) :
        self.bot = bot
    
    whitelist_member_list = []    
    whitelist_chanmel_list = []    
    user_message_count = {}
    second = 1
    timed_out = 60
    count = 3
    reset_time = 6
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.message):
        # 检查用户是否在白名单中
        if message.author in self.whitelist_member_list or message.channel in self.whitelist_chanmel_list:
            return
        # 检查计数器中是否已经存在相同的消息
        user_id = message.author.id
        current_time = time.time()
        # >1 實際上要刷三次才會觸發!
        if user_id in self.user_message_count and current_time - self.user_message_count[user_id]['time'] < self.second and self.user_message_count[user_id]['count'] > self.count-2:
            # 封禁用户
            await message.author.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=self.timed_out))
            self.user_message_count[user_id] = {'message': message.content, 'time': current_time,'count':0}
            await message.channel.send(f'{message.author.mention} 已因刷頻被禁言 {self.timed_out} 分鐘, 如果有誤ban請私訊管理員')
            print(f"因刷頻已禁言{message.author.name}")
        elif not user_id in self.user_message_count or current_time - self.user_message_count[user_id]['time'] > self.reset_time:
            self.user_message_count[user_id] = {'message': message.content, 'time': current_time,'count':1}
        elif self.user_message_count[user_id]['message'] == message.content:
            self.user_message_count[user_id] = {'message': message.content, 'time': current_time,'count':int(self.user_message_count[user_id]['count'])+1}
            print(self.user_message_count[user_id]['count'])
            
        await self.bot.process_commands(message)
    @app_commands.command(name="設定防刷頻參數")
    @app_commands.rename(count="刷頻次數",second="幾秒內",timed_out = "禁言幾分鐘",reset_time="幾秒後重置計數時間")
    async def setup_antispam(self,interaction:discord.Interaction,count:int = 3,second:int = 1,timed_out:int = 60,reset_time:int = 6):
        self.timed_out = timed_out
        self.second = second
        self.count = count
        self.reset_time = reset_time
        await interaction.response.send_message("設置完成",ephemeral=True)
    
    @app_commands.command(name="防刷頻白名單人員")
    async def antispam_whitelist_member(self,interaction:discord.Interaction,member : discord.Member):
        self.whitelist_member_list.append(member)
        await interaction.response.send_message(f"已將{member.name}設置為白名單",ephemeral=True)
        
    @app_commands.command(name="防刷頻白名單頻道")
    async def antispam_whitelist_chanmel(self,interaction:discord.Interaction,channel : Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel]):
        self.whitelist_member_list.append(channel)
        await interaction.response.send_message(f"已將{channel.name}設置為白名單",ephemeral=True)
        
    
async def setup(bot):
    await bot.add_cog(Antispam(bot))