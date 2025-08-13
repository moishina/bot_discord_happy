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
            await ctx.reply("❌ Expressão inválida! Use algo como 1d20 + 6 ou 2#d20 + 3.")
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

        # processa dados normais
        tipo_regex = re.findall(
            r"(\d+)d(\d+)(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?", expressao_original)

        dados_bônus_set = set(re.findall(r"[+-](\d+d\d+)", expressao))
        tipo_regex = [t for t in tipo_regex if f"{t[0]}d{t[1]}" not in dados_bônus_set]

        agrupados = []
        soma_normal = 0
        

        for qtd_str, faces_str, tipo_dano in tipo_regex:
            qtd = int(qtd_str)
            faces = int(faces_str)

            if f"{qtd}#{faces}" in expressao:
                continue

            tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
            resultados = [random.randint(1, faces) for _ in range(qtd)]
            soma = sum(resultados)
            soma_normal += soma

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
            agrupados.append(f"[{valores}] {qtd}d{faces}{tipo_texto}")

        if agrupados:
            linha = " + ".join(agrupados)

            # inclui bônus de dados extras no total
            # dados_bônus = re.findall(r"([+-])(\d+)d(\d+)", expressao)
            # bonus_dados_total = 0
            # bonus_detalhes = []
            # for s, qtd_str, faces_b in dados_bônus:
            #     qtd = int(qtd_str)
            #     faces_b = int(faces_b)
            #     rolagens = [random.randint(1, faces_b) for _ in range(qtd)]
            #     bonus_detalhes.append(f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b}")
            #     bonus_dados_total += sum(rolagens) if s == "+" else -sum(rolagens)
            
            # inclui bônus de dados extras no total (preservando o tipo de dano)
            dados_bônus = re.findall(r"([+-])\s*(\d+)d(\d+)(?:\s+([a-zA-ZÀ-ÖØ-öø-ÿ]+))?", expressao_original)
            bonus_dados_total = 0
            bonus_detalhes = []
            for s, qtd_str, faces_b, tipo_dano in dados_bônus:
                qtd = int(qtd_str)
                faces_b = int(faces_b)
                rolagens = [random.randint(1, faces_b) for _ in range(qtd)]
                tipo_texto = f" {tipo_dano}" if tipo_dano else ""
                bonus_detalhes.append(f"{s} [{', '.join(map(str, rolagens))}] {qtd}d{faces_b}{tipo_texto}")
                bonus_dados_total += sum(rolagens) if s == "+" else -sum(rolagens)


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
        pattern_dado = r"^(\d+#?\d*d\d+(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?(?:\s*[+\-]\s*\d+#?\d*d\d+(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?)*)(?:\s*[+\-]\s*\d+)?$"

        if re.fullmatch(pattern_dado, conteudo):
            ctx = await self.bot.get_context(message)
            if not ctx.valid:
                await self.roll(ctx, expressao=conteudo)
            return

        await self.bot.process_commands(message)        
 
async def setup(bot):
    await bot.add_cog(Roll(bot))
