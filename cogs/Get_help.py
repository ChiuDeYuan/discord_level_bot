import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Get_help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="get_help", description="i need help!",guild_ids=[1075946528021151744])
    async def get_help(self,interaction: nextcord.Interaction):
        member = interaction.user.mention
        await interaction.response.send_message(member+"\n\n取得段位流程:"+"```css\n"+"\n初次使用請先輸入/register [你在CodeForces的handle]\n用/get_task [你要的段位] 可得到題目\n\n目前有Newbie,Advanced,Competent,Expert,Master五種難度\n難度Newbie最低, Master最難\n每種難度分別有不同的作答時間\n會寫在作答說明上\n輸入/left可查詢剩餘時間\n\n每次的挑戰皆有三道題目\n做完題目後到CodeForces上submit並取得Accept後\n輸入/judge [你要judge的題目]\n才算完成其中一題\n作答順序不限\n\n記得做完一題就要先/judge它\n不然會判斷錯誤\n三題皆作答完成即可獲得相應段位\n\n輸入/give_up可放棄挑戰\n"+"```"+ "\n指令總表:"+"```"+"/get_help\n/register\n/get_task\n/left\n/give_up\n/judge"+"```"+"\n聯絡:"+"```css\n"+"ChiuChiuCircle#9802"+"```")

def setup(bot):
    bot.add_cog(Get_help(bot))
