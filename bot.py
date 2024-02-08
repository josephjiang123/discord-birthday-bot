from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
import asyncio
import discord
import birthdays
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
    await channel.send('Hello!')

@bot.command()
async def isItMyBirthday(ctx):
    await ctx.send("No")

@bot.command()
async def isItThisGuysBirthday(ctx, user:discord.User):
    if user.name == "josephjiang123":
        await ctx.send("Yes")
    else:
        await ctx.send("No")

@bot.command()
async def secondsUntilMidnight(ctx):
    await ctx.send(f'Time now: {seconds_until_midnight()}')
    await ctx.send(seconds_until_midnight())

@bot.command()
async def pingMe(ctx, member: discord.Member):
    await ctx.send(f'Happy birthday {member.mention}')

@bot.command()
async def birthday(ctx):
    birthday = birthdays.getTodaysBirthdays()
    guild = bot.get_guild(GUILD_ID)
    guild.fetch_members()

    for member in birthday:
        await ctx.send(f'Happy birthday {guild.get_member_named(member).mention}, please wish {birthday[member]} a happy birthday!')

def seconds_until_midnight():
    now = datetime.now()
    target = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    return diff

@tasks.loop(seconds=1)
async def called_once_a_day_at_midnight():
    message_channel = bot.get_channel(CHANNEL_ID)
    await message_channel.send(seconds_until_midnight())
    await asyncio.sleep(seconds_until_midnight())
    
    print(f"Got channel {message_channel}")
    await message_channel.send("ITS MIDNIGHT")

@called_once_a_day_at_midnight.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


bot.run(BOT_TOKEN)
