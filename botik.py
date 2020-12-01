import discord
import os
from discord.ext import commands
from discord import Activity, ActivityType

prefix="-"

client=commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print("Бот подключен")
    await client.change_presence(status = discord.Status.online, activity = Activity(name = 'за Arizona Squad', type = ActivityType.watching))

@client.command()
async def clear(ctx,amount:int=None):
    if amount is None:
        await ctx.send("**Необходимо ввести количество сообщений. Пример: -clear 10**")
    elif amount > 20:
        await ctx.send("**Нельзя очистить больше 20-ти сообщений за раз.**")
    else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        
token=os.environ.get('TOKEN')
client.run(str(token))
