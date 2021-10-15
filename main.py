import discord
import json
import os
import random
import asyncio

from discord.errors import NoMoreItems
from JasonManager import Guardar_Users, Ler_Empregos
from discord.ext import commands, tasks
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
import datetime as dt

os.chdir("home\\user_238459676876996619")

client = commands.Bot(command_prefix="!!",  case_insensitive=True)

"""for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')"""

@client.event
async def on_ready():
    Aula_Portugues.start()
    print('Opa! To On!')
#-------------------------------------------------------------------------------------
#--------------------------------Aulas------------------------------------------------
#-------------------------------------------------------------------------------------

aulaAtual= {"nome": "Nenhuma", "professor": "00000000", "motivo": "Aula normal"}

#-------------------------------------------------------------------------------------
#--------------------------------ITENS------------------------------------------------
#-------------------------------------------------------------------------------------

lojaalunos = [{"nome":"Refrigerante Cola-Coca", "preço": 6, "descrição": "Suquinho"},
            {"nome":"Sanduiche", "preço": 5, "descrição": "Sanduicheiche" },
            {"nome":"Caderno", "preço": 20, "descrição":"Caderno" },
            {"nome":"Mochila estilosa", "preço": 30, "descrição":"Caderno" },
            {"nome":"Régua", "preço": 10, "descrição":"Caderno" },
            {"nome":"Mapa", "preço": 14, "descrição":"Caderno" },
            {"nome":"Pizza", "preço": 8, "descrição":"Caderno" },
            {"nome":"Bala 7Feios", "preço": 3, "descrição":"Caderno" },]



#-------------------------------------------------------------------------------------
#--------------------------------PERFIL-----------------------------------------------
#-------------------------------------------------------------------------------------
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
        #await Criar_Conta_Professor(ctx.author)
        await ctx.send(f"Fale com <@238459676876996619> sobre o cargo de professor!!")
        await ctx.send(f"Atualmente só estamos aceitando professores após entrevistas.")
    else:
        await ctx.send("O cadastro só aceita 'Aluno' ou 'Professor' ")



@client.command(brief='Mostra seu perfil escolar(cria um caso não tenha)', description='Mostra a maioria das informações sobre você ná escola. É o primeiro comando que devo usar!')
async def Perfil(ctx):

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
            professorempre = Users[str(ctx.author.id)]["emprego"]["nomeemprego"]
            #ocupação = Users[str(ctx.author.id)]["ocupação"]
            

            avatar = ctx.author.avatar_url

            em = discord.Embed(title = f"{ctx.author.name} Perfil", color = discord.Color.blue())
            em.set_author(name = "Perfil de Professor", icon_url='https://cdn-icons-png.flaticon.com/512/167/167707.png')
            em.set_thumbnail(url=avatar)
            #em.set_footer(text= f"Perfil de {ocupação}")
            em.add_field(name = "Reputação🎭", value= reputacao_total, inline=True)
            em.add_field(name = "Dinheiro💰", value= f"R${dinheiro_total}", inline=True)

            em.add_field(name="Professor📜", value= professorempre, inline= False)
            await ctx.send(embed = em)
    else:
        await ctx.send("Se não tem conta, digite !Escola e crie")

@client.command(brief='Mostrar o inventário', description='Mostra todos seus itens guardados no iventário')
async def Inv(ctx):
    contacriada = await ContaCriada(ctx.author)
    if contacriada != False:
        await ctx.send("Você não tem conta ainda, digite !!CriarConta")
        return

    user = ctx.author
    
    users = await Ler_Users()

    try:
        inv = users[str(user.id)]["inventario"]
    except:
        inv = []


    em = discord.Embed(title = "Inventário")
    for item in inv:
        name = item["item"]
        quantidade = item["quantidade"]

        em.add_field(name = name, value = quantidade)    

    await ctx.send(embed = em)    

#-------------------------------------------------------------------------------------
#--------------------------------TRABALHO---------------------------------------------
#-------------------------------------------------------------------------------------

@client.command(brief='Trabalhar = Dinheiro', description='Comando serve para você trabalhar caso tenha um emprego!')
@commands.cooldown(1,60,commands.BucketType.user) # one command, every 30 seconds, per user
async def Trab(ctx):
    Users = await Ler_Users()
    if str(ctx.author.id) in Users:
        if Users[str(ctx.author.id)]["estaempregado"] == True:
            dinheirominq = int(Users[str(ctx.author.id)]["emprego"]["dinheiromin"])
            dinheiromaxq = int(Users[str(ctx.author.id)]["emprego"]["dinheiromax"])
            DinheiroGanho = random.randrange(dinheirominq,dinheiromaxq)
            Users[str(ctx.author.id)]["dinheiro"] += DinheiroGanho
            await ctx.send(f"Seu trabalho rendeu: {DinheiroGanho} pila!")

            Guardar_Users(Users)
        else:
            await ctx.send("Você não tem emprego!")
    else:
        await ctx.send("Você não é um aluno!!")

