import discord
import os
from discord.ext import commands
from discord import Activity, ActivityType
from discord.utils import get

prefix="-"

client=commands.Bot(command_prefix=prefix)
client.remove_command('help')

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

@client.command()
async def help(ctx):
    emb=discord.Embed(title='Список команд бота "Izya":',description=f'**-help - информация о командах.\n-clear - очистить сообщения в чате.**', color=0xf47fff, timestamp=ctx.message.created_at)
    await ctx.send(embed=emb)

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Izya присоединился к каналу.')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Izya отключился от канала.')

token=os.environ.get('TOKEN')
client.run(str(token))
