import discord
from discord import app_commands
from discord.ext import commands
import random

# ----------------- função de resultado -----------------
def get_rps_result(a: str, b: str) -> int:
    beats = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}
    if a == b:
        return 0
    elif beats[a] == b:
        return 1
    else:
        return 2

# ----------------- view da mensagem principal -----------------
class RPSView(discord.ui.View):
    def __init__(self, author: discord.User, opponent: discord.User, origin_interaction: discord.Interaction):
        super().__init__(timeout=60)
        self.author = author
        self.opponent = opponent
        self.origin_interaction = origin_interaction
        self.choices = {author.id: None, opponent.id: None}

    @discord.ui.button(label="Aceitar Desafio", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            return await interaction.response.send_message("Você não foi convidado pra esse jogo!", ephemeral=True)

        await interaction.response.edit_message(
            content=f"{self.opponent.mention} aceitou o desafio!",
            view=None
        )

        #  envia a mensagem de escolhas para cada jogador de forma privada
        await self.send_choice_buttons(self.origin_interaction, self.author)
        await self.send_choice_buttons(interaction, self.opponent)

    @discord.ui.button(label="Recusar Desafio", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            return await interaction.response.send_message("Você não foi convidado pra esse jogo!", ephemeral=True)

        await interaction.response.edit_message(
            content=f"{self.opponent.mention} recusou o desafio de {self.author.mention}.",
            view=None
        )

    async def send_choice_buttons(self, interaction: discord.Interaction, user: discord.User):
        view = RPSChoiceView(self, user)
        await interaction.followup.send(
            content=f"{user.mention}, escolha sua jogada:",
            ephemeral=True,
            view=view
        )

# ----------------- view de mensagem de escolha -----------------
class RPSChoiceView(discord.ui.View):
    def __init__(self, parent_view: RPSView, user: discord.User):
        super().__init__(timeout=30)
        self.parent_view = parent_view
        self.user = user

    @discord.ui.button(label="🗿 Pedra", style=discord.ButtonStyle.primary)
    async def pedra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "pedra")

    @discord.ui.button(label="📄 Papel", style=discord.ButtonStyle.primary)
    async def papel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "papel")

    @discord.ui.button(label="✂️ Tesoura", style=discord.ButtonStyle.primary)
    async def tesoura(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "tesoura")

    async def make_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user != self.user:
            return await interaction.response.send_message("Essa não é sua vez!", ephemeral=True)

        self.parent_view.choices[self.user.id] = choice
        await interaction.response.send_message(f"Você escolheu **{choice}**!", ephemeral=True)

        if all(self.parent_view.choices.values()):
            await self.declare_winner(interaction)

        self.stop()

    async def declare_winner(self, interaction: discord.Interaction):
        author = self.parent_view.author
        opponent = self.parent_view.opponent
        a_choice = self.parent_view.choices[author.id]
        b_choice = self.parent_view.choices[opponent.id]

        result = get_rps_result(a_choice, b_choice)

        if result == 0:
            outcome = "Empate!"
        elif result == 1:
            outcome = f"{author.mention} venceu!"
        else:
            outcome = f"{opponent.mention} venceu!"

        await interaction.channel.send(
            f"🎮 Resultado do Jogo:\n\n"
            f"→ {author.mention} escolheu **{a_choice}**\n"
            f"→ {opponent.mention} escolheu **{b_choice}**\n\n"
            f"🏆 {outcome}"
        )
        
class Jokenpo(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        

    @app_commands.command(name="jokenpo", description="Desafie alguém para pedra, papel e tesoura!")   
    @app_commands.describe(user="Quem você quer desafiar?")
    async def jokenpo(self, interaction: discord.Interaction, user: discord.Member):
        if user.bot:
            return await interaction.response.send_message("Você não pode desafiar bots!", ephemeral=True)
        if user == interaction.user:
            return await interaction.response.send_message("Você não pode se desafiar!", ephemeral=True)

        view = RPSView(author=interaction.user, opponent=user, origin_interaction=interaction)
        await interaction.response.send_message(
            f"{user.mention}, você foi desafiado por {interaction.user.mention} para uma partida de Pedra, Papel e Tesoura!\nClique abaixo para aceitar ou recusar.",
            view=view
        )    
        
 
 
async def setup(bot):
    await bot.add_cog(Jokenpo(bot))