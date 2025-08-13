import discord
from discord import app_commands
from discord.ext import commands

# Classe dos botões — fora da classe principal para evitar erro de escopo
class AvatarButtons(discord.ui.View):
    def __init__(self, user: discord.User, member: discord.Member):
        super().__init__()
        self.user = user
        self.member = member

    @discord.ui.button(label="Avatar de Usuário", style=discord.ButtonStyle.primary)
    async def avatar_usuario(self, interaction: discord.Interaction, button: discord.ui.Button):
        avatar_url = self.user.avatar.url if self.user.avatar else self.user.default_avatar.url
        embed = discord.Embed(title=f"Avatar de {self.member.display_name}", color=discord.Color.blue())
        embed.set_image(url=avatar_url)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Avatar de Servidor", style=discord.ButtonStyle.secondary)
    async def avatar_servidor(self, interaction: discord.Interaction, button: discord.ui.Button):
        avatar_url = self.member.guild_avatar.url if self.member.guild_avatar else (
            self.user.avatar.url if self.user.avatar else self.user.default_avatar.url
        )
        embed = discord.Embed(title=f"Avatar de servidor de {self.member.display_name}", color=discord.Color.from_rgb(255, 255, 255))
        embed.set_image(url=avatar_url)
        await interaction.response.edit_message(embed=embed, view=self)


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="avatar", description="Mostra o avatar de um usuário (ou o seu)")
    @app_commands.describe(usuario="Pessoa cujo avatar você quer ver")
    async def avatar_command(self, interaction: discord.Interaction, usuario: discord.Member = None):
        member = usuario or interaction.user
        user = member._user if hasattr(member, "_user") else member

        global_avatar = user.avatar.url if user.avatar else user.default_avatar.url
        server_avatar = member.guild_avatar.url if member.guild_avatar else None

        initial_avatar_url = server_avatar or global_avatar
        embed = discord.Embed(title=f"Avatar de {user.name}", color=discord.Color.from_rgb(255, 255, 255))
        embed.set_image(url=initial_avatar_url)

        if server_avatar and server_avatar != global_avatar:
            view = AvatarButtons(user=user, member=member)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed)




async def setup(bot):
    await bot.add_cog(Avatar(bot))
