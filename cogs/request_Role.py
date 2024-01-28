import discord
from discord.ext import commands
from discord.ui import Button,View
from discord.utils import get
import Setting


class Request_Role(commands.Cog):
    def __init__(self,bot) :
        self.bot = bot
        
    @commands.command(name="request_Youtuber")
    async def request_Youtuber(self, ctx):
        button = Button(label="我要申請!",style=discord.ButtonStyle.green,emoji="<:startled:1199670121787052162>")
        async def button_callback(interaction:discord.Interaction):
            print(f"申請Youtuber訊息: 申請人:{interaction.user.name}, 原有身分組:{interaction.user.roles}")
            request_user = interaction.user
            agree_button = Button(label="同意",style=discord.ButtonStyle.red)
            async def agree_button_callback(interaction:discord.Interaction):
                if get(interaction.guild.roles,id=1199388464450392114) in interaction.user.roles:
                    await request_user.add_roles(interaction.guild.get_role(1199392623509647521))
                    await interaction.response.edit_message(content="處理中...",delete_after=0.1)
                    await ctx.send(f"{request_user.mention} 已獲得YouTuber身分組")
                else:
                    print(interaction.user.name,"不是管理員但點擊了同意")
                    await interaction.response.send_message("你不是管理員，請勿點擊!",ephemeral=True)
            agree_button.callback = agree_button_callback
            agree_view = View()
            agree_view.add_item(agree_button)
            await interaction.response.send_message("通知管理員中...",delete_after=0.1)
            await ctx.send(f"<@&1199388464450392114> 申請Youtuber身分組: {interaction.user.mention}",view=agree_view,ephemeral=False)
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send("",view = view)    
    @commands.command(name="request_vtuber_or_vtype")
    async def request_vtuber_or_vtype(self, ctx):
        button = Button(label="我要申請!",style=discord.ButtonStyle.green,emoji="<:startled:1199670121787052162>")
        async def button_callback(interaction:discord.Interaction):
            print(f"申請Youtuber訊息: 申請人:{interaction.user.name}, 原有身分組:{interaction.user.roles}")
            request_user = interaction.user
            agree_button = Button(label="同意",style=discord.ButtonStyle.red)
            async def agree_button_callback(interaction:discord.Interaction):
                if get(interaction.guild.roles,id=1199388464450392114) in interaction.user.roles:
                    await request_user.add_roles(interaction.guild.get_role(1199392210030964897))
                    await interaction.response.edit_message(content="處理中...",delete_after=0.1)
                    await ctx.send(f"{request_user.mention} 已獲得vtuber/vtype身分組")
                else:
                    print(interaction.user.name,"不是管理員但點擊了同意")
                    await interaction.response.send_message("你不是管理員，請勿點擊!",ephemeral=True)
            agree_button.callback = agree_button_callback
            agree_view = View()
            agree_view.add_item(agree_button)
            await interaction.response.send_message("通知管理員中...",delete_after=0.1)
            await ctx.send(f"<@&1199388464450392114> 申請vtuber/vtype身分組: {interaction.user.mention}",view=agree_view)
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send("",view = view)    

async def setup(bot):
    await bot.add_cog(Request_Role(bot))