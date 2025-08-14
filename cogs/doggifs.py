import os
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

DOG_API_KEY = os.getenv("DOG_API_KEY")


class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dog", description="Envia um gif aleatório de cachorrinho! 🐶")
    async def dog(self, interaction: discord.Interaction):
        if not DOG_API_KEY:
            await interaction.response.send_message(
                "⚠️ API Key TheDogAPI não configurada.",
                ephemeral=True
            )
            return

        url = "https://api.thedogapi.com/v1/images/search?mime_types=gif&size=small&limit=1"
        headers = {"x-api-key": DOG_API_KEY}  # variável para a key dos cachorros

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await interaction.response.send_message(
                        "‼️ Não consegui encontrar um gif agora, tente novamente!",
                        ephemeral=True
                    )
                    return

                data = await resp.json()

        #  extrai a URL do GIF
        gif_url = data[0]["url"] if isinstance(data, list) and data else None

        if not gif_url:
            await interaction.response.send_message(
                "🦴 Não achei um gif válido agora. Tenta de novo!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(gif_url)




async def setup(bot):
    await bot.add_cog(Dog(bot))



