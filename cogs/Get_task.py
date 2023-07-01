import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord import SlashOption
import random
import asyncio

class Get_task(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="get_task", description="Enter what Level you'd like to challenge",guild_ids=[1075946528021151744])
    async def get_task(self,interaction: nextcord.Interaction, arg: str = SlashOption(name="choose", description="Choose a Level you'd like to challenge",choices={"Newbie":"Newbie", "Advanced": "Advanced","Competent":"Competent","Expert":"Expert","Master":"Master"},),):
        
        member = interaction.user.mention

        Register=self.bot.get_cog('Register')
        data=Register.data

        Problemset=self.bot.get_cog('Problemset')
        problemset=Problemset.problemset
        
        try:
            data[interaction.user.id]['role_task']="[段位]"+arg
            data[interaction.user.id]['state']='yes'
                
            if(arg=="Newbie"):   idx_task=0
            elif(arg=="Advanced"):   idx_task=1
            elif(arg=="Competent"):   idx_task=2
            elif(arg=="Expert"):   idx_task=3
            elif(arg=="Master"):   idx_task=4

            data[interaction.user.id]['time']['total']=int((idx_task+1)*3600)

            if(data[interaction.user.id]['state']=='yes'):

                idx_problem1=random.randint(0,5000)%len(problemset[idx_task])
                idx_problem2=random.randint(0,5000)%len(problemset[idx_task])
                idx_problem3=random.randint(0,5000)%len(problemset[idx_task])
                await interaction.response.send_message(member+"\nChallenge level: "+data[interaction.user.id]['role_task']+"\nHere are your tasks:\n\n1:https://codeforces.com/problemset/problem/"+str(problemset[idx_task][idx_problem1][0])+"/"+str(problemset[idx_task][idx_problem1][1])+"\n2:https://codeforces.com/problemset/problem/"+str(problemset[idx_task][idx_problem2][0])+"/"+str(problemset[idx_task][idx_problem2][1])+"\n3:https://codeforces.com/problemset/problem/"+str(problemset[idx_task][idx_problem3][0])+"/"+str(problemset[idx_task][idx_problem3][1])+"\n```css\n"+"作答方式說明:\n\n共有"+str(idx_task+1)+"小時答題時間\n輸入%left可查詢剩餘時間\n\n每次的挑戰皆有三道題目\n做完題目後到CodeForces上submit並取得Accept後\n輸入\"/judge [選擇你要judge的題目]\"\n才算完成其中一題\n作答順序不限\n\n記得做完一題就要先/judge它\n不然會判斷錯誤\n三題皆作答完成即可獲得相應段位\n\n輸入/give_up可放棄挑戰\n更多資訊請輸入/get_help"+"```")

                data[interaction.user.id]['task_contest']['task1_ctt']=str(problemset[idx_task][idx_problem1][0])
                data[interaction.user.id]['task_contest']['task2_ctt']=str(problemset[idx_task][idx_problem2][0])
                data[interaction.user.id]['task_contest']['task3_ctt']=str(problemset[idx_task][idx_problem3][0])
                data[interaction.user.id]['task_index']['task1_idx']=str(problemset[idx_task][idx_problem1][1])
                data[interaction.user.id]['task_index']['task2_idx']=str(problemset[idx_task][idx_problem2][1])
                data[interaction.user.id]['task_index']['task3_idx']=str(problemset[idx_task][idx_problem3][1])
                data[interaction.user.id]['task_verdict']['task1_verdict']='no'
                data[interaction.user.id]['task_verdict']['task2_verdict']='no'
                data[interaction.user.id]['task_verdict']['task3_verdict']='no'

                while(data[interaction.user.id]['time']['total'] and data[interaction.user.id]['state']=='yes'):
                    data[interaction.user.id]['time']['hour'], data[interaction.user.id]['time']['minute']=divmod(data[interaction.user.id]['time']['total'], 3600)
                    data[interaction.user.id]['time']['minute'], data[interaction.user.id]['time']['second'] = divmod(data[interaction.user.id]['time']['minute'], 60)
                    data[interaction.user.id]['time']['timer'] = '{:2d}小時 {:02d}分 {:02d}秒'.format(data[interaction.user.id]['time']['hour'],data[interaction.user.id]['time']['minute'] , data[interaction.user.id]['time']['second'])
                    await asyncio.sleep(1)
                    data[interaction.user.id]['time']['total']-= 1

                if(data[interaction.user.id]['time']['total']==0):  
                    await interaction.followup.send(member+"\nTime's up!\nU FaiLeD.\nTry again")
                    data[interaction.user.id]['state']='no'

        except:
            await interaction.response.send_message(member+"\nPlease register!")

def setup(bot):
    bot.add_cog(Get_task(bot))