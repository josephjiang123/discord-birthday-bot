from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
import asyncio
import discord
import birthdays
import util
import random
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    called_once_a_day_at_midnight.start()
    channel = bot.get_channel(CHANNEL_ID)

@bot.command()
async def isItMyBirthday(ctx):
    if birthdays.isItTheirBirthday(ctx.author.name):
        await ctx.send("Yes")
    else:
        await ctx.send("No")

@bot.command()
async def secondsUntilMidnight(ctx):
    await ctx.send(f'Time now: {seconds_until_midnight()}')
    await ctx.send(seconds_until_midnight())

@bot.command()
async def insult(ctx, member: discord.Member):
    if member.global_name == "Pidgeon":
        await ctx.send(file=discord.File('snape.jpg'))
    else:
        insult = random.choice(util.insults)
        print(insult)
        await ctx.send(f'{insult}, {member.mention}')

@bot.command()
async def love(ctx, member: discord.Member):
    compliment = random.choice(util.compliments)
    await ctx.send(f'{compliment}, {member.mention}')


@bot.command()
async def birthday(ctx):
    birthday = birthdays.getTodaysBirthdays()
    guild = bot.get_guild(GUILD_ID)
    guild.fetch_members()

    for member in birthday:
        await ctx.send(f'Happy birthday {guild.get_member_named(member).mention}!')

def seconds_until_midnight():
    now = datetime.now()
    target = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    return diff

@tasks.loop(seconds=1)
async def called_once_a_day_at_midnight():
    message_channel = bot.get_channel(CHANNEL_ID)
    await asyncio.sleep(seconds_until_midnight())
    birthday = birthdays.getTodaysBirthdays()
    guild = bot.get_guild(GUILD_ID)
    guild.fetch_members()

    for member in birthday:
        await message_channel.send(f'Happy birthday {guild.get_member_named(member).mention}!')

@called_once_a_day_at_midnight.before_loop
async def before():
    await bot.wait_until_ready()

bot.run(BOT_TOKEN)
