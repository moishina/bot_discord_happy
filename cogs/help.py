import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
# codigo do comando help. para slash commands = @app_commands.command() e usa interaction invés de ctx
    @commands.hybrid_command(name="help", description='Lista de comandos e suas descrições!')   
    async def help(self, ctx:commands.Context):
        embed = discord.Embed(
            title=f"— lista de comandos e descrições: ",
            description="""**/avatar** — mostra o seu avatar de perfil ou avatar do usuário escolhido.
                       **/server_icon** — mostra o avatar do servidor.
                       **/roll ou .r** — role um dado de qualquer face com, ou sem bônus.
                       **/clear ou .clear** — limpa mensagens do chat (até 100). 
                       **/jokenpo** — jogue pedra, papel e tesoura com alguém!
                       **/time** — divide os membros da call em dois times aleatórios.
                       **/shipp** — junta dois usuários e dá uma nota de compatibilidade.
                       **/kiss** — beije um usuário.
                       **/hug** — abrace um usuário.
                       **/bite** — dê uma mordida em um usuário.
                       **/slap** — dê um tapa em um usuário.
                       **/patpat** — faça carinho em um usuário.
                       **/highfive** — faça um "bate aqui" com um usuário.
                       **/text** — envia o texto que for digitado como Happy.
                       **/amimir** — happy indo a mimir.
                       **/dance** — happy dançandinho.
                       
                       """,
                       
            color=discord.Color.from_rgb(255,255,255)
            ) 
        await ctx.reply(embed=embed)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Help(bot))
    
