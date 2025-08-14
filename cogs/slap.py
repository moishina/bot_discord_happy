import discord
from discord import app_commands
from discord.ext import commands
import random

class Slap(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="slap", description="Dá um tapa em alguém")   
    @app_commands.describe(user="Quem vai receber o tapa")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("‼️ Você não pode se dar tapas...", ephemeral=True)
            return

        #  resposta especial se tentar bater no bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                title=":(",
                color=discord.Color.from_rgb(158, 242, 255)
            )
            embed.set_image(url="https://media.tenor.com/LVT7ipJn_C8AAAAd/happy-fairy-tail.gif")
            
            await interaction.response.send_message(embed=embed)
            return

        #  lista de GIFs de tapa
        gifs_tapa = [
            "https://media.tenor.com/AzIExqZBjNoAAAAd/anime-slap.gif",
            "https://media.tenor.com/FrEq8y-Qf78AAAAd/anime-slapping.gif",
            "https://imgur.com/EozsOgA.gif",
            "https://i.pinimg.com/originals/40/ef/24/40ef24388a01ba9be6da6dea69d30fda.gif",
            "https://mageinabarrel.com/wp-content/uploads/2014/06/akari-slap.gif",
            "https://i.gifer.com/2mqv.gif",
            "https://i.gifer.com/TgZ1.gif",
            "https://imgur.com/lAioGCC.gif"
        ]

        gif_escolhido = random.choice(gifs_tapa)

        embed = discord.Embed(
            description=f"👊\u2003{user1.mention} **deu um tapa em {user2.mention}!**",
            color=discord.Color.pink()
        )
        embed.set_image(url=gif_escolhido)

        
    # botao retribuir
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_deutapa: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_deutapa = quem_deutapa
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="👊 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("‼️ Só quem recebeu o tapa pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o tapa de {self.quem_deutapa.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_tapa))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_deutapa, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)   
        
 
 
 
async def setup(bot):
    await bot.add_cog(Slap(bot))