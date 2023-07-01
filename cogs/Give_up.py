import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Give_up(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="give_up", description="Never give you up.",guild_ids=[1075946528021151744])
    async def give_up(self,interaction: nextcord.Interaction):
        member = interaction.user.mention

        Register=self.bot.get_cog('Register')
        data=Register.data

        try:
            if(data[interaction.user.id]['state']=='no'):
                await interaction.response.send_message(member+"\nYou are not challenging!")
            
            else:
                await interaction.response.send_message(member+"\nSo sad ಥ_ಥ")
                data[interaction.user.id]['state']='no'

        except:
            await interaction.response.send_message(member+"\nPlease register!")

def setup(bot):
    bot.add_cog(Give_up(bot))