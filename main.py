import discord
from discord.ext import commands
from discord import app_commands
import random
import re
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv(override=True)
import os
# ( all ) todas as permissoes q o bot precisa guardado na var intents

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all()) # prefix
bot.remove_command("help")

# importando tds os cogs de 1 vez só
async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'): # se o arq termina com '.py'
            await bot.load_extension(f'cogs.{arquivo[:-3]}') # :-3 ".py"


@bot.event # eventos são ativos qnd algo especifico acontece
async def on_ready(): 
    await carregar_cogs()
    # await bot.tree.sync()
    print('—————————————————————————————————————————————————\nBOT INICIALIZADO COM SUCESSO! :) \n')
    
    # status do bot
    activity = discord.Activity(type=discord.ActivityType.watching, name="Fairy Tail")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
# jogando:
# activity = discord.Game(name="nomedojogo")  

# ouvindo:
# discord.Activity(type=discord.ActivityType.listening, name="música boa")

# transmitindo (streaming) — aparece roxinho:
# discord.Streaming(name="meu gameplay", url="https://twitch.tv/link")

        





# ctx = comando hibrido/padrao e interaction = comando slash
# bot.run precisa estar em ULTIMO para analisar todo o código e poder rodar
bot.run(os.getenv("DISCORD_TOKEN"))
