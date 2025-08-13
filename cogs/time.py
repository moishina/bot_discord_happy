import discord
from discord import app_commands
from discord.ext import commands
import random
import re

class Time(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
# # codigo do comando X. para slash commands = @app_commands.command() e usa interaction invés de ctx
    @app_commands.command(name="time", description="Divide os membros do canal de voz em dois times aleatórios.")
    async def time(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("Você precisa estar em um canal de voz pra usar esse comando!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        members = [member for member in voice_channel.members if not member.bot]

        if len(members) < 2:
            await interaction.response.send_message("Precisa ter pelo menos 2 pessoas no canal de voz pra formar times!", ephemeral=True)
            return

        random.shuffle(members)
        half = len(members) // 2
        time1 = members[:half]
        time2 = members[half:]

        def format_team(team):
            return '\n'.join(member.display_name for member in team)

        mensagem = (
            f"🎮 **Times formados!** 🎮\n\n"
            f"🔵 **Time 1:**\n{format_team(time1)}\n\n"
            f"🔴 **Time 2:**\n{format_team(time2)}"
    )
        await interaction.response.send_message(mensagem)   
        
        
 
 
 
async def setup(bot):
    await bot.add_cog(Time(bot))