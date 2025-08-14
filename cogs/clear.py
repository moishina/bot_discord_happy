import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

class Clear(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name='clear', description='Limpa mensagens do chat (até 100)')  # comando apenas slash
    @app_commands.describe(count='Quantidade de mensagens a deletar (2-100)') #  descricao
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, count: int):
            if count < 2 or count > 100:
                await interaction.response.send_message("⚠️ Você pode limpar apenas entre 2 e 100 mensagens!", ephemeral=True)
                return
            # defer pra evitar erro de timeout
            await interaction.response.defer(ephemeral=True)
            
            # slash command n cria mensagem no chat, então n soma +1(?)
            deleted = await interaction.channel.purge(limit=count, reason=f"Solicitado por {interaction.user}")
            
            # envia confirmação visível no canal. (WebhookMessage não aceita delete_after)
            confirm_msg = await interaction.followup.send(
                f"{len(deleted)} mensagens foram deletadas por {interaction.user.mention}!"
            )

            #  followup.send n aceita delete_after, apagamos manualmente após 8s:
            async def _auto_delete(msg, delay: int = 8):
                try:
                    await asyncio.sleep(delay)
                    await msg.delete()
                except discord.HTTPException:
                    pass

            asyncio.create_task(_auto_delete(confirm_msg))

    #  erros
    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error):
        # Se já houve resposta (defer ou send), use followup; senão, use response.send_message
        responder = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message

        if isinstance(error, app_commands.MissingPermissions):
            await responder("‼️ Você não tem permissão pra usar esse comando!", ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            await responder("‼️ Use um número válido entre 2 e 100.", ephemeral=True) 
        else:
            # Opcional: logar/printar outros erros
            try:
                await responder("‼️ Ocorreu um erro ao executar o comando.", ephemeral=True)
            except discord.InteractionResponded:
                #  se por algum motivo já respondeu, ignore
                pass
              
# OBS: por algum motivo tem delay para aparecer a mensagem de confirmação de exclusão das mensagens.        
        
 
 
 
async def setup(bot):
    await bot.add_cog(Clear(bot))