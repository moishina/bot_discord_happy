import discord
from discord.ext import commands
import random
import re
from collections import defaultdict

class Roll(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
    @commands.command(name="roll", aliases=["r"], description='Role um d20!')   
    async def roll(self, ctx: commands.Context, *, expressao: str):
        expressao_original = expressao
        expressao = expressao.replace(" ", "")

        dados_kh = re.findall(r"(\d+)#(\d*)d(\d+)", expressao)
        dados_normais = re.findall(r"(?<!#)(\d+)d(\d+)", expressao)
        bonus_fixos = re.findall(r"([+-])(\d+)(?!d)", expressao)
        
        if not dados_kh and not dados_normais:
            await ctx.reply("‼️ Expressão inválida! Use algo como 1d20 + 6 ou 2#d20 + 3.")
            return

        mensagens = []
        total_geral = 0
        bonus_total = sum(int(v) if s == "+" else -int(v) for s, v in bonus_fixos)
        bonus_str = "".join(f"{s}{v}" for s, v in bonus_fixos)
        bonus_formatado = f" {bonus_str[0]} {bonus_str[1:]}" if bonus_str else ""

        tem_critico = False
        tem_falha = False

        def to_bold_number(n: int) -> str:
            return ''.join(chr(0x1D7CE + int(d)) for d in str(n))

        # processa dados com #
        for total_str, kh_str, faces_str in dados_kh:
            total = int(total_str)
            keep = int(kh_str) if kh_str else total
            faces = int(faces_str)

            if faces != 20:
                await ctx.reply("❌ O modificador `#` só pode ser usado com dados d20.")
                return

            resultados = [random.randint(1, faces) for _ in range(total)]
            usados = sorted(resultados, reverse=True)[:keep]

            for r in usados:
                bonus_dado_total = 0
                bonus_agrupado = {}

                dados_bônus = re.findall(r"([+-])(\d+)d(\d+)", expressao)
                for s, qtd_str, faces_b in dados_bônus:
                    qtd = int(qtd_str)
                    faces_b = int(faces_b)
                    key = (s, faces_b)
                    if key not in bonus_agrupado:
                        bonus_agrupado[key] = []
                    for _ in range(qtd):
                        val = random.randint(1, faces_b)
                        bonus_agrupado[key].append(val)
                        bonus_dado_total += val if s == "+" else -val

                r_total = r + bonus_dado_total + bonus_total
                total_geral += r_total

                if r == 20:
                    tem_critico = True
                    valor = to_bold_number(20)
                elif r == 1:
                    tem_falha = True
                    valor = to_bold_number(1)
                else:
                    valor = str(r)

                bonus_partes = []
                for (s, faces_b), valores in bonus_agrupado.items():
                    simbolo = "+" if s == "+" else "-"
                    lista_valores = ", ".join(str(v) for v in valores)
                    qtd = len(valores)
                    bonus_partes.append(f"{simbolo} [{lista_valores}] {qtd}d{faces_b}")

                bonus_final = " " + " ".join(bonus_partes) if bonus_partes else ""
                bonus_final += bonus_formatado

                mensagens.append(f"` {str(r_total)} ` ⟵ [{valor}] 1d{faces}{bonus_final}")

        # processa dados normais (multiplicador *N aplica na soma do bloco; não multiplica a quantidade)
        tipo_regex = re.findall(
            r"(\d+)d(\d+)(?:\s*\*\s*(\d+))?(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?(?:\s*\*\s*(\d+))?",
            expressao_original
        )

        # Ajusta multiplicador caso esteja depois do tipo
        tipo_regex = [
            (t[0], t[1], t[2] if t[2] else (t[4] if t[4] else ""), t[3])
            for t in tipo_regex
        ]

        dados_bônus_set = set(re.findall(r"[+-](\d+d\d+)", expressao))
        tipo_regex = [t for t in tipo_regex if not (f"{t[0]}d{t[1]}" in dados_bônus_set and t[3] == "")]

        agrupados = []
        soma_normal = 0
        num_grupos_main = len(tipo_regex)

        for qtd_str, faces_str, mult_str, tipo_dano in tipo_regex:
            qtd = int(qtd_str)
            faces = int(faces_str)
            multiplicador = int(mult_str) if mult_str and faces != 20 else 1

            if f"{qtd}#{faces}" in expressao:
                continue

            tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
            resultados = [random.randint(1, faces) for _ in range(qtd)]
            soma = sum(resultados)
            grupo_total = soma * multiplicador
            soma_normal += grupo_total

            valores_formatados = []
            for x in resultados:
                if x == 20 and faces == 20:
                    tem_critico = True
                    valores_formatados.append(to_bold_number(20))
                elif x == 1 and faces == 20:
                    tem_falha = True
                    valores_formatados.append(to_bold_number(1))
                else:
                    valores_formatados.append(str(x))

            valores = ", ".join(valores_formatados)
            if multiplicador > 1:
                if num_grupos_main == 1:
                    agrupados.append(f"[{valores}] * {multiplicador}")
                else:
                    agrupados.append(f"[{valores}] {qtd}d{faces}{tipo_texto} * {multiplicador}")

            else:
                agrupados.append(f"[{valores}] {qtd}d{faces}{tipo_texto}")

        if agrupados:
            linha = " + ".join(agrupados)

            dados_bônus = re.findall(
                r"([+-])\s*(\d+)d(\d+)(?:\s*\*\s*(\d+))?(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?(?:\s*\*\s*(\d+))?",
                expressao_original
            )

            # Ajusta multiplicador caso esteja depois do tipo nos bônus
            dados_bônus = [
                (b[0], b[1], b[2], b[3] if b[3] else (b[5] if b[5] else ""), b[4])
                for b in dados_bônus
            ]
            
            # Evita duplicar dados já processados no tipo_regex
            tipo_regex_set = {(t[0], t[1], t[2] or "", t[3] or "") for t in tipo_regex}
            dados_bônus = [
                b for b in dados_bônus
                if (b[1], b[2], b[3] or "", b[4] or "") not in tipo_regex_set
            ]          

            bonus_dados_total = 0
            bonus_detalhes = []
            for s, qtd_str, faces_b, mult_str, tipo_dano in dados_bônus:
                qtd = int(qtd_str)
                faces_b = int(faces_b)
                multiplicador = int(mult_str) if mult_str and faces_b != 20 else 1
                rolagens = [random.randint(1, faces_b) for _ in range(qtd)]
                soma_bloco = sum(rolagens) * multiplicador
                tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
                
                if multiplicador > 1:
                    bonus_detalhes.append(
                        f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b}{tipo_texto} * {multiplicador}")

                    
                else:
                    bonus_detalhes.append(
                        f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b}{tipo_texto}"
                    )

                bonus_dados_total += soma_bloco if s == "+" else -soma_bloco

            total_completo = soma_normal + bonus_dados_total + bonus_total
            total_geral += total_completo

            bonus_extra_str = " " + " ".join(bonus_detalhes) if bonus_detalhes else ""
            mensagens.append(f"` {total_completo} ` ⟵ {linha}{bonus_extra_str}{bonus_formatado}")

        mensagem = await ctx.reply("\n".join(mensagens))
    
        if tem_critico:
            await mensagem.add_reaction("😈")
        if tem_falha:
            await mensagem.add_reaction("💀")    

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return
        
        conteudo = message.content.strip()
        # aceita multiplicador antes ou depois do tipo de dano
        pattern_dado = (
            r"^("
            r"\d+#?\d*d\d+"
            r"(?:\s*\*\s*\d+)?"
            r"(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?"
            r"(?:\s*\*\s*\d+)?"
            r"(?:\s*[+\-]\s*\d+#?\d*d\d+"
            r"(?:\s*\*\s*\d+)?"
            r"(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?"
            r"(?:\s*\*\s*\d+)?)*"
            r")(?:\s*[+\-]\s*\d+)?$"
        )

        if re.fullmatch(pattern_dado, conteudo):
            ctx = await self.bot.get_context(message)
            if not ctx.valid:
                await self.roll(ctx, expressao=conteudo)
            return

        await self.bot.process_commands(message)        
 
