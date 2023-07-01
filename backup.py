'''

import keep_alive
import os
import nextcord
import requests
import json
import random
import time
import ast
import asyncio
from nextcord import Interaction, SlashOption, ChannelType

intents = nextcord.Intents.all()
client = nextcord.Client()

TOKEN = os.environ['段位bot2.0']
guild_id=1075946528021151744

def writedict(write_dict):
    with open("./user_data.txt","w+") as data_write:
        data_write.write(str(write_dict))

def readdict():
    with open("./user_data.txt","r") as data_read:
        d=ast.literal_eval(data_read.read())
        return d
      
problem_url="https://codeforces.com/api/problemset.problems?tags=implementation"
res = requests.get(problem_url)
resjson=json.loads(res.text)

problemset=[[],[],[],[],[]]

for i in resjson['result']['problems'] :
    if(0<int(i.get('rating','0'))<=1199):
        problemset[0].append([i.get('contestId'),i.get('index')])
    elif(1199<int(i.get('rating','0'))<=1699):
        problemset[1].append([i.get('contestId'),i.get('index')])
    elif(1699<int(i.get('rating','0'))<=2299):
        problemset[2].append([i.get('contestId'),i.get('index')])
    elif(2299<int(i.get('rating','0'))<=2899):
        problemset[3].append([i.get('contestId'),i.get('index')]) 
    elif(2899<int(i.get('rating','0'))):
        problemset[4].append([i.get('contestId'),i.get('index')]) 
      
@client.event
async def on_ready():
    print(f"目前登入身份 --> {client.user}")
    ectivity = nextcord.Game('正在比薩斜塔上跟袋熊下沒有國王的西洋棋')
    await client.change_presence(status=nextcord.Status.online, activity=ectivity)

data=dict()
@client.slash_command(name="register", description="If you're using this bot for the first time, please register",guild_ids=[guild_id])
async def register(interaction: nextcord.Interaction, codeforces_handle:str):
    
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

    data[interaction.user.id]={}
    data[interaction.user.id].update(info)
    writedict(data)
    await interaction.response.send_message(member+"\nRegister Successfully!")


@client.slash_command(name="get_task", description="Enter what Level you'd like to challenge",guild_ids=[guild_id])
async def get_task(interaction: nextcord.Interaction, arg: str = SlashOption(
        name="choose", description="Choose a Level you'd like to challenge",
        choices={"Newbie":"Newbie", "Advanced": "Advanced","Competent":"Competent","Expert":"Expert","Master":"Master"},
    ),):

    member = interaction.user.mention

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


@client.slash_command(name="give_up", description="Never give you up.",guild_ids=[guild_id])
async def give_up(interaction: nextcord.Interaction):
    member = interaction.user.mention
    try:
        if(data[interaction.user.id]['state']=='no'):
            await interaction.response.send_message(member+"\nYou are not challenging!")
        
        else:
            await interaction.response.send_message(member+"\nSo sad ಥ_ಥ")
            data[interaction.user.id]['state']='no'

    except:
        await interaction.response.send_message(member+"\nPlease register!")




@client.slash_command(name="left", description="How much time i have?",guild_ids=[guild_id])
async def left(interaction: nextcord.Interaction):
    member = interaction.user.mention
    try:
        if(data[interaction.user.id]['state']=='yes'):
            await interaction.response.send_message(member+"\nYou have"+"```css\n"+data[interaction.user.id]['time']['timer']+"```"+" left.")

        else:
            await interaction.response.send_message(member+"\nYou are not challenging!")
    
    except:
        await interaction.response.send_message(member+"\nPlease register!")





@client.slash_command(name="judge", description="judge!",guild_ids=[guild_id])
async def judge(interaction: nextcord.Interaction, arg: int=SlashOption(
        name="judge", description="Which task you'd like to judge",
        choices={"第一題":1, "第二題":2,"第三題":3},
    ),):
    member = interaction.user.mention
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
                                    if(str(result.get('verdict'))=="yes"):
                                    
                                        await interaction.response.send_message(member+"Your task: "+arg+"\nis accept!")
                                        data[interaction.user.id]['task_verdict'][judge_verdict]='ok'
                                    
                                    else:
                                        await interaction.response.send_message(member+"\nU got the wrong AnsW3r!\nTry again")

                                    
                                if(data[interaction.user.id]['task_verdict']['task1_verdict']=='ok' and data[interaction.user.id]['task_verdict']['task2_verdict']=='ok' and data[interaction.user.id]['task_verdict']['task3_verdict']=='ok'):
                                    role = nextcord.utils.get(interaction.user.roles, name=data[interaction.user.id]['role_now'])
                                    await interaction.user.remove_roles(role)
                                    role=nextcord.utils.get(interaction.user.roles, name=data[interaction.user.id]['role_task'])
                                    await interaction.user.add_roles(role)
                                
                                    await interaction.response.send_message(member+"\nCongratulation!\n\nNow You r the member of:\n"+"```css\n"+data[interaction.user.id]['role_task']+"```")
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



@client.slash_command(name="get_help", description="i need help!",guild_ids=[guild_id])
async def get_help(interaction: nextcord.Interaction):
    member = interaction.user.mention
    await interaction.response.send_message(member+"\n\n取得段位流程:"+"```css\n"+"\n初次使用請先輸入/register [你在CodeForces的handle]\n用/get_task [你要的段位] 可得到題目\n\n目前有Newbie,Advanced,Competent,Expert,Master五種難度\n難度Newbie最低, Master最難\n每種難度分別有不同的作答時間\n會寫在作答說明上\n輸入/left可查詢剩餘時間\n\n每次的挑戰皆有三道題目\n做完題目後到CodeForces上submit並取得Accept後\n輸入/judge [你要judge的題目]\n才算完成其中一題\n作答順序不限\n\n記得做完一題就要先/judge它\n不然會判斷錯誤\n三題皆作答完成即可獲得相應段位\n\n輸入/give_up可放棄挑戰\n"+"```"+ "\n指令總表:"+"```"+"/get_help\n/register\n/get_task\n/left\n/give_up\n/judge"+"```"+"\n聯絡:"+"```css\n"+"ChiuChiuCircle#9802"+"```")

keep_alive.keep_alive()
client.run(TOKEN)

'''