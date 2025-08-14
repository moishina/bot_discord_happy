import discord
from discord import app_commands
from discord.ext import commands
import random

class Hug(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        

    @app_commands.command(name="hug", description="Abrace alguém (ou o bot...)")   
    @app_commands.describe(user="Quem vai receber o abraço")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("‼️ Você não pode se abraçar sozinho...", ephemeral=True)
            return

        #  resposta especial se abraçar o bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                description=f"🥹\u2003{user1.mention} **abraçou {user2.mention}!**\n",
                color=discord.Color.from_rgb(158, 242, 255)
            )
            embed.set_image(url="https://64.media.tumblr.com/95a69094fc81a22ebc4b13339efbc090/tumblr_mkipflKprA1s6slcbo1_500.gif")
            
            await interaction.response.send_message(embed=embed)
            return     
        

        #  lista de GIFs de abraço
        gifs_abraco = [
            "https://media.tenor.com/FgLRE4gi5VoAAAAd/hugs-cute.gif",
            "https://media.tenor.com/BFmsQg9J1ZMAAAAd/chikako-hugging-otohime-for-the-first-and-she-confused.gif",
            "https://media.tenor.com/2HxamDEy7XAAAAAd/yukon-child-form-embracing-ulquiorra.gif",
            "https://media.tenor.com/P-8xYwXoGX0AAAAd/anime-hug-hugs.gif",
            "https://media.tenor.com/J7eGDvGeP9IAAAAd/enage-kiss-anime-hug.gif",
            "https://media.tenor.com/HBTbcCNvLRIAAAAd/syno-i-love-you-syno.gif",
            "https://media.tenor.com/mB_y2KUsyuoAAAAd/cuddle-anime-hug.gif",
            "https://media.tenor.com/ZHeWMKzI39QAAAAd/hug-hugs.gif",
            "https://media.tenor.com/tbzuQSodu58AAAAd/oshi-no-ko-onk.gif",
            "https://media.tenor.com/sl3rfZ7mQBsAAAAd/anime-hug-canary-princess.gif",
            "https://media.tenor.com/Maq1tnCFd2UAAAAd/hug-anime.gif",
            "https://media.tenor.com/0QALoFNm07AAAAAd/kaname-hug-kaname-hug-yuki.gif",
            "https://media.tenor.com/dHn4BG7y014AAAAd/yang-hugs-ruby.gif",
            "https://media.tenor.com/ubTTvDJRtKwAAAAd/sora-no-method-celestial-method.gif"
        ]

        gif_escolhido = random.choice(gifs_abraco)

        embed = discord.Embed(
            description=f"💌\u2003{user1.mention} **abraçou {user2.mention}!**\n",
            color=discord.Color.pink()
        )
        embed.set_image(url=gif_escolhido)

    # botao de retribuir
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_abracou: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_abracou = quem_abracou
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("‼️ Só quem recebeu o abraço pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o abraço de {self.quem_abracou.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_abraco))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_abracou, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Hug(bot))