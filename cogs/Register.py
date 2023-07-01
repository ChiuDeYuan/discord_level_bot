import nextcord
from nextcord import Interaction
from nextcord.ext import commands



class Register(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data=dict()

    @nextcord.slash_command(name="register", description="If you're using this bot for the first time, please register",guild_ids=[1075946528021151744])
    async def register(self, interaction: nextcord.Interaction, codeforces_handle:str, ):
        member=interaction.user.mention
        role_now='none'

        for r in interaction.user.roles:
            r=str(r)
            if(r.count("[段位]")):
                role_now=str(r)
                break
            

        info={
            
            'state':'none',
            'name_dc': str(interaction.user.name),
            'name_cf': codeforces_handle,
            'role_now':role_now,
            'role_task':'none',
            'time':{
            
            'total':int(0),
            'hour':int(0),
            'minute':int(0),
            'second':int(0),
            'timer':'{:2d}小時 {:02d}分 {:02d}秒'.format(0, 0, 0)
            
            },
            'task_contest':{

                'task1_ctt':0,
                'task2_ctt':0,
                'task3_ctt':0
            },
            'task_index':{

                'task1_idx':'none',
                'task2_idx':'none',
                'task3_idx':'none'

            },
            'task_verdict':{

                'task1_verdict':'no',
                'task2_verdict':'no',
                'task3_verdict':'no'

                }

        }

        self.data[interaction.user.id]={}
        self.data[interaction.user.id].update(info)
        await interaction.response.send_message(member+"\nRegister Successfully!")
    

def setup(bot):
    bot.add_cog(Register(bot))