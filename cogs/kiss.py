import discord
from discord import app_commands
from discord.ext import commands
import random

class Kiss(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
# # codigo do comando X. para slash commands = @app_commands.command() e usa interaction invés de ctx
    @app_commands.command(name="kiss", description="Beija alguém com estilo (ou o bot...)")   
    @app_commands.describe(user="Quem vai receber o beijo")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        user1 = interaction.user
        user2 = user

        if user1 == user2:
            await interaction.response.send_message("‼️ Você não pode se beijar...", ephemeral=True)
            return

    #  resposta especial se beijar o bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                title="-_-",
                color=discord.Color.from_rgb(158, 242, 255)
        )
            embed.set_image(url="https://i.gifer.com/66ac.gif")
        
            await interaction.response.send_message(embed=embed)
            return

    #  lista de GIFs aleatórios 
        gifs_beijo = [
        "https://i.gifer.com/KTGr.gif",
        "https://media.tenor.com/LOWcGLwNC2AAAAAM/dabi.gif",
        "https://i.gifer.com/8Sbz.gif",
        "https://i.pinimg.com/originals/88/1b/20/881b20d1ff94efbd69594c175597d53d.gif",
        "https://media.tenor.com/qnrnHJojgx8AAAAM/anime-lesbians.gif",
        "https://gifdb.com/images/high/anime-kissing-498-x-280-gif-h9dpoyzyiwm4okco.gif",
        "https://64.media.tumblr.com/5888c0c0592c29d750b3118e3260187e/tumblr_n8ieektmAA1rcv8zio1_500.gif",
        "https://64.media.tumblr.com/386629a5ea2079fb76dfc76e7216dec2/783ccc48501e3d96-b4/s540x810/3fa7d5db78585d42176f9ce4253fa05702be295b.gif",
        "https://64.media.tumblr.com/7e77b6772d0f6b3ce7f991fbcb902514/901973f6353964a3-bd/s540x810/656f303847a829fa52a7a126afd671addfe957cf.gif",
        "https://64.media.tumblr.com/f34fe7b01573743938f30c51d211227e/tumblr_oqgoupiCnF1slt45io1_500.gif",
        "https://gifdb.com/images/high/anime-kissing-498-x-278-gif-srvx1mau6f5dd3kj.gif",
        "https://31.media.tumblr.com/fcbf08c089b113985c9c9329deed735d/tumblr_mjitqkxXr31rjf4f5o1_500.gif",
        "https://gifsec.com/wp-content/uploads/2022/11/love-anime-gif-20.gif",
        "https://i.imgur.com/i3uwlmZ.gif",
        "https://i.pinimg.com/originals/0e/2d/6f/0e2d6f0b9936191a69335a3c68bdfabc.gif",
        "https://i.pinimg.com/originals/0c/af/1c/0caf1cd11ff39a16f0e86b4e9f914b74.gif",
        "https://i.gifer.com/2uEt.gif",
        "https://wethehunted.wordpress.com/wp-content/uploads/2015/11/katanagatari-kiss.gif",
        "https://i.gifer.com/XrqL.gif",
        "https://i.gifer.com/LxDu.gif"
    ]

        gif_escolhido = random.choice(gifs_beijo)

        embed = discord.Embed(
            description=f"💌\u2003{user1.mention} **beijou {user2.mention}!**\n",
            color=discord.Color.pink()
    )
        embed.set_image(url=gif_escolhido)
    
    
#  BOTAO DE RETRIBUIR
        class RetribuirButton(discord.ui.View):
            def __init__(self, quem_beijou: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
                super().__init__(timeout=None)  # botão permanente
                self.quem_beijou = quem_beijou
                self.quem_recebeu = quem_recebeu
                self.combo = combo

            @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
            async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.quem_recebeu.id:
                    await interaction.response.send_message("‼️ Só quem recebeu o beijo pode retribuir!", ephemeral=True)
                    return

                novo_combo = self.combo + 1

                descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o beijo de {self.quem_beijou.mention}!**"
                if novo_combo >= 3:
                    descricao += f"  **(Combo {novo_combo}x!)**"

                novo_embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.pink()
                )
                novo_embed.set_image(url=random.choice(gifs_beijo))

                nova_view = RetribuirButton(self.quem_recebeu, self.quem_beijou, combo=novo_combo)
                await interaction.response.send_message(embed=novo_embed, view=nova_view)

        view = RetribuirButton(user1, user2)
        await interaction.response.send_message(embed=embed, view=view)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Kiss(bot))