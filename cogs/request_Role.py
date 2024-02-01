import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button,View,Modal,TextInput
from discord.utils import get
import traceback


class Request_Role(commands.Cog):
    def __init__(self,bot) :
        self.bot = bot
    @app_commands.command(name="申請權限")
    @app_commands.rename(role="權限")
    async def request(self,interaction:discord.Interaction,role:discord.Role):
        button = Button(label="我要申請!",style=discord.ButtonStyle.green)
        async def button_callback(interaction:discord.Interaction):
            print(f"申請{role.name}: 申請人:{interaction.user.name}, 原有身分組:{interaction.user.roles}")
            request_user = interaction.user
            
            agree_button = Button(label="同意",style=discord.ButtonStyle.green)
            async def agree_button_callback(interaction:discord.Interaction):
                administrator_role = get(interaction.guild.roles,name="管理員")
                if administrator_role in interaction.user.roles:
                    await request_user.add_roles(interaction.guild.get_role(role.id))
                    await interaction.response.edit_message(content="處理中...",delete_after=0.1)
                    await interaction.channel.send(f"{request_user.mention} 已獲得{role.name}身分組")
                else:
                    print(interaction.user.name,"不是管理員但點擊了同意")
                    await interaction.response.send_message("你不是管理員，請勿點擊!",ephemeral=True)
            agree_button.callback = agree_button_callback
            
            disagree_agree_button = Button(label="不同意",style=discord.ButtonStyle.red)
            async def disagree_button_callback(interaction:discord.Interaction):
                administrator_role = get(interaction.guild.roles,name="管理員")
                if administrator_role in interaction.user.roles:
                    class disagree_modal(Modal,title="不同意原因"):
                        disagree_reason = TextInput(label="原因:",style=discord.TextStyle.long,max_length=2000,)
                        async def on_submit(self, interaction: discord.Interaction):
                            await interaction.response.edit_message(content="處理中...",delete_after=0.1)
                            await request_user.send(f"## 聲請{role.name}遭拒絕! \n 原因: \n {self.disagree_reason}")
                        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
                            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
                            traceback.print_exception(type(error), error, error.__traceback__)
                    await interaction.response.send_modal(disagree_modal())
                else:
                    print(interaction.user.name,"不是管理員但點擊了同意")
                    await interaction.response.send_message("你不是管理員，請勿點擊!",ephemeral=True)
            disagree_agree_button.callback = disagree_button_callback
            
            agree_view = View(timeout=None)
            agree_view.add_item(agree_button)
            agree_view.add_item(disagree_agree_button)
            await interaction.response.send_message("通知管理員中...",delete_after=0.1,ephemeral=True)
            await interaction.channel.send(f"<@&1199388464450392114> 申請{role.name}身分組: {interaction.user.mention} (同意/不同意按鈕只限管理員，請勿亂點)",view=agree_view)
        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)
        await interaction.channel.send("",view = view)   
async def setup(bot):
    await bot.add_cog(Request_Role(bot))