# Discord PY Warning system!

import sqlite3
import discord
from discord.ext import commands

con = sqlite3.connect("./databases/simple.db") # Link with database
cur = con.cursor()

bot = commands.Bot(command_prefix='yourprefixhere', intents=discord.Intents.all())

@bot.command()
@commands.has_permissions(manage_messages=True) # Checking for permission (manage messages)
async def warn(ctx: commands.Context, member: discord.Member, *, reason):

    cur.execute(f"INSERT INTO Warny (UserId, UserName, Reason, GuildId) VALUES ({member.id}, '{f'{member.name}#{member.discriminator}'}', '{reason}', {ctx.guild.id})") #Executing command with sqlite3 (inserting data)
    con.commit() # Committing, thats required!

# Embeds below (in my example in Polish)
    embed = discord.Embed(title="Zwarnowano!", colour=discord.Colour.red())
    embed.add_field(name='Użytkownik', value=f'{member.name}: {member.id}', inline=False)
    embed.add_field(name='Powód', value=reason, inline=False)
    await ctx.send(embed=embed) # Sending embed, required too!


# Below command for getting warn list of specified user!

    
@bot.command()
@commands.has_permissions(manage_messages=True) # Checking perms!
async def warnlist(ctx: commands.Context, member: discord.Member):
    numrow = 0 # Its variable for counting the warns of different user! Not required.
    rows = cur.execute(f"SELECT * FROM Warny WHERE UserId={member.id} AND GuildId={ctx.guild.id}")
    con.commit()
    embed = discord.Embed(title="Warn lista!", colour=discord.Colour.og_blurple())
    for i in rows:
        numrow += 1 # Adds 1 to numrow variable for single one warn!
        embed.add_field(name=f'Warn ID: {i[0]}', value=f'```ID Użytkownika :::: {i[1]}\nNazwa użytkownika :::: {i[2]}\nPowód warna :::: {i[3]}```', inline=False) # adds field for every warn (if there are 2 warns it adds two fields)
    embed.set_footer(text=f'Aktualnie użytkownik {member.name} posiada {numrow} ostrzeżeń') # Here is info about how many warns it is
    await ctx.send(embed=embed) # Sending embed
    
    
# Below deleting warns!
    
@bot.command()
@commands.has_permissions(manage_messages=True) # Checking perms!
async def delwarn(ctx: commands.Context, member: discord.Member, warnid):
    w = cur.execute(f"SELECT * FROM Warny WHERE ID={warnid} AND UserId={member.id}") # Selecting/searching for warns
    embed = discord.Embed(title="Usunięto ostrzeżenie")
    for i in w:
        embed.add_field(name=f'Warn ID: {i[0]}', value=f'```ID Użytkownika :::: {i[1]}\nNazwa użytkownika :::: {i[2]}\nPowód warna :::: {i[3]}```', inline=False)
    await ctx.send(embed=embed)
    cur.execute(f"DELETE FROM Warny WHERE ID={warnid} AND UserId={member.id}")
    con.commit()


