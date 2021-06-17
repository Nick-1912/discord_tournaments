import discord
from discord.ext import commands
from cfg import config
import asyncio
import data_methods


async def timer(sec, ctx, channel, role, role_result_id):
    await asyncio.sleep(sec)
    await channel.purge(limit=1000)
    try:
        await ctx.author.remove_roles(role)
        result = data_methods.start_method(name='get: user_id',
                                           user_id=ctx.author.id)
        if result['auth'] == '1':
            data_methods.start_method(name='edit: del',
                                      user_id=ctx.author.id)
        elif result['auth'] == '2':
            await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=778995970221932555))
            return
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=role_result_id))
    except:
        return


bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())


@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, id=778994811457110026))


@bot.command(pass_context=True)
@commands.has_role(778994811457110026)
async def auth(ctx):
    auth_rooms = [
        bot.get_channel(783630534504218674), bot.get_channel(783630011470184448),
        bot.get_channel(783630064960667668), bot.get_channel(783630105142099978)
        # bot.get_channel(783630150649774101), bot.get_channel(783630332971843614),
        # bot.get_channel(783630359962845205), bot.get_channel(783630406166773770),
        # bot.get_channel(783630435598073896), bot.get_channel(783630465521156096)
    ]
    auth_roles = [
        discord.utils.get(ctx.author.guild.roles, id=783630647561420850),
        discord.utils.get(ctx.author.guild.roles, id=783630789068849153),
        discord.utils.get(ctx.author.guild.roles, id=783630869360410625),
        discord.utils.get(ctx.author.guild.roles, id=783630902302474250)
        # discord.utils.get(ctx.author.guild.roles, id=783630956972081193),
        # discord.utils.get(ctx.author.guild.roles, id=783630980362534952),
        # discord.utils.get(ctx.author.guild.roles, id=783631005344858112),
        # discord.utils.get(ctx.author.guild.roles, id=783631029259730944),
        # discord.utils.get(ctx.author.guild.roles, id=783631047102562316),
        # discord.utils.get(ctx.author.guild.roles, id=783631066417332255)
    ]
    temp = 0
    for auth_room in auth_rooms:
        if len(auth_room.members) == 2:
            await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=778994811457110026))
            await ctx.author.add_roles(auth_roles[temp])
            # bot.loop.create_task(room_timer(sec=300, ctx=ctx, role=auth_roles[temp], role_result=778994811457110026))
            await timer(sec=300, ctx=ctx, channel=auth_room, role=auth_roles[temp], role_result_id=778994811457110026)
            break
        temp += 1


@bot.command(pass_context=True)
@commands.has_role(778994811457110026)
async def reg(ctx):
    auth_rooms = [
        # bot.get_channel(783630534504218674), bot.get_channel(783630011470184448),
        # bot.get_channel(783630064960667668), bot.get_channel(783630105142099978),
        bot.get_channel(783630150649774101), bot.get_channel(783630332971843614),
        bot.get_channel(783630359962845205), bot.get_channel(783630406166773770),
        bot.get_channel(783630435598073896), bot.get_channel(783630465521156096)
    ]
    auth_roles = [
        # discord.utils.get(ctx.author.guild.roles, id=783630647561420850),
        # discord.utils.get(ctx.author.guild.roles, id=783630789068849153),
        # discord.utils.get(ctx.author.guild.roles, id=783630869360410625),
        # discord.utils.get(ctx.author.guild.roles, id=783630902302474250),
        discord.utils.get(ctx.author.guild.roles, id=783630956972081193),
        discord.utils.get(ctx.author.guild.roles, id=783630980362534952),
        discord.utils.get(ctx.author.guild.roles, id=783631005344858112),
        discord.utils.get(ctx.author.guild.roles, id=783631029259730944),
        discord.utils.get(ctx.author.guild.roles, id=783631047102562316),
        discord.utils.get(ctx.author.guild.roles, id=783631066417332255)
    ]
    temp = 0
    for auth_room in auth_rooms:
        if len(auth_room.members) == 2:
            await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=778994811457110026))
            await ctx.author.add_roles(auth_roles[temp])
            # bot.loop.create_task(room_timer(sec=600, ctx=ctx, role=auth_roles[temp], role_result=778994811457110026))
            await timer(sec=300, ctx=ctx, channel=auth_room, role=auth_roles[temp], role_result_id=778994811457110026)
            break
        temp += 1


# login room 0
@bot.command(pass_context=True)
@commands.has_role(783630647561420850)
async def login(ctx, nickname=None, password=None):
    if not (nickname and password):
        await ctx.send('[login] Ошибка запроса не ввели данные... Попробуйте еще раз')
        return
    result = data_methods.start_method(name='get: user_id',
                                       user_id=ctx.author.id)
    if not result:
        await ctx.send('[login] Вы не зарегистрированы!')
        return
    else:
        if result['user_id'] == ctx.author.id and result['nickname'] == nickname and result['password'] == password:
            data_methods.start_method(name='edit: auth_add',
                                      user_id=ctx.author.id)
            await ctx.channel.purge(limit=1000)
            await ctx.author.remove_roles(ctx.author.roles[-1])
            await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=778995970221932555))
        else:
            ctx.send('[login] Вы ввели неправильные данные!')


# registration room 4
@bot.command(pass_context=True)
@commands.has_role(783630956972081193)
async def registration(ctx, nickname1, password1, nickname2, password2):
    if nickname1 == nickname2 and password1 == password2:
        if not data_methods.start_method(name='get: user_id',
                                         user_id=ctx.author.id):
            data_methods.start_method(name='edit: add_reg',
                                      user_id=ctx.author.id, nickname=nickname1, password=password1)
            await ctx.send('[registration] Подождите... бот проверяет данные!\nИспользуйте команду ".check"')
        else:
            await ctx.send('[registration] Вы уже зарегестрированы!')
    else:
        await ctx.send('[registration] Не одинаковые данные!')


# registration room 4
@bot.command(pass_context=True)
@commands.has_role(783630956972081193)
async def check(ctx):
    result = data_methods.start_method(name='get: user_id',
                                       user_id=ctx.author.id)
    if result['auth'] == '2':
        await ctx.channel.purge(limit=1000)
        await ctx.author.remove_roles(ctx.author.roles[-1])
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=778995970221932555))
    else:
        await ctx.send('[register] Идет проверка, подождите...')


bot.run(config['token'])
