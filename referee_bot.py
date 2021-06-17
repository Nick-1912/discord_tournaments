import discord
from discord.ext import commands
from cfg import config_referee
import asyncio
import nest_asyncio
import data_methods
import qiwi_methods
from faceit_methods import FACEIT

nest_asyncio.apply()

faceit_bot_1 = FACEIT()
faceit_bot_1.faceit_login()
input('press enter after login')

bot = commands.Bot(command_prefix=config_referee['prefix'], intents=discord.Intents.all())
agree_bet = '👍'
delete_bet = '❌'


@bot.event
async def on_ready():
    print('bot started')


@bot.command(pass_context=True)
@commands.has_role(778995970221932555)
async def go(ctx, bet):
    await ctx.channel.purge(limit=1)
    try:
        float(bet)
    except ValueError:
        ans = await ctx.send(f'{ctx.author.mention}, Вы ввели не число!')
        await ans.delete(delay=5)
        return

    result = data_methods.start_method(name='get: user_id',
                                       user_id=ctx.author.id)
    if float(result['cash']) < float(bet):
        await ctx.author.send(f'{ctx.author.mention}, у Вас недостаточно средств на балансе!')
        return
    message = await ctx.send(f'{ctx.author.mention} хочет играть на {bet}!')
    await message.add_reaction(agree_bet)
    await message.add_reaction(delete_bet)

    def check(reaction_st1, user_st1):
        if str(user_st1) == 'referee_bot#5816':
            return
        result1 = data_methods.start_method(name='get: user_id',
                                            user_id=user_st1.id)
        if float(result1['cash']) < float(bet):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(user_st1.send(f'{user_st1.mention}, у Вас недостаточно средств на балансе!'))
            return
        else:
            return user_st1 != ctx.author and str(reaction_st1.emoji) == agree_bet or user_st1 == ctx.author and str(
                reaction_st1.emoji) == delete_bet

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=300.0, check=check)

    except asyncio.TimeoutError:
        ans = await ctx.send(f'{ctx.author.mention} никто не согласился :(')
        await message.delete()
        await ans.delete(delay=30)
        return
    if str(reaction.emoji) == agree_bet:
        await message.delete()
        ans2 = await ctx.send(f'{ctx.author.mention} и {user.mention} начало Вашего матча!\n'
                              f'Подтвердите свое присутсвие (30 сек):')
        await ans2.add_reaction('✔️')
        await asyncio.sleep(30)
        cache_ans2 = discord.utils.get(bot.cached_messages, id=ans2.id)
        reacts = cache_ans2.reactions[0]
        users = await reacts.users().flatten()
        users_count = 0
        await ans2.delete()
        for temp_user in users:
            if temp_user.id == user.id or temp_user.id == ctx.author.id:
                users_count += 1
            if users_count == 2:
                ans3 = await ctx.send(f'{ctx.author.mention} и {user.mention} Ваш матч готов! '
                                      f'Бот отправит Вам в личные сообщения ссылку на матч...')
                data_methods.start_method(name='edit: minus_cash',
                                          user_id=ctx.author.id, cash=bet)
                data_methods.start_method(name='edit: minus_cash',
                                          user_id=user.id, cash=bet)
                #
                # create match
                #
                result = faceit_bot_1.start_method(name='create_tournament',
                                                   nickname1=ctx.author.name, nickname2=user.name)
                while result:
                    print('[match] cant create, waiting 10 sec...')
                    faceit_bot_1.start_method(name='create_tournament',
                                              nickname1=ctx.author.name, nickname2=user.name)
                    await asyncio.sleep(10)

                await ans3.delete(delay=5)
                break
        else:
            ans3 = await ctx.send(f'{ctx.author.mention} и {user.mention} Ваш матч отменен, один из Вас не принял!')
        await ans3.delete(delay=10)
        return
    elif str(reaction.emoji) == delete_bet:
        await message.delete()
        ans = await ctx.send(f'{ctx.author.mention}, Вы отменили событие')
        await ans.delete(delay=5)
        return


@bot.command(pass_context=True)
@commands.has_role(778995970221932555)
async def info(ctx):
    await ctx.channel.purge(limit=1)
    qiwi_methods.update_cash(user_id=ctx.author.id)
    result = data_methods.start_method(name='get: user_id',
                                       user_id=ctx.author.id)
    await ctx.author.send(f"Ваш баланс: {result['cash']} руб")


@bot.command(pass_context=True)
@commands.has_role(778995970221932555)
async def cash(ctx, amount=None):
    await ctx.channel.purge(limit=1)
    if not amount:
        ans = await ctx.send(f'{ctx.author.mention}, Вы не указали сумму вывода!')
        await ans.delete(delay=5)
        return
    try:
        float(amount)
    except ValueError:
        ans = await ctx.send(f'{ctx.author.mention}, Вы ввели не число!')
        await ans.delete(delay=5)
        return
    result = data_methods.start_method(name='get: user_id',
                                       user_id=ctx.author.id)
    if float(result['cash']) < float(amount):
        await ctx.author.send(f'{ctx.author.mention}, у Вас недостаточно средств для вывода!')
    else:
        qiwi_methods.send_cash(user_id=ctx.author.id, cash=amount)
        await ctx.author.send(f'{ctx.author.mention}, оплата проведена.')


bot.run(config_referee['token'])
