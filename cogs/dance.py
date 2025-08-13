import discord
from discord import app_commands
from discord.ext import commands
import random

class Dance(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        

    @app_commands.command(name="dance", description="Happy dançandinho")   
    async def dance(self, interaction: discord.Interaction):
        gifs_dance = ["https://64.media.tumblr.com/42c1aadb9e924a58c7578045d306fe5c/tumblr_on78agNv5W1vefoo6o1_540.gif",
            "https://media.tenor.com/GM-JoUIZ_ZgAAAAM/fairy-tail-happy.gif",
            "https://i.pinimg.com/originals/75/c2/81/75c2816899af78fba491c893125e16aa.gif"]
        
        gif_escolhido = random.choice(gifs_dance)

        embed = discord.Embed(

            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url=gif_escolhido)

        # envia a resposta e salva a mensagem retornada
        await interaction.response.send_message(embed=embed)
        response = await interaction.original_response()

        # reage com emoji de dança
        await response.add_reaction("💃")    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Dance(bot))