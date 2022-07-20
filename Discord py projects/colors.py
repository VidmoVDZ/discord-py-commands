# Discord PY rainbow roles!
import discord
from discord.ext import commands, tasks

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="prefixHere", intents=intents)

@tasks.loop(minutes=1) # Interval: every time after 1 minute color of role changes!
async def colors():
    guild = bot.get_guild(GUILD_ID_HERE) # Getting guild by its id
    rola = discord.utils.get(guild.roles, id=ROLE_ID_HERE) # Getting role by its id
    await rola.edit(colour=discord.Colour.random()) #Getting random color
