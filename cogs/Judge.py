import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord import SlashOption
import requests
import json


class Judge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="judge", description="judge!",guild_ids=[1075946528021151744])
    async def judge(self,interaction: nextcord.Interaction, arg: int=SlashOption(
            name="judge", description="Which task you'd like to judge",
            choices={"第一題":1, "第二題":2,"第三題":3},
        ),):
        member = interaction.user.mention

        Register=self.bot.get_cog('Register')
        data=Register.data

        try:
            if(data[interaction.user.id]['state']=='yes'):
                    
                judge_url="https://codeforces.com/api/user.status?handle="+data[interaction.user.id]['name_cf']+"&from=1&count=1"

                try:
                    judgeres = requests.get(judge_url)
                    judgejson=json.loads(judgeres.text)

                    if(judgejson['status']=="FAILED"):
                        await interaction.response.send_message(member+"\n"+judgejson['comment'])

                    elif(judgejson['status']=="OK"):
                        
                        judge_ctt="task"+str(arg)+"_ctt"
                        judge_idx="task"+str(arg)+"_idx"
                        judge_verdict="task"+str(arg)+"_verdict"
                        
                        for task in judgejson['result']:
                            if(str(task['problem'].get('contestId','0')) == str(data[interaction.user.id]['task_contest'][judge_ctt]) and str(task['problem'].get('index','none')) == str(data[interaction.user.id]['task_index'][judge_idx])):
                            

                                for result in judgejson['result']:
                                    if(str(result.get('verdict'))=="OK"):
                                    
                                        await interaction.response.send_message(member+"\nThe task is accepted!")
                                        data[interaction.user.id]['task_verdict'][judge_verdict]='ok'

                                    else:
                                        await interaction.response.send_message(member+"\nU got the wrong AnsW3r!\nTry again")

                                    
                                if(data[interaction.user.id]['task_verdict']['task1_verdict']=='ok' and data[interaction.user.id]['task_verdict']['task2_verdict']=='ok' and data[interaction.user.id]['task_verdict']['task3_verdict']=='ok'):
                                    
                                    await interaction.followup.send(member+"\nCongratulation!\n\nNow You r the member of:\n"+"```css\n"+data[interaction.user.id]['role_task']+"```")
                                    
                                    role = nextcord.utils.get(interaction.guild.roles, name=data[interaction.user.id]['role_now'])
                                    await interaction.user.remove_roles(role)
                                    
                                    role=nextcord.utils.get(interaction.guild.roles, name=data[interaction.user.id]['role_task'])
                                    await interaction.user.add_roles(role)

                                    data[interaction.user.id]['role_now']=data[interaction.user.id]['role_task']
                                    data[interaction.user.id]['role_task']='none'
                                    data[interaction.user.id]['state']='no'
    
                            else:
                                await interaction.response.send_message(member+"\nPlease submit or re-submit on CodeForces!")
                            
                            
                except:
                    await interaction.response.send_message(member+"\nSomething went wrong...ಥ_ಥ\nPlease wait a minutes")

            else:
                
                await interaction.response.send_message(member+"\nYou are not challenging!")
        
        except:
            await interaction.response.send_message(member+"\nPlease register!")

def setup(bot):
    bot.add_cog(Judge(bot))