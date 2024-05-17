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
MAIN_CHANNEL = int(os.getenv("MAIN_CHANNEL_ID"))

TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))

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
async def love(ctx, mention: str):
    compliment = random.choice(util.compliments)

    if mention == "@everyone":
        await ctx.send(f'@everyone {compliment}')
    else:
        # Attempt to convert the mention to a member object
        try:
            member = await commands.MemberConverter().convert(ctx, mention)
            await ctx.send(f'{compliment}, {member.mention}')
        except commands.MemberNotFound:
            await ctx.send("Member not found. Please mention a valid member.")


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
    message_channel = bot.get_channel(MAIN_CHANNEL)
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
