import discord
import discord.ext
from discord.ext import commands
import datetime
from datetime import timezone, tzinfo, timedelta
from time import sleep
import time as timeModule
from discord import Activity, ActivityType
from discord.utils import get
import os
import asyncio
from discord import Member
from discord import ChannelType
from discord.ext.commands.cooldowns import BucketType
import random
from random import randint
from pymongo import MongoClient
prefix="-"

client=commands.Bot(command_prefix=prefix, intents = discord.Intents.all())
client.remove_command('help')

claster=MongoClient('mongodb+srv://Izya:Qn0vTnfdj6lUCwdT@cluster0.affa1.mongodb.net/izyadb?retryWrites=true&w=majority')
coll=claster.izyadb.izyacoll

@client.event
async def on_ready():
    print("Бот подключен")
    await client.change_presence(status = discord.Status.online, activity = Activity(name = 'за AS & ERP', type = ActivityType.watching))
    for guild in client.guilds:
        post={
            '_id': guild.id,
            'role_id': 0,
            'name': guild.name
        }
        if coll.count_documents({"_id": guild.id}) == 0:
            coll.insert_one(post)
        
@client.event
async def on_member_join(member):
    channel = client.get_channel(699589471527764049)
    await channel.send('hello')

@client.event
async def on_guild_join(guild):
    mute = {
        "_id": guild.id,
        "name": guild.name,
        "role_id": 0
    }
    if coll.count_documents({"_id": guild.id}) == 0:
        coll.insert_one(mute)

@client.event
async def on_guild_role_delete(role):
    rol = coll.find_one({"_id": role.guild.id})["role_id"]
    if role.id == rol:
        coll.update_one({"_id": role.guild.id}, {"$set": {"role_id": 0}})
    else:
        return

#Mute
@client.command()
@discord.ext.commands.has_permissions(view_audit_log = True)
async def mute(ctx, member: discord.Member, time: int, *, reason):
    r_id = coll.find_one({"_id": ctx.guild.id})["role_id"]
    if r_id == 0:
        perm = discord.Permissions(change_nickname = True, read_messages = True, view_channel = True, send_messages = False, send_tts_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = False, stream = True, use_voice_activation = True)
        mute_role = await ctx.guild.create_role(name = 'Muted', permissions = perm, colour = discord.Colour(0x9b0b55))
        coll.update_one({"_id": ctx.guild.id}, {"$set": {"role_id": mute_role.id}})
        e = discord.Embed(timestamp = ctx.message.created_at, color = 0x4e6100, description = f'**💻 Модератор _{ctx.author.mention}_  выдал блокировку голосового/текстового чата пользователю _{member.mention}_ на {time} мин. Причинa: {reason}**')
        e.set_author(name = f'{ctx.guild.name} | Muted ⛔', icon_url = ctx.guild.icon_url)
        e.set_footer(text = 'Izya Bot ©️ 2020')
        await ctx.send(embed = e)
        await member.add_roles(mute_role, reason = f'Muted by {ctx.message.author.display_name}')
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak = False, add_reactions = False)
        await asyncio.sleep(time * 60)
        await member.remove_roles(mute_role, reason = f'Auto Unmute')
    else:
        role = coll.find_one({"_id": ctx.guild.id})["role_id"]
        mute_role1 = discord.utils.get(ctx.guild.roles, id = role)
        e1 = discord.Embed(timestamp = ctx.message.created_at, color = 0x4e6100, description = f'**💻 Модератор _{ctx.author.mention}_  выдал блокировку голосового/текстового чата пользователю _{member.mention}_ на {time} мин. Причинa: {reason}**')
        e1.set_author(name = f'{ctx.guild.name} | Muted ⛔', icon_url = ctx.guild.icon_url)
        e1.set_footer(text = 'Izya Bot ©️ 2020')
        await ctx.send(embed = e1)
        await member.add_roles(mute_role1, reason = f'Muted by {ctx.message.author.display_name}')
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role1, send_messages=False, speak = False, add_reactions = False)
        await asyncio.sleep(time * 60)
        await member.remove_roles(mute_role1, reason = f'Auto Unmute')

@client.command()
@discord.ext.commands.has_permissions(view_audit_log = True)
async def unmute(ctx, member:discord.Member):
    role = coll.find_one({"_id": ctx.guild.id})["role_id"]
    rol = discord.utils.get(ctx.guild.roles,id=role)
    if rol in member.roles:
        await ctx.channel.purge(limit = 1)
        mute_role = discord.utils.get(ctx.guild.roles, id = role) 
        await member.add_roles(mute_role)
        emb = discord.Embed(color = 0x479114, timestamp = ctx.message.created_at, description = f"**💻 Модератор _{ctx.author.mention}_ снял блокировку голосового/текстового чата пользователю _{member.mention}_ **")
        emb.set_author(name = f'{ctx.guild.name} | Unmuted ✅', icon_url = ctx.guild.icon_url)
        emb.set_footer(text = 'Izya Bot ©️ 2020')
        await ctx.send(embed = emb)
        await member.remove_roles(mute_role, reason = f'Unmuted by {ctx.message.author.display_name}')
    else:
        await ctx.send('**Пользователь не заглушен.**')       

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
    emb=discord.Embed(title='Список команд бота "Izya":',description=f'**-help - информация о командах.\n-clear - очистить сообщения в чате.\n-mute - блокировка текстового/голосового чата. (-mute @упоминание время причина)**', color=0xf47fff, timestamp=ctx.message.created_at)
    await ctx.send(embed=emb)
    
token=os.environ.get('TOKEN')
client.run(str(token))
