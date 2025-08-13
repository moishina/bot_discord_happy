import discord
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    async def sincronizar(self, ctx: commands.Context):
        dono_id = 925521235394326538  

        if ctx.author.id != dono_id:
            return await ctx.reply("Apenas o dono do bot pode usar esse comando!")

        try:
            sincs = await self.bot.tree.sync()
            await ctx.reply(f"✅ {len(sincs)} comandos sincronizados com sucesso!")
        except Exception as e:
            await ctx.reply(f"❌ Erro ao sincronizar comandos:\n```{e}```")




async def setup(bot):
    await bot.add_cog(Sync(bot))
