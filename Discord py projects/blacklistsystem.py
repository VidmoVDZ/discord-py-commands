# Discord PY blacklist system, baning or kicking user that is on guild blacklist, you need database and one simple event for baning user on join

import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix="PrefixHere", intents=discord.Intents.all())

con = sqlite3.connect('./databases/simple.db')
cur = con.cursor()



#The event!!!
@bot.event
async def on_member_join(member: discord.Member):
    search = cur.execute(f"SELECT * FROM Blacklist WHERE UserId={member.id} AND GuildId={member.guild.id}")
    for x in search:
        if int(x[1]) == member.id:
            await member.send("Wyrzucono cie ponieważ widniejesz na blackliscie tego serwera")
            await member.kick(reason='Wyrzucono ponieważ użytkownik widnieje na blackliście na tym serwerze')


#The command!!!
@bot.command(description="Dodaje, usuwa, lub wyświetla osoby z blacklisty")
@commands.has_permissions(administrator=True)
async def blacklist(ctx: commands.Context, option = None, member: discord.Member = None):
    if option != None:
        if member != None:
            search = cur.execute(f"SELECT * FROM Blacklist WHERE UserId={member.id} AND GuildId={ctx.guild.id}")
            x = 0
            for z in search:
                x += 1
            if option == '-a' or option == '-add':
                if x > 1 or x == 1:
                    if x > 1:
                        y = x - 1
                        await ctx.send(f"Istnieje już ten użytkownik na blackliście na tym serwerze, wpis powtarza się {x} razy, usuniętych zostanie {y}")
                        cur.execute(f"DELETE FROM Blacklist WHERE UserId={member.id} AND GuildId={ctx.guild.id} IN (SELECT {y} FROM Blacklist WHERE UserId={member.id} AND GuildId={ctx.guild.id} LIMIT {y})")
                        con.commit()
                        pass
                    if x == 1:
                        await ctx.send("Istnieje już ten użytkownik w spisie!")
                        pass
                else:
                    cur.execute(f"INSERT INTO Blacklist (UserId, UserName, GuildId) VALUES ({member.id}, '{member.name}', {ctx.guild.id})")
                    embed = discord.Embed(title="Dodano użytkownika do blacklisty!", colour=discord.Colour.red())
                    embed.add_field(name="Info o użytkowniku poddanym blackliście", value=f'```Nazwa :::: {member.name}#{member.discriminator}\nID :::: {member.id}```')
                    await ctx.send(embed=embed)
                    con.commit()
        if option == '-h' or option == '-help':
            embed = discord.Embed(title="Możliwe opcje dla tej komendy", description="Dodaj użytkownika do blacklisty")
            embed.add_field(name='-h/-help', value="Pokazuję tą wiadomość", inline=False)
            embed.add_field(name='-r/-remove', value="Usuwa użytkownika z blacklisty", inline=False)
            embed.add_field(name='-a/-add', value="Dodaje użytkownika do blacklisty", inline=False)
            embed.add_field(name='-l/-list', value="Pokazuje liste osób na blackliście", inline=False)
            embed.add_field(name='-c/-clear', value="Czyści blackliste", inline=False)
            embed.add_field(name="Przykład użycia", value='```$blacklist -h\n$blacklist -a @user\n$blacklist```')
            await ctx.send(embed=embed)
        if option == '-r' or option == '-remove':
            cur.execute(f"DELETE FROM Blacklist WHERE UserId={member.id} AND GuildId={ctx.guild.id}")
            embed = discord.Embed(title="Usunięto użytkownika z blacklisty!", colour=discord.Colour.red())
            embed.add_field(name="Info o użytkowniku poddanym usunięciu z blacklisty", value=f'```Nazwa :::: {member.name}#{member.discriminator}\nID :::: {member.id}```')
            await ctx.send(embed=embed)
            con.commit()
        if option == '-l' or option == '-list':
            rows = cur.execute(f'SELECT * FROM Blacklist WHERE GuildId={ctx.guild.id}')
            y = 0
            embed = discord.Embed(title='Lista osób na blackliście', colour=discord.Colour.red())
            for x in rows:
                y += 1
                embed.add_field(name=f'ID użytkownika: {x[1]}', value=f'```Nazwa :::: {x[2]}```', inline=False)
            embed.set_footer(text=f'Na serwerze nałożono blackliste {y} razy')
            await ctx.send(embed=embed)
        if option == '-c' or option == '-clear':
            cur.execute(f"DELETE FROM Blacklist WHERE GuildId={ctx.guild.id}")
            embed = discord.Embed(title="Wyczyszczono blacklistę!", colour=discord.Colour.red())
            await ctx.send(embed=embed)
            con.commit()
    if option == None:
        embed = discord.Embed(title="Możliwe opcje dla tej komendy", description="Dodaje użytkownika do blacklisty")
        embed.add_field(name='-h/-help', value="Pokazuję tą wiadomość", inline=False)
        embed.add_field(name='-r/-remove', value="Usuwa użytkownika z blacklisty", inline=False)
        embed.add_field(name='-a/-add', value="Dodaje użytkownika do blacklisty", inline=False)
        embed.add_field(name='-l/-list', value="Pokazuje liste osób na blackliście", inline=False)
        embed.add_field(name='-c/-clear', value="Czyści blackliste", inline=False)
        embed.add_field(name="Przykład użycia", value='```$blacklist -h\n$blacklist -a @user\n$blacklist```')
        await ctx.send(embed=embed)
