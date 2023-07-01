import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import json
import requests


class Problemset(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.problemset=[[],[],[],[],[]]

        problem_url="https://codeforces.com/api/problemset.problems?tags=implementation"
        res = requests.get(problem_url)
        resjson=json.loads(res.text)
        for i in resjson['result']['problems'] :
            if(0<int(i.get('rating','0'))<=1199):
                self.problemset[0].append([i.get('contestId'),i.get('index')])
            elif(1199<int(i.get('rating','0'))<=1699):
                self.problemset[1].append([i.get('contestId'),i.get('index')])
            elif(1699<int(i.get('rating','0'))<=2299):
                self.problemset[2].append([i.get('contestId'),i.get('index')])
            elif(2299<int(i.get('rating','0'))<=2899):
                self.problemset[3].append([i.get('contestId'),i.get('index')]) 
            elif(2899<int(i.get('rating','0'))):
                self.problemset[4].append([i.get('contestId'),i.get('index')]) 

def setup(bot):
    bot.add_cog(Problemset(bot))