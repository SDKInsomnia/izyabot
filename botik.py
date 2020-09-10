import discord
import os
from discord.ext import commands
from discord import Activity, ActivityType

client=commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print( 'Izya подключен' )
    await client.change_presence(status = discord.Status.online, activity = Activity(name = 'работу', type = ActivityType.playing))

@client.command()
async def hello(ctx):
    emb=discord.Embed(title='opisanie',description=f'**Privet, {ctx.author.display_name}**', color=0xf47fff, timestamp=ctx.message.created_at)
    emb.set_footer(text=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    emb.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    emb.add_field(name='cooper',value="ya123",inline=False)
    emb.set_image(url=ctx.author.avatar_url)
    emb.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@client.command()
async def magic(ctx):
    e=discord.Embed()
    e.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=e)

@client.command()
async def cc(ctx,amount:int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@client.event
async def on_message(message):
    if message.author.premium_since:
        await message.add_reaction('<:booster:750658847634358383>')

token=os.environ.get('TOKEN')
client.run(str(token))
