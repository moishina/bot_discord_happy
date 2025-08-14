import discord
from discord.ext import commands

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addrole")
    @commands.has_permissions(administrator=True)  # só adms podem usar o comando
    async def addrole(self, ctx, member: discord.Member, role_name: str, color_hex: str):
        #  remove o "#" do hex se tiver
        if color_hex.startswith("#"):
            color_hex = color_hex[1:]

        try:
            color = discord.Color(int(color_hex, 16))  #  converte hex para cor
        except ValueError:
            await ctx.send("‼️ Cor inválida! Use o formato HEX, ex: ` #FF0000 `.")
            return

        #  tenta ver se tem cargo existente
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        #  qnd n encontra se tem existente, cria o cargo
        if not role:
            try:
                role = await ctx.guild.create_role(name=role_name, colour=color)
                # await ctx.send(f"✅ Cargo `{role_name}` criado com a cor `{color_hex}`.")
            except discord.Forbidden: # tratando erro se n tiver a permissao pra criar cargo
                await ctx.send("‼️ Não tenho permissão para criar cargos.")
                return

        #  add o cargo ao usuario
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ Cargo `{role_name}` adicionado para {member.mention}.")
        except discord.Forbidden: # tratando erro se n tiver a permissao pra add cargos
            await ctx.send("‼️ Não tenho permissão para adicionar cargos.")

    @addrole.error # erros de que precisa ser adm e erros da forma correta de ser digitada
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("‼️ Você precisa ser administrador para usar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("‼️ Uso correto: `.addrole @usuário NomeDoCargo #CorHex`")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(AddRole(bot))
