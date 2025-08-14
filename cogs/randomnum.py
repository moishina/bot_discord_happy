import discord
from discord import app_commands
from discord.ext import commands
import random

class RandomNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}  #  guarda o número q cada usuário deve adivinhar nessa var 

    @app_commands.command(name="randomnum", description="Jogo de adivinhação de número")
    async def randomnum(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        #  se ja ter um jogo ativo, avisa:
        if user_id in self.active_games:
            await interaction.response.send_message(
                "‼️ Você já tem um jogo ativo! Continue tentando digitando apenas números no chat.",
                ephemeral=True
            )
            return

        #  criando o jogo:
        number = random.randint(1, 100)
        self.active_games[user_id] = number
        await interaction.response.send_message(
            "😼 Pensei em um número entre **1 e 100**! Mande seu palpite. ",
            ephemeral=False
        )
    # evento qnd começar a digitar os numeros no chat para adivinhar
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        #  ignora mensagens do próprio bot
        if message.author.bot:
            return

        user_id = message.author.id

        #  vê se o usuário ta em um jogo ativo
        if user_id in self.active_games:
            content = message.content.strip()

            #  tenta converter a mensagem para número
            if not content.isdigit():
                return  #  ignora se não for número

            guess = int(content)
            correct_number = self.active_games[user_id]

            if guess < correct_number:
                await message.channel.send(f"📤 {message.author.mention}, meu número é **maior**!")
            elif guess > correct_number:
                await message.channel.send(f"📥 {message.author.mention}, meu número é **menor**!")
            else:
                await message.channel.send(
                    f"🎉 {message.author.mention} acertou! O número era **{correct_number}**."
                )
                del self.active_games[user_id]  #  termina o jogo ativo




async def setup(bot):
    await bot.add_cog(RandomNumber(bot))
