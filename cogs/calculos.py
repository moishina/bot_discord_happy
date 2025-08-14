import discord
from discord.ext import commands

class Calculos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command(aliases=["m"])
    async def math(self, ctx: commands.Context, *, expressao: str):

        try:
            # remove espaços
            expressao = expressao.replace(" ", "")

            if "+" in expressao:
                n1, n2 = expressao.split("+")
                resultado = float(n1) + float(n2)
                operacao = "+"
            elif "-" in expressao:
                n1, n2 = expressao.split("-")
                resultado = float(n1) - float(n2)
                operacao = "-"
            elif "*" in expressao:
                n1, n2 = expressao.split("*")
                resultado = float(n1) * float(n2)
                operacao = "*"
            elif "/" in expressao:
                n1, n2 = expressao.split("/")
                if float(n2) == 0:
                    await ctx.reply("‼️ Não é possível dividir por zero.")
                    return
                resultado = float(n1) / float(n2)
                operacao = "/"
            else:
                await ctx.reply("‼️ Operador inválido! Use +, -, * ou /")
                return
            
            # se for número inteiro, mostrar sem .0
            if resultado.is_integer(): resultado = int(resultado)    
            
            await ctx.reply(f"{n1} {operacao} {n2} = **{resultado}**")

        except ValueError:
            await ctx.reply("‼️ Formato inválido! Ex.: ` !math 5+3 `")

async def setup(bot):
    await bot.add_cog(Calculos(bot))



# import discord
# from discord.ext import commands
# import re

# class Calculos(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

# # função para tratar de ordem de precedencia dos operadores
#     def calcular(self, expr: str):
#         expr = expr.replace(" ", "")  # remove espaços

#         # foca em mult e div primeiro
#         tokens = re.split(r"([*/])", expr)
#         tokens = [t for t in tokens if t]  # remove vazios
#         i = 0
#         while i < len(tokens):
#             if tokens[i] in ['*', '/']:
#                 a = float(tokens[i - 1])
#                 b = float(tokens[i + 1])
#                 if tokens[i] == '*':
#                     res = a * b
#                 elif tokens[i] == '/':
#                     if b == 0:
#                         raise ZeroDivisionError
#                     res = a / b
#                 tokens[i - 1:i + 2] = [str(res)]
#                 i -= 1
#             i += 1
#         expr = "".join(tokens)

#         # dps soma e subtracao
#         tokens = re.split(r"([+\-])", expr)
#         tokens = [t for t in tokens if t]
#         i = 0
#         while i < len(tokens):
#             if tokens[i] in ['+', '-']:
#                 a = float(tokens[i - 1])
#                 b = float(tokens[i + 1])
#                 if tokens[i] == '+':
#                     res = a + b
#                 elif tokens[i] == '-':
#                     res = a - b
#                 tokens[i - 1:i + 2] = [str(res)]
#                 i -= 1
#             i += 1

#         return float(tokens[0])


#     @commands.command()
#     async def math(self, ctx: commands.Context, *, expressao: str):
#         try:
#             expressao_original = expressao.strip()
#             if not re.fullmatch(r"[0-9+\-*/.\s]+", expressao_original):
#                 await ctx.reply("‼️ Expressão inválida! Use apenas números e + - * /")
#                 return

#             resultado = self.calcular(expressao_original)

#             if resultado.is_integer():
#                 resultado = int(resultado)

#             await ctx.reply(f"{expressao_original} = **{resultado}**")

#         except ZeroDivisionError:
#             await ctx.reply("‼️ Não é possível dividir por zero.")
#         except Exception:
#             await ctx.reply("‼️ Erro ao calcular a expressão.")




# async def setup(bot):
#     await bot.add_cog(Calculos(bot))