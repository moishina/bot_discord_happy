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
            description="""
            
                       `— utilidade: `
                       **/help:**  mostra todos os comandos do bot e suas descrições.
                       **.math ou .m:**  faça cálculos simples com as operações básicas
                       **/avatar:**  mostra o seu avatar de perfil ou avatar do usuário escolhido.
                       **/server_avatar:**  mostra o avatar do servidor.
                       **/clear:**  limpa mensagens do chat (até 100).
                       **.addrole:**  adicione um cargo ao seu perfil! ( apenas adms conseguem usar esse comando ) 
                       **/time:**  divide os membros da call em dois times aleatórios.
                       
                       `— interações: `
                       **/shipp:**  junta dois usuários e dá uma nota de compatibilidade.
                       **/kiss:**  beije um usuário.
                       **/hug:**  abrace um usuário.
                       **/bite:**  dê uma mordida em um usuário.
                       **/slap:**  dê um tapa em um usuário.
                       **/patpat:**  faça carinho em um usuário.
                       **/highfive:**  faça um "bate aqui" com um usuário.
                       **/jokenpo:**  jogue pedra, papel e tesoura com alguém!
                       
                       `— sobre o happy: `
                       **/text:**  envia o texto que for digitado como happy bot.
                       **/amimir:**  happy indo a mimir.
                       **/dance:**  happy dançandinho.

                       `— comandos especiais: `
                       **.r ou "1d20":**  role um dado de qualquer face com ou sem bônus.
                       **/randomnum:**  adivinhe o número!
                       **/cat:**  mande um gif aleatório de gatinho no chat!
                       **/dog:**  mande um gif aleatório de cachorrinho no chat!
                       
                       """,
                       
            color=discord.Color.from_rgb(255,255,255)
            ) 
        await ctx.reply(embed=embed)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Help(bot))
    
