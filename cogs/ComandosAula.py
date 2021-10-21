import discord
from discord.ext import commands

class Aulas(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def TAulas(self, ctx):
        em = discord.Embed(title = f"{ctx.author.name} Perfil", color = discord.Color.green())
        em.set_author(name = "Horário/dia das aulas", icon_url='https://cdn-icons-png.flaticon.com/512/167/167707.png')
        em.add_field(name = "Horários:", value= "⌚", inline=False)
        em.add_field(name = "Segunda/Terça/Quinta:", value= "21:00 - 22:00", inline=True)
        em.add_field(name = "Quarta/Sexta:", value= "21:00 - 23:00", inline=True)
        em.add_field(name = "Aulas:", value= "📚", inline=False)
        em.add_field(name = "Segunda-Feira", value= "Aula de Biologia", inline=False)
        em.add_field(name = "Terça-Feira", value= "Aula de Matemática", inline=False)
        em.add_field(name = "Quarta-Feira", value= "Aula de Português, Aula de Geografia", inline=False)
        em.add_field(name = "Quinta-Feira", value= "Aula de História", inline=False)
        em.add_field(name = "Sexta-Feira", value= "Aula de Física, Aula de Química", inline=False)

        await ctx.send(embed = em)
def setup(client):
    client.add_cog(Aulas(client))