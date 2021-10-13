import discord
import json
import os
import random

from JasonManager import Guardar_Users, Ler_Empregos

from discord.ext import commands
os.chdir("D:\Py\BotSharp\BotAlt")

client = commands.Bot(command_prefix="$",  case_insensitive=True)


@client.event
async def on_ready():
    #await Verificar_Users()
    print('Opa! To On!')


@client.command()
async def CriarConta(ctx, arg):
    Users = await Ler_Users()
    if str(ctx.author.id) in Users:
        ocup = Users[str(ctx.author.id)]["ocupação"]
        await ctx.send(f"Você já é cadastrado nessa escola como {ocup}")
        return
    
    arg = arg.lower()
    if arg == "aluno":
        await Criar_Conta_Aluno(ctx.author)
        await ctx.send("Você foi cadastrado com sucesso como Aluno")
    elif arg == "professor":
        await Criar_Conta_Professor(ctx.author)
        await ctx.send("Você foi cadastrado com sucesso como Professor")
    else:
        await ctx.send("O cadastro só aceita alunos ou professores")


    
    

@client.command(brief='Mostra seu perfil escolar(cria um caso não tenha)', description='Mostra a maioria das informações sobre você ná escola. É o primeiro comando que devo usar!')
async def MPerfil(ctx):

    contacriada = await ContaCriada(ctx.author)
    if contacriada != False:
        return
    

    Users = await Ler_Users()
    ocup = await Verficar_Ocupação(ctx.author)
    if str(ctx.author.id) in Users:
        if ocup == "Aluno":
            user = await Ler_Users()

            reputacao_total = user[str(ctx.author.id)]["reputação"]
            dinheiro_total = user[str(ctx.author.id)]["dinheiro"]
            
            portugues_total= user[str(ctx.author.id)]["notas"]["português"]
            matematica_total= user[str(ctx.author.id)]["notas"]["matemática"]
            biologia_total= user[str(ctx.author.id)]["notas"]["biologia"]
            historia_total= user[str(ctx.author.id)]["notas"]["história"]
            fisica_total= user[str(ctx.author.id)]["notas"]["física"]
            quimica_total= user[str(ctx.author.id)]["notas"]["química"]
            edfisica_total= user[str(ctx.author.id)]["notas"]["edfisica"]
            geografia_total= user[str(ctx.author.id)]["notas"]["geografia"]

            avatar = ctx.author.avatar_url

            em = discord.Embed(title = f"{ctx.author.name} Perfil", color = discord.Color.blue())
            em.set_author(name = "Perfil Escolar", icon_url='https://cdn-icons-png.flaticon.com/512/167/167707.png')
            em.set_thumbnail(url=avatar)
            em.add_field(name = "Reputação🎭", value= reputacao_total, inline=True)
            em.add_field(name = "Dinheiro💰", value= f"R${dinheiro_total}", inline=True)
            em.add_field(name = "NOTAS:", value= "📚" ,inline=False)
            em.add_field(name = "Português: 📕", value= portugues_total)
            em.add_field(name = "Matemática: 📊", value= matematica_total)
            em.add_field(name = "Biologia: 🔬", value= biologia_total)
            em.add_field(name = "História: 🗿", value= historia_total)
            em.add_field(name = "Fisíca: ⚗", value= fisica_total)
            em.add_field(name = "Química: 🧪", value= quimica_total)
            em.add_field(name = "Educação Fisica: ⚽", value= edfisica_total)
            em.add_field(name = "Geografia: 🌍", value= geografia_total)

            await ctx.send(embed = em)

        else: #---------------PROFESSOR

            reputacao_total = Users[str(ctx.author.id)]["reputação"]
            dinheiro_total = Users[str(ctx.author.id)]["dinheiro"]
            #ocupação = Users[str(ctx.author.id)]["ocupação"]
            

            avatar = ctx.author.avatar_url

            em = discord.Embed(title = f"{ctx.author.name} Perfil", color = discord.Color.blue())
            em.set_author(name = "Perfil de Professor", icon_url='https://cdn-icons-png.flaticon.com/512/167/167707.png')
            em.set_thumbnail(url=avatar)
            #em.set_footer(text= f"Perfil de {ocupação}")
            em.add_field(name = "Reputação🎭", value= reputacao_total, inline=True)
            em.add_field(name = "Dinheiro💰", value= f"R${dinheiro_total}", inline=True)

            await ctx.send(embed = em)
    else:
        await ctx.send("Se não tem conta, digite !Escola e crie")




async def Verficar_Ocupação(autor):
    Users= await Ler_Users()
    if Users[str(autor.id)]["ocupação"] == "Aluno":
        return "Aluno"
    else:
        return "Professor"

async def Ler_Users():
    if os.path.exists('UsersData.json'):
        with open('UsersData.json', 'r', encoding='utf-8') as f:
            Users= json.load(f)
    return Users


async def ContaCriada(autor):
    Users= await Ler_Users()
    if not str(autor.id) in Users:
        return True
    else:
        return False

async def Criar_Conta_Professor(autor):
    Users= await Ler_Users()
    if not str(autor.id) in Users:
        print("Não está na lista")
        Users[autor.id] = {
            "id": autor.id,
            "nome": autor.name,
            "ocupação": "Professor",
            "dinheiro": 0,
            "reputação": 0,
            "estaempregado": True,
            "emprego":{},
            "inventario": {}
            }
        Guardar_Users(Users)
        return True
    else:
        return False

async def Criar_Conta_Aluno(autor):
    Users= await Ler_Users()
    if not str(autor.id) in Users:
        print("Não está na lista")
        Users[autor.id] = {
            "id": autor.id,
            "nome": autor.name,
            "ocupação": "Aluno",
            "dinheiro": 0,
            "reputação": 0,
            "estaempregado": False,
            "emprego":{},
            "notas": {
                "português": 0,
                "matemática": 0,
                "biologia": 0,
                "história": 0,
                "física": 0,
                "química":0,
                "geografia": 0,
                "edfisica": 0
            },
            "inventario": {}
            }
        Guardar_Users(Users)
        return True
    else:
        return False



client.run('ODk3NTU5MDA0NzgyMzk5NTE5.YWXa9g.fkAbeN7ZKGBGthS128FfLxnhrqk')