async def setup(bot):
    await bot.add_cog(Roll(bot))








# import discord
# from discord.ext import commands
# import random
# import re
# from collections import defaultdict

# class Roll(commands.Cog):
#     def __init__(self, bot): #função q vai iniciar qnd for chamada
#         self.bot = bot
#         super().__init__()
        
#     @commands.command(name="roll", aliases=["r"], description='Role um d20!')   
#     async def roll(self, ctx: commands.Context, *, expressao: str):
#         expressao_original = expressao
#         expressao = expressao.replace(" ", "")

#         dados_kh = re.findall(r"(\d+)#(\d*)d(\d+)", expressao)
#         dados_normais = re.findall(r"(?<!#)(\d+)d(\d+)", expressao)
#         bonus_fixos = re.findall(r"([+-])(\d+)(?!d)", expressao)
        
#         if not dados_kh and not dados_normais:
#             await ctx.reply("‼️ Expressão inválida! Use algo como 1d20 + 6 ou 2#d20 + 3.")
#             return

#         mensagens = []
#         total_geral = 0
#         bonus_total = sum(int(v) if s == "+" else -int(v) for s, v in bonus_fixos)
#         bonus_str = "".join(f"{s}{v}" for s, v in bonus_fixos)
#         bonus_formatado = f" {bonus_str[0]} {bonus_str[1:]}" if bonus_str else ""