@client.command(brief='Entre em um emprego', description='Esse comando serve para você entrar em um emprego que queria! Especifique o nome do emprego!')
async def Emprego(ctx, emprego):
    Users = await Ler_Users()
    Empregos = Ler_Empregos()
    emp = emprego.lower()
    if str(ctx.author.id) in Users:
        if Users[str(ctx.author.id)]["estaempregado"] == False:
            if emp in Empregos:
                print("AAA")
                Users[str(ctx.author.id)]["estaempregado"] = True
                Users[str(ctx.author.id)]["emprego"] = Empregos[emprego]
                Guardar_Users(Users)
                await ctx.send(f"Você agora está trabalhando como {emprego}")
            else:
                await ctx.send("Verifique o nome do emprego que você digitou e tente novamente!")
        else:
            await ctx.send("Você já está em um emprego!")
    else:
        await ctx.send("Você não é um aluno")

@client.command(brief='Você desiste do seu emprego', description='Comando para sair do emprego. (Muito bom caso você odeia ele)')
async def SairEmprego(ctx):
    Users = await Ler_Users()
    if str(ctx.author.id) in Users:
        if Users[str(ctx.author.id)]["estaempregado"] == True:
            Users[str(ctx.author.id)]["estaempregado"] = False
            Users[str(ctx.author.id)]["emprego"] = {
                "nomeemprego": "Sem emprego",
                "dinheiromin": "0",
                "dinheiromax": "0"
            }
            Guardar_Users(Users)
            await ctx.send(f"Você deixou o emprego!")
        else:
            await ctx.send("Você não está em um emprego!")
    else:
        await ctx.send("Você não é um aluno")



@client.command(brief='Uma lista de empregos', description='Verificar os empregos disponiveis!')
async def ListaDeEmpregos(ctx):
    em = discord.Embed(
        title = "Lista de empregos", 
        description = 'Encontre sua forma de ganhar dinheiro‼',
        color = discord.Color.dark_orange()
        )
    em.add_field(name = "Limpeza do campus", value= "De R$10 a R$ 20", inline=False)
    em.add_field(name = "Trabalhar na cantina", value= "De R$5 a R$20", inline=False)
    em.add_field(name = "Ajudante de professor", value= "De R$5 a R$25" ,inline=False)
    '''em.add_field(name = "Mochila estilosa 🎒", value= "R$30" ,inline=False)
    em.add_field(name = "Régua 📐", value= "R$10" ,inline=False)
    em.add_field(name = "Mapa´🗺", value= "R$14" ,inline=False)
    em.add_field(name = "Pizza 🍕", value= "R$8" ,inline=False)
    em.add_field(name = "Bala 7Feios 🍬", value= "R$3" ,inline=False)
    em.add_field(name = "??? ⁉", value= "R$???" ,inline=False)'''
        
    await ctx.send(embed = em)


#-------------------------------------------------------------------------------------
#--------------------------------LOJAS------------------------------------------------
#-------------------------------------------------------------------------------------

@client.command()
async def Loja(ctx):
    em = discord.Embed(
        title = "Loja Escolar", 
        description = 'Lojinha comum da escola.',
        color = discord.Color.gold()
        )

    for item in lojaalunos:
        nomeitem = item["nome"]
        preçoitem = item["preço"]
        descriçãoitem = item["descrição"]
        em.add_field(name = nomeitem, value= f"${preçoitem} | {descriçãoitem}")
    '''em.add_field(name = "Refrigerante Cola-Coca 🥤", value= "R$6", inline=False)
    em.add_field(name = "Sanduiche 🥪", value= "R$5", inline=False)
    em.add_field(name = "Caderno 📖", value= "R$20" ,inline=False)
    em.add_field(name = "Mochila estilosa 🎒", value= "R$30" ,inline=False)
    em.add_field(name = "Régua 📐", value= "R$10" ,inline=False)
    em.add_field(name = "Mapa´🗺", value= "R$14" ,inline=False)
    em.add_field(name = "Pizza 🍕", value= "R$8" ,inline=False)
    em.add_field(name = "Bala 7Feios 🍬", value= "R$3" ,inline=False)
    em.add_field(name = "??? ⁉", value= "R$???" ,inline=False)'''
        
    await ctx.send(embed = em)


@client.command(brief='Compre um item', description='Coloque o nome do item entre aspas e a quantidade depois')
async def Comprar(ctx,item, quantidade =1):
    contacriada = await ContaCriada(ctx.author)
    if contacriada != False:
        await ctx.send("Você não tem conta ainda, digite !!CriarConta")
        return
    
    print("comprar")
    res = await buy_this(ctx.author, item, quantidade)
    if not res[0]:
        if res[1] == 1:
            await ctx.send("Esse item não está disponível nessa loja!")
            return
        if res[1] == 2:
            await ctx.send(f"Você não tem dinheiro para isso!! O total dava R${res[2]}!")
            return
        
    await ctx.send(f"Você comprou {quantidade} item de {item}!")


