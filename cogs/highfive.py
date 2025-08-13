import discord
from discord import app_commands
from discord.ext import commands
import random

class HighFive(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="highfive", description="Faz um toca aqui com alguém (ou com o bot...)")   
    @app_commands.describe(user="Quem vai receber o highfive")
    async def highfive(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("❌ Você não pode fazer toca aqui consigo mesmo(a)!...", ephemeral=True)
            return

        #  resposta especial se fazer carinho no bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                color=discord.Color.from_rgb(158, 242, 255)
            )
            embed.set_image(url="https://imgur.com/M4A0Yys.gif")
            
            await interaction.response.send_message(embed=embed)
            return

        #  lista de GIFs aleatórios 
        gifs_highfive = [
            "https://64.media.tumblr.com/bb330522676865e19a3323bae4911f0c/bed24f800fd76092-30/s640x960/1be36be488e76453fa0a62709e9f0548c33a606d.gif",
            "https://imgur.com/gYRdIJy.gif",
            "https://64.media.tumblr.com/670b47fe8f7da2a49e8089ccfa233c9d/tumblr_pc1t0wl1xR1wn2b96o1_1280.gif",
            "https://media.tenor.com/F7JahZ_ntfUAAAAd/fairy-tail-high-five.gif",
            "https://imgur.com/jqvfgq0.gif",
            "https://imgur.com/6PzAerS.gif",
            "https://imgur.com/vO5SgfO.gif"
            ]

        gif_escolhido = random.choice(gifs_highfive)

        embed = discord.Embed(
            description=f"💌\u2003{user1.mention} **fez um toca aqui com {user2.mention}!**\n",
            color=discord.Color.pink()
        )
        embed.set_image(url=gif_escolhido)
        
        
    #  BOTAO DE RETRIBUIR
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_deuhighfive: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_deuhighfive = quem_deuhighfive
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("❌ Só quem recebeu o toca aqui pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o toca aqui de {self.quem_deuhighfive.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_highfive))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_deuhighfive, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(HighFive(bot))