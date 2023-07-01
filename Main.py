import nextcord
from nextcord.ext import commands
import os
import keep_alive

TOKEN='token'

def main():

    intents = nextcord.Intents.all()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix="%", intents=intents)
    client = nextcord.Client()

    # ---------------------------------------------------------------------------
 
    @bot.event
    async def on_ready():
        print(f"目前登入身份 --> {bot.user}")
        ectivity = nextcord.Game('沒有國王的西洋棋')
        await client.change_presence(status=nextcord.Status.online, activity=ectivity)

    for fn in os.listdir("cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")

    @bot.command()
    async def load(ctx,extension):
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("loaded cog!")

    @bot.command()
    async def unload(ctx,extension):
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("unloaded cog!")

    @bot.command()
    async def reload(ctx,extension):
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send("reloaded cog!")

    keep_alive.keep_alive()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