async def buy_this(user, item_name, quantidade):
    item_name = item_name.lower()
    name_ = None
    print(name_)
    for item in lojaalunos:
        print(item["nome"].lower())
        name = item["nome"].lower()
        if(name == item_name):
            name_ = name
            print(name_)
            price = item["preço"]
            break
    
    if(name_ == None):
        print("Test1")
        return[False, 1]
    
    cost = price*quantidade
    Users = await Ler_Users()

    if Users[str(user.id)]["dinheiro"]<cost:
        print("test 2")
        return[False,2, cost]

    print("test 3")
    try:
        index = 0
        t = None
        print("test 4")
        for thing in Users[str(user.id)]["inventario"]:
            print("Test 5")
            print(thing["item"] + "AAAAAAAAAAAAA")
            n = thing["item"]
            print(n)
            if n == item_name:
                old_amt = thing["quantidade"]
                new_amt = old_amt + quantidade
                print(new_amt)
                Users[str(user.id)]["inventario"][index]["quantidade"] = new_amt
                t = 1
                break
            index += 1
        print("Test 6")
        if t == None:
            print("Test 7")
            obj = {"item":item_name , "quantidade" : quantidade}
            Users[str(user.id)]["inventario"].append(obj)
    except:
        print("Test 8")
        obj = {"item":item_name , "quantidade" : quantidade}
        Users[str(user.id)]["inventario"] =[obj]
    Users[str(user.id)]["dinheiro"] -= cost
    Guardar_Users(Users)

    return[True, "Worked"]
#-------------------------------------------------------------------------------------
#--------------------------------DEFS-------------------------------------------------
#-------------------------------------------------------------------------------------


    
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
            "emprego":{
                "nomeemprego": "Sem emprego",
                "dinheiromin": "0",
                "dinheiromax": "0"
            },
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
            "reputação": 50,
            "estaempregado": False,
            "emprego":{
                "nomeemprego": "Sem emprego",
                "dinheiromin": "0",
                "dinheiromax": "0"
            },
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

#-------------------------------------------------------------------------------------
#--------------------------------ERROS------------------------------------------------
#-------------------------------------------------------------------------------------

@Trab.error
async def Trab_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
         await ctx.send(f'Você trabalhou demais! O comando estará disponivel em {round(error.retry_after, 2)} seconds')

@Emprego.error # Decorator to specify this is the handler for this command only
async def Emprego_arg_faltando(ctx, error): # Context and error required
    if isinstance(error, commands.MissingRequiredArgument): # Check if the exception is what you want to handler
        await ctx.send("Especifique o trabalho que você quer trabalhar, entre aspas")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando não existe')




#-------------------------------------------------------------------------------------
#--------------------------------COISAS-----------------------------------------------
#-------------------------------------------------------------------------------------
@tasks.loop(hours=168)
async def Aula_Portugues():
    message_channel = client.get_channel(898308678187364352)
    await message_channel.send("A aula de portguês está començando")
    prof = await Get_professor("Professor de Português")
    aulaAtual["nome"] = "Português"
    aulaAtual["professor"] = prof
    aulaAtual["motivo"] = "Aula normal"
    if prof != False:
        profid = "<@!"+ str(prof) +">"
        await message_channel.send(f"Professor {profid}, já vai chegar")
    else:
        await message_channel.send(f"Professor ausente, aula livre!!")
    await asyncio.sleep(60)


    await message_channel.send("A aula acabou")

@Aula_Portugues.before_loop
async def before_Aula_Portugues():
    # loop the whole 7 day (60 sec 60 min 24 hours 7 days)
    for _ in range(60*60*24*7):  
        if dt.datetime.utcnow().strftime("%H:%M UTC %a") == "23:00 UTC Fri":
            print('It is time')
            return

        # wait some time before another loop. Don't make it more than 60 sec or it will skip
        await asyncio.sleep(10)


async def Get_professor(materia):
    Users = await Ler_Users()
    id_ = None
    for prof in Users:
        print(Users[prof]["emprego"]["nomeemprego"])
        if Users[prof]["emprego"]["nomeemprego"] == str(materia):
            id_ = Users[prof]["id"]
            print(id_)
            return id_
    
    if id_ == None:
        print("Nada")
        return False




@client.command()
async def checkTime(ctx):
    # This function runs periodically every 1 second

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    await ctx.send(f"Current Time = {current_time}")

    if(current_time >= '21:10:00'):  # check if matches with the desired time
        await ctx.send('sending message')
    else:
        await ctx.send('não está na hora')

'''def check(m):
        return m.content == "hello" and m.channel == ctx.channel


    msg = await client.wait_for("message", check=check)
    await ctx.send(f"Hello {msg.author}!")'''

client.run('ODg4MDg1NzczNTU4MTE2MzYz.YUNkVA.SQkLn6homzrsyBW_qiTbehK-QbU')