#         tem_critico = False
#         tem_falha = False

#         def to_bold_number(n: int) -> str:
#             return ''.join(chr(0x1D7CE + int(d)) for d in str(n))

#         # processa dados com #
#         for total_str, kh_str, faces_str in dados_kh:
#             total = int(total_str)
#             keep = int(kh_str) if kh_str else total
#             faces = int(faces_str)

#             if faces != 20:
#                 await ctx.reply("❌ O modificador `#` só pode ser usado com dados d20.")
#                 return

#             resultados = [random.randint(1, faces) for _ in range(total)]
#             usados = sorted(resultados, reverse=True)[:keep]

#             for r in usados:
#                 bonus_dado_total = 0
#                 bonus_agrupado = {}

#                 dados_bônus = re.findall(r"([+-])(\d+)d(\d+)", expressao)
#                 for s, qtd_str, faces_b in dados_bônus:
#                     qtd = int(qtd_str)
#                     faces_b = int(faces_b)
#                     key = (s, faces_b)
#                     if key not in bonus_agrupado:
#                         bonus_agrupado[key] = []
#                     for _ in range(qtd):
#                         val = random.randint(1, faces_b)
#                         bonus_agrupado[key].append(val)
#                         bonus_dado_total += val if s == "+" else -val

#                 r_total = r + bonus_dado_total + bonus_total
#                 total_geral += r_total

#                 if r == 20:
#                     tem_critico = True
#                     valor = to_bold_number(20)
#                 elif r == 1:
#                     tem_falha = True
#                     valor = to_bold_number(1)
#                 else:
#                     valor = str(r)

#                 bonus_partes = []
#                 for (s, faces_b), valores in bonus_agrupado.items():
#                     simbolo = "+" if s == "+" else "-"
#                     lista_valores = ", ".join(str(v) for v in valores)
#                     qtd = len(valores)
#                     bonus_partes.append(f"{simbolo} [{lista_valores}] {qtd}d{faces_b}")

#                 bonus_final = " " + " ".join(bonus_partes) if bonus_partes else ""
#                 bonus_final += bonus_formatado

#                 mensagens.append(f"` {str(r_total)} ` ⟵ [{valor}] 1d{faces}{bonus_final}")

#         # processa dados normais (multiplicador *N aplica na soma do bloco; não multiplica a quantidade)
#         tipo_regex = re.findall(
#             r"(\d+)d(\d+)(?:\s*\*\s*(\d+))?(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?",
#             expressao_original
#         )

#         dados_bônus_set = set(re.findall(r"[+-](\d+d\d+)", expressao))
#         tipo_regex = [t for t in tipo_regex if not (f"{t[0]}d{t[1]}" in dados_bônus_set and t[3] == "")]

#         agrupados = []
#         soma_normal = 0
        
#         # quantidade de grupos "normais" para formatação (decidir quando omitir 2dX)
#         num_grupos_main = len(tipo_regex)

#         for qtd_str, faces_str, mult_str, tipo_dano in tipo_regex:
#             qtd = int(qtd_str)
#             faces = int(faces_str)
#             multiplicador = int(mult_str) if mult_str and faces != 20 else 1  # não aplica * em d20

#             if f"{qtd}#{faces}" in expressao:
#                 continue

