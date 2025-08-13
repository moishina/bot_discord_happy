import discord
from discord import app_commands
from discord.ext import commands
import random


# lista de respostas com frases e GIFs
respostas = [
    {
        "min": 91,
        "frase": "💖\u2003É o casal dos sonhos! Almas gêmeas confirmadas!",
        "gifs": [
            "https://64.media.tumblr.com/85e8ad832b9826c5a57bf3b5e8addbf9/tumblr_o8qidpQ7oB1uj0rk4o1_540.gif",
            "https://i.gifer.com/Xn.gif",
            "https://i.pinimg.com/originals/51/ab/4b/51ab4baaff2899eae721289e70615851.gif"
        ]
    },
    {
        "min": 71,
        "frase": "💕\u2003Esse casal tem tudo pra dar certo!",
        "gifs": [
            "https://i.pinimg.com/originals/c2/65/d5/c265d5457bf2e9ba76a9c9bf8b58c031.gif",
            "https://media.tenor.com/rZ9d2kPYoUAAAAAd/kaguya-shinomiya.gif"
        ]
    },
    {
        "min": 51,
        "frase": "💞\u2003Um casal ok! Tem química, talvez...",
        "gifs": [
            "https://64.media.tumblr.com/464ac39a4c20594774059d099a54f93e/5e773c36742b70a4-34/s540x810/edfe663bbe29e0e505cae9c80cb8d7bdc4f88d98.gif",
            "https://pa1.aminoapps.com/6411/eabf20824f154125844e475f5356c181d2978770_hq.gif"
        ]
    },
    {
        "min": 31,
        "frase": "💔\u2003Só amizade mesmo... mas vai que né?",
        "gifs": [
            "https://pa1.aminoapps.com/6030/9b9dad5b30dae4cc663613e364dfe165ec35ec66_hq.gif",
            "https://media.tenor.com/lUU2wbgHrioAAAAC/konata-luckystar.gif"
        ]
    },
    {
        "min": 0,
        "frase": "🚫\u2003Melhor deixar quieto...",
        "gifs": [
            "https://steamuserimages-a.akamaihd.net/ugc/436072181609430873/213D4A67E9A330BDF75E36D5941F548B2AF1558D/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false",
            "https://media.tenor.com/9T38EKSwugcAAAAd/anime-hatsune-miku.gif"
        ]
    }
]

class Shipp(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="shipp", description="Junta dois usuários e dá uma nota de casal")   
    @app_commands.describe(user1="Primeira pessoa", user2="Segunda pessoa")
    async def shipp(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        if user1 == user2:
            await interaction.response.send_message("❌ Você não pode shippar a mesma pessoa com ela mesma!", ephemeral=True)
            return

    #  resposta especial se alguém shippar o bot
        if self.bot.user in [user1, user2]:
            outro_usuario = user1 if user2 == self.bot.user else user2
            embed = discord.Embed(
                title="😳",
                color=discord.Color.from_rgb(158, 242, 255)
                )
        
            embed.set_image(url="https://media.tenor.com/KICzsB9HKQYAAAAC/fairy-tail-cat.gif")

            await interaction.response.send_message(embed=embed)
            return

    #  compatibilidade normal
        nota = random.randint(0, 100)
        resposta = next((r for r in respostas if nota >= r["min"]), respostas[-1])
        gif_escolhido = random.choice(resposta["gifs"])

        embed = discord.Embed(
            title="💟\u2003SHIP DETECTOR\u2003💟",
            description=f"""
        ➤\u2003**{user1.mention}** e **{user2.mention}**: `{nota}%` de compatibilidade!
        {resposta['frase']}""",
    
            color=discord.Color.pink()
    )
        embed.set_image(url=gif_escolhido)

        await interaction.response.send_message(embed=embed)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Shipp(bot))