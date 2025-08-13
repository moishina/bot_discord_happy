import discord
from discord import app_commands
from discord.ext import commands
import random

class Bite(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="bite", description="Dê uma mordida em alguém (ou no bot...)")   
    @app_commands.describe(user="Quem vai receber a mordida")
    async def bite(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("❌ Você não pode morder a si mesmo(a)!...", ephemeral=True)
            return

        #  resposta especial se morder o bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                color=discord.Color.from_rgb(158, 242, 255)
            )
            embed.set_image(url="https://giffiles.alphacoders.com/141/141597.gif")
            
            await interaction.response.send_message(embed=embed)
            return

        #  lista de GIFs aleatórios 
        gifs_bite = [
            "https://i.pinimg.com/originals/f3/08/e2/f308e2fe3f1b3a41754727f8629e5b56.gif",
        "https://media.tenor.comp82FpH4jzp0AAAAd/vampire-diabolik-lovers.gif",
        "https://i.gifer.com/QHEF.gif",
        "https://i.gifer.com/2qw6.gif",
        "https://i.makeagif.com/media/1-15-2016/7QJBkD.gif",
        "https://64.media.tumblr.com/bd7c3f0bb557197439c03b82354b8ba8/5833c15b778ca53f-ce/s640x960/a741fd75532af2e6e71446e8e392b5418d2a86e3.gif",
        "https://media.tenor.com/BMEjcm2O8zsAAAAM/anime-bite.gif"
            ]

        gif_escolhido = random.choice(gifs_bite)

        embed = discord.Embed(
            description=f"💌\u2003{user1.mention} **deu uma mordida em {user2.mention}!**\n",
            color=discord.Color.pink()
        )
        embed.set_image(url=gif_escolhido)
        
        
    #  BOTAO DE RETRIBUIR
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_mordeu: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_mordeu = quem_mordeu
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("❌ Só quem recebeu a mordida pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu a mordida de {self.quem_mordeu.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_bite))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_mordeu, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Bite(bot))