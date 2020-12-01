import discord
import os
from discord.ext import commands
from discord import Activity, ActivityType

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
    emb=discord.Embed(title='Список команд Izya:',description=f'**-clear - очистить чат\n-help - информация о командах**', color=0xf47fff, timestamp=ctx.message.created_at)
    emb.set_footer(text=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    emb.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    emb.add_field(name='cooper',value="ya123",inline=False)
    emb.set_image(url=ctx.author.avatar_url)
    emb.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
        
token=os.environ.get('TOKEN')
client.run(str(token))