#             tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
#             # 🔸 rola somente a quantidade base (qtd), não multiplicada
#             resultados = [random.randint(1, faces) for _ in range(qtd)]
#             soma = sum(resultados)
#             # 🔸 aplica multiplicador na soma do bloco (exceto d20)
#             grupo_total = soma * (multiplicador if faces != 20 else 1)
#             soma_normal += grupo_total

#             valores_formatados = []
#             for x in resultados:
#                 if x == 20 and faces == 20:
#                     tem_critico = True
#                     valores_formatados.append(to_bold_number(20))
#                 elif x == 1 and faces == 20:
#                     tem_falha = True
#                     valores_formatados.append(to_bold_number(1))
#                 else:
#                     valores_formatados.append(str(x))

#             valores = ", ".join(valores_formatados)
#             if multiplicador > 1:
#                 # Se há só um grupo no total, omite "2dX" (ex.: [4, 3] * 2)
#                 if num_grupos_main == 1:
#                     agrupados.append(f"[{valores}] * {multiplicador}")
#                 else:
#                     agrupados.append(f"[{valores}] {qtd}d{faces} * {multiplicador}{tipo_texto}")
#             else:
#                 agrupados.append(f"[{valores}] {qtd}d{faces}{tipo_texto}")

#         if agrupados:
#             linha = " + ".join(agrupados)

#             # bônus de dados (+/- NdX * N) também multiplicam a soma do bloco (exceto d20)
#             dados_bônus = re.findall(
#                 r"([+-])\s*(\d+)d(\d+)(?:\s*\*\s*(\d+))?(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?",
#                 expressao_original
#             )
            
#             # Evita duplicar dados já processados no tipo_regex
#             tipo_regex_set = {(t[0], t[1], t[2] or "", t[3] or "") for t in tipo_regex}

#             dados_bônus = [
#                 b for b in dados_bônus
#                 if (b[1], b[2], b[3] or "", b[4] or "") not in tipo_regex_set
# ]          
            
#             bonus_dados_total = 0
#             bonus_detalhes = []
#             for s, qtd_str, faces_b, mult_str, tipo_dano in dados_bônus:
#                 qtd = int(qtd_str)
#                 faces_b = int(faces_b)
#                 multiplicador = int(mult_str) if mult_str and faces_b != 20 else 1
#                 rolagens = [random.randint(1, faces_b) for _ in range(qtd)]
#                 soma_bloco = sum(rolagens) * (multiplicador if faces_b != 20 else 1)
#                 tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
                
#                 if multiplicador > 1:
#                     bonus_detalhes.append(
#                     f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b} * {multiplicador}{tipo_texto}"
#                 )
#                 else:
#                     bonus_detalhes.append(
#                     f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b}{tipo_texto}"
#                 )

#                 bonus_dados_total += soma_bloco if s == "+" else -soma_bloco

#             total_completo = soma_normal + bonus_dados_total + bonus_total
#             total_geral += total_completo

#             bonus_extra_str = " " + " ".join(bonus_detalhes) if bonus_detalhes else ""
#             mensagens.append(f"` {total_completo} ` ⟵ {linha}{bonus_extra_str}{bonus_formatado}")

#         mensagem = await ctx.reply("\n".join(mensagens))
    
#         if tem_critico:
#             await mensagem.add_reaction("😈")
#         if tem_falha:
#             await mensagem.add_reaction("💀")    

#     @commands.Cog.listener()
#     async def on_message(self, message):
#         if message.author.bot:
#             return
        
#         ctx = await self.bot.get_context(message)
#         if ctx.valid:
#             return
        
#         conteudo = message.content.strip()
#         # aceita multiplicador com ou sem espaço no *N
#         pattern_dado = r"^(\d+#?\d*d\d+(?:\s*\*\s*\d+)?(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?(?:\s*[+\-]\s*\d+#?\d*d\d+(?:\s*\*\s*\d+)?(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?)*)(?:\s*[+\-]\s*\d+)?$"

#         if re.fullmatch(pattern_dado, conteudo):
#             ctx = await self.bot.get_context(message)
#             if not ctx.valid:
#                 await self.roll(ctx, expressao=conteudo)
#             return

#         await self.bot.process_commands(message)        
 
# async def setup(bot):
#     await bot.add_cog(Roll(bot))





