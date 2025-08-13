import discord
from discord import app_commands
from discord.ext import commands
import random

class Clear(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @commands.hybrid_command(name='clear', description='Limpa mensagens do chat (até 100)')
    @app_commands.describe(count='Quantidade de mensagens a deletar (2-100)') #  descricao
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
            if count < 2 or count > 100:
                await ctx.response.send_message("⚠️ Você pode limpar apenas entre 2 e 100 mensagens!", delete_after=8)
                return
        
            await ctx.defer()
            
            await ctx.channel.purge(limit=count+1)
            # await asyncio.sleep(1)
            # await ctx.channel.send(f"{count} mensagens foram deletadas por {ctx.author.mention}!", delete_after=8)
            await ctx.channel.send(f"{count} mensagens foram deletadas por {ctx.author.mention}!", delete_after=8)

    #  erros
    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão pra usar esse comando!", delete_after=8)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Use um número válido. Ex: `.clear 10` ou `/clear amount: 10`", delete_after=8) 
              
# OBS: por algum motivo tem delay para aparecer a mensagem de confirmação de exclusão das mensagens.        
        
 
 
 
async def setup(bot):
    await bot.add_cog(Clear(bot))