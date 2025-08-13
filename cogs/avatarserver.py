import discord
from discord import app_commands
from discord.ext import commands

class AvatarServer(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="server_avatar", description="Mostra o ícone do servidor")   
    async def server_avatar(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild.icon:
            embed = discord.Embed(
                title=f"avatar do servidor '{guild.name}'",
                color=discord.Color.from_rgb(255,255,255)
            )
            embed.set_image(url=guild.icon.url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Este servidor não tem ícone.", ephemeral=True)  
           
 
 
 
async def setup(bot):
    await bot.add_cog(AvatarServer(bot))