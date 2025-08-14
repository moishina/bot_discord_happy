import discord
from discord import app_commands
from discord.ext import commands
import random

class PatPat(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
# # codigo do comando X. para slash commands = @app_commands.command() e usa interaction invés de ctx
    @app_commands.command(name="patpat", description="Faz carinho em alguém (ou no bot...)")   
    @app_commands.describe(user="Quem vai receber o carinho")
    async def patpat(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("‼️ Você não pode fazer patpat em si mesmo(a)!...", ephemeral=True)
            return

        #  resposta especial se fazer carinho no bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                color=discord.Color.from_rgb(158, 242, 255)
            )
            embed.set_image(url="https://giffiles.alphacoders.com/141/141690.gif")
            
            await interaction.response.send_message(embed=embed)
            return

        #  lista de GIFs aleatórios 
        gifs_patpat = [
            "https://i.pinimg.com/originals/4c/03/bb/4c03bbe17bc0825e064d049c5f8262f3.gif",
            "https://i.pinimg.com/originals/f4/1b/39/f41b3974036070fd1c498acf17a3a42e.gif",
            "https://imgur.com/q31lv2t.gif",
            "https://imgur.com/9TdPHN8.gif",
            "https://imgur.com/OrUiyCp.gif",
            "https://media.tenor.com/f5asRSsfl-wAAAAM/good-boy-pat-on-head.gif",
            "https://i0.wp.com/images.wikia.com/adventuretimewithfinnandjake/images/2/2e/Jake_pat.gif",
            "https://static.wikia.nocookie.net/shipping/images/d/dd/ZoNa_Zou_arc.gif",
            "https://imgur.com/qdMIRpZ.gif",
            "https://imgur.com/25PNMah.gif"
            ]

        gif_escolhido = random.choice(gifs_patpat)

        embed = discord.Embed(
            description=f"💌\u2003{user1.mention} **fez patpat em {user2.mention}!**\n",
            color=discord.Color.pink()
        )
        embed.set_image(url=gif_escolhido)
        
        
    #  BOTAO DE RETRIBUIR
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_fezpatpat: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_fezpatpat = quem_fezpatpat
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("‼️ Só quem recebeu o patpat pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o patpat de {self.quem_fezpatpat.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_patpat))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_fezpatpat, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(PatPat(bot))




