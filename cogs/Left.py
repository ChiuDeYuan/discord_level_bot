import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Left(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="left", description="How much time i have?",guild_ids=[1075946528021151744])
    async def left(self,interaction: nextcord.Interaction):
        member = interaction.user.mention

        Register=self.bot.get_cog('Register')
        data=Register.data

        try:
            if(data[interaction.user.id]['state']=='yes'):
                await interaction.response.send_message(member+"\nYou have"+"```css\n"+data[interaction.user.id]['time']['timer']+"```"+" left.")

            else:
                await interaction.response.send_message(member+"\nYou are not challenging!")
        
        except:
            await interaction.response.send_message(member+"\nPlease register!")

def setup(bot):
    bot.add_cog(Left(bot))