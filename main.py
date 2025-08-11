import discord
from discord.ext import commands
from discord import app_commands
import random
import re
from collections import defaultdict
# ( all ) todas as permissoes q o bot precisa guardado na var intents

# intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all()) # prefix
# intents.members = True  # necessário para pegar os membros do canal de voz
bot.remove_command("help")
# tree = bot.tree # acessa a arvore de comandos

@bot.event # eventos são ativos qnd algo especifico acontece
async def on_ready(): # qnd o bot estiver pronto
    await bot.tree.sync()
    # enviar_mensagem.start()
    print('—————————————————————————————————————————————————\nBOT INICIALIZADO COM SUCESSO!\n')
    
    # status do bot
    activity = discord.Activity(type=discord.ActivityType.watching, name="Fairy Tail")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
# jogando
# activity = discord.Game(name="Crosscode")  

# Ouvindo
# discord.Activity(type=discord.ActivityType.listening, name="música boa")

# Transmitindo (streaming) — aparece roxinho
# discord.Streaming(name="meu gameplay", url="https://twitch.tv/seulink")


#  COMANDO DE HELP ( VER OS COMANDOS DO BOT )
@bot.hybrid_command(name="help", description='Lista de comandos e suas descrições!')
async def help(ctx):
    embed = discord.Embed(
        title=f"— lista de comandos e descrições: ",
        description="""**/avatar** — mostra o seu avatar de perfil ou avatar do usuário escolhido.
                       **/server_icon** — mostra o avatar do servidor.
                       **/roll ou .r** — role um dado de qualquer face com, ou sem bônus.
                       **/clear ou .clear** — limpa mensagens do chat (até 100). 
                       **/jokenpo — jogue pedra, papel e tesoura com alguém!
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


#  COMANDO DE MOSTRAR O AVATAR
#  classe que representa os botões que serão exibidos no embed
class AvatarButtons(discord.ui.View):
    def __init__(self, user: discord.User, member: discord.Member):
        super().__init__()  # Inicializa a View (estrutura de UI do Discord)
        self.user = user    # Avatar global do usuário (fora do servidor)
        self.member = member  # Avatar de servidor (caso o usuário tenha um diferente aqui)

    #  botão que mostra o avatar global do usuário (aquele que aparece fora do servidor)
    @discord.ui.button(label="Avatar de Usuário", style=discord.ButtonStyle.primary)
    async def avatar_usuario(self, interaction: discord.Interaction, button: discord.ui.Button):
        #  verifica se o usuário tem avatar global, senão usa o avatar padrão do Discord
        avatar_url = self.user.avatar.url if self.user.avatar else self.user.default_avatar.url
        #  cria um embed com o avatar global
        embed = discord.Embed(title=f"Avatar de {self.user.name}", color=discord.Color.blue())
        embed.set_image(url=avatar_url)
        #  atualiza a mensagem com o embed novo e mantém os botões
        await interaction.response.edit_message(embed=embed, view=self)

    #  botão que mostra o avatar usado especificamente neste servidor
    @discord.ui.button(label="Avatar de Servidor", style=discord.ButtonStyle.secondary)
    async def avatar_servidor(self, interaction: discord.Interaction, button: discord.ui.Button):
        #  se o usuário tiver avatar de servidor, usa ele; senão, usa o avatar global ou padrão
        avatar_url = self.member.guild_avatar.url if self.member.guild_avatar else (self.user.avatar.url if self.user.avatar else self.user.default_avatar.url)
        #  cria um embed com o avatar de servidor
        embed = discord.Embed(title=f"Avatar de Servidor de {self.member.display_name}", color=discord.Color.green())
        embed.set_image(url=avatar_url)
        #  atualiza a mensagem com o embed novo e mantém os botões
        await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(name="avatar", description="Mostra o avatar de um usuário (ou o seu)")
@app_commands.describe(usuario="Pessoa cujo avatar você quer ver")
async def avatar_command(interaction: discord.Interaction, usuario: discord.Member = None):
    #  se não for passado ninguém, usa quem executou o comando
    member = usuario or interaction.user
    #  acessa o objeto de usuário "global" (fora do servidor), compatível com alguns casos internos
    user = member._user if hasattr(member, "_user") else member

    #  pega o link do avatar global (ou padrão, se não tiver)
    global_avatar = user.avatar.url if user.avatar else user.default_avatar.url
    #  pega o link do avatar de servidor (se tiver um diferente configurado com Nitro)
    server_avatar = member.guild_avatar.url if member.guild_avatar else None

    #  escolhe o avatar inicial a ser mostrado — prioriza o avatar de servidor, se existir
    initial_avatar_url = server_avatar or global_avatar
    embed = discord.Embed(title=f"avatar de {user.name}", color=discord.Color.from_rgb(255, 255, 255))
    embed.set_image(url=initial_avatar_url)

    #  se o avatar de servidor for diferente do global, exibe os botões para alternar entre eles
    if server_avatar and server_avatar != global_avatar:
        view = AvatarButtons(user=user, member=member)
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # Se não tiver avatar de servidor ou for igual ao global, só mostra o embed simples
        await interaction.response.send_message(embed=embed)



#  COMANDO DE MOSTRAR AVATAR DO SERVIDOR
@bot.tree.command(name="server_icon", description="Mostra o ícone do servidor")
async def server_icon(interaction: discord.Interaction):
    guild = interaction.guild
    if guild.icon:
        embed = discord.Embed(
            title=f"avatar do servidor '{guild.name}'",
            color=discord.Color.from_rgb(255,255,255)
        )
        embed.set_image(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Este servidor não tem ícone.", ephemeral=True)



#  COMANDO DE ROLL
@bot.hybrid_command(name="roll", aliases=["r"], description='Role um d20!')
async def roll(ctx: commands.Context, *, expressao: str):
    expressao_original = expressao  # preserva para detectar tipo de dano
    expressao = expressao.replace(" ", "")

    # capta dados com o mod '#' \d+ nº de dados, #(\d*) qnts manter (kh), d(\d+) quantas faces
    dados_kh = re.findall(r"(\d+)#(\d*)d(\d+)", expressao)
    dados_normais = re.findall(r"(?<!#)(\d+)d(\d+)", expressao)
    bonus = re.findall(r"([+-])(\d+)(?!d)", expressao)
    
    # verifica se n encontrou nenhum dado válido
    if not dados_kh and not dados_normais:
        await ctx.reply("❌ Expressão inválida! Use algo como 1d20 + 6 ou 2#d20 + 3.")
        return

    # armazena as mensagens de resultado e soma final de tds as rolagens
    mensagens = []
    total_geral = 0
    # constrói o valor total do bônus (bonus_total) e tbm a string formatada para exibir o bônus, como + 5
    bonus_total = sum(int(v) if s == "+" else -int(v) for s, v in bonus)
    bonus_str = "".join(f"{s}{v}" for s, v in bonus)
    bonus_formatado = f" {bonus_str[0]} {bonus_str[1:]}" if bonus_str else ""

    # flags q serao ativadas se houver (20) critico ou (1) falha
    tem_critico = False
    tem_falha = False

    # transforma 20 em bold
    def to_bold_number(n: int) -> str:
        return ''.join(chr(0x1D7CE + int(d)) for d in str(n))

    # para cada grupo de d20 com #
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
            bonus_agrupado = {}  # tipo: {("+", 6): [4, 6], ("-", 4): [3]}

            # Busca e aplica bônus de dados extras (ex: +1d4, -1d6)
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



            # Aplica bônus fixos (ex: +5, -3)
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



    # Agrupamento por tipo de dano (após todos os d20 processados)
    tipo_regex = re.findall(r"(\d+)d(\d+)(?:\s+([a-zA-ZçÇáéíóúãõâêôê]+))?", expressao_original)
    
    # Remove dados bônus já usados no bloco com #
    dados_bônus_set = set(re.findall(r"[+-](\d+d\d+)", expressao))
    tipo_regex = [t for t in tipo_regex if f"{t[0]}d{t[1]}" not in dados_bônus_set]


    agrupados = []
    soma_normal = 0

    for qtd_str, faces_str, tipo_dano in tipo_regex:
        qtd = int(qtd_str)
        faces = int(faces_str)

        # Skip if already handled in dados_kh
        if f"{qtd}#{faces}" in expressao:
            continue

        tipo_texto = f" ({tipo_dano})" if tipo_dano else ""
        resultados = [random.randint(1, faces) for _ in range(qtd)]
        soma = sum(resultados)
        soma_normal += soma

        #  aplica bold ao 20 e 1 nos dados d20 normais
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
        total_com_bonus = soma_normal + bonus_total
        total_geral += total_com_bonus
        mensagens.append(f" {total_com_bonus}  ⟵ {linha}{bonus_formatado}")

######################################

#  botao de reroll
    class RerollButton(discord.ui.View):
        def __init__(self, original_expressao: str, autor_id: int):
            super().__init__()
            self.original_expressao = original_expressao
            self.autor_id = autor_id

        @discord.ui.button(label="🔄 Re-roll", style=discord.ButtonStyle.secondary)
        async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.autor_id:
                await interaction.response.send_message("❌ Apenas quem rolou pode rerrolar!", ephemeral=True)
                return
            await interaction.response.defer()
            await roll.callback(ctx, expressao=self.original_expressao)

    apenas_d20 = all(int(f) == 20 for _, _, f in dados_kh) and all(int(f) == 20 for _, f in dados_normais)
    view = RerollButton(expressao_original, ctx.author.id) if apenas_d20 and (dados_kh or dados_normais) else None

###
    mensagem = await ctx.reply("\n".join(mensagens), view=view)
    

# reagir qnd vier 1 ou 20
    if tem_critico:
        await mensagem.add_reaction("😈")
    if tem_falha:
        await mensagem.add_reaction("💀")
        
@bot.event
async def on_message(message):
    # Ignora qualquer mensagem enviada por bots (incluindo ele mesmo)
    if message.author.bot:
        return

    conteudo = message.content.strip()  # Remove espaços extras no início/fim da mensagem

    #  regex que detecta apenas mensagens contendo expressões de dados
    # Ex: "1d20 + 4", "2#d20 + 1", "1d8 fogo + 2d6"
    pattern_dado = r"^(\d+#?\d*d\d+(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?(?:\s*[\+\-]\s*\d+#?\d*d\d+(?:\s*[a-zA-ZçÇáéíóúãõâêôê]+)?)*)\s*(?:[\+\-]\s*\d+)?$"


    #  regex para detectar apenas expressões matemáticas puras (sem letras ou frases misturadas)
    # Agora suporta: + - * / . e () para parênteses
    pattern_soma = r"^[\d\s\+\-\*/\.\(\)]+$"

    #  verifica se a mensagem bate com o padrão de rolagem de dados
    if re.fullmatch(pattern_dado, conteudo):
        ctx = await bot.get_context(message)

        #  se a mensagem NÃO for um comando com prefixo (.r, .somar, etc.)
        if not ctx.valid:
            await roll(ctx, expressao=conteudo)
        return

    #  ----verifica se a mensagem é uma expressão matemática válida (soma, subtração, etc.)
    elif re.fullmatch(pattern_soma, conteudo):
        ctx = await bot.get_context(message)

        if not ctx.valid:
            #  remove qualquer caractere que não seja número ou operador
            expressao_limpa = re.sub(r"[^\d\+\-\*/\.\(\)]", "", conteudo)

            #  função auxiliar para converter número para fonte bold unicode (igual à usada em rolagens)
            def to_bold_number(n: float) -> str:
                return ''.join(chr(0x1D7CE + int(d)) for d in str(int(n))) if n == int(n) else f"{n:.2f}"

            try:
                #  executa a expressão com segurança (eval avalia a conta)
                resultado = eval(expressao_limpa)
                resultado_bold = to_bold_number(resultado)

                #  formata visualmente com ANSI: expressão em cinza e resultado em azul negrito
                descricao = f"```ansi\n[90m{conteudo}[0m → [35m{resultado_bold}[0m\n```"

                embed = discord.Embed(
                    description=descricao,
                    color=discord.Color.from_rgb(255, 255, 255)  # Cor da borda do embed
                )

                await message.reply(embed=embed)

            except:
                #  se algo der errado na conta, exibe erro
                await message.reply("❌ Expressão inválida! Ex: `2 + 3 * 4`")
        return

    #  se a mensagem não for nem expressão de dado nem soma, segue para processar comandos normalmente
    await bot.process_commands(message)


##############
#  COMANDO DE PEDRA / PAPEL / TESOURA
# ----------------- função de resultado -----------------
def get_rps_result(a: str, b: str) -> int:
    beats = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}
    if a == b:
        return 0
    elif beats[a] == b:
        return 1
    else:
        return 2

# ----------------- view da mensagem principal -----------------
class RPSView(discord.ui.View):
    def __init__(self, author: discord.User, opponent: discord.User, origin_interaction: discord.Interaction):
        super().__init__(timeout=60)
        self.author = author
        self.opponent = opponent
        self.origin_interaction = origin_interaction
        self.choices = {author.id: None, opponent.id: None}

    @discord.ui.button(label="Aceitar Desafio", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            return await interaction.response.send_message("Você não foi convidado pra esse jogo!", ephemeral=True)

        await interaction.response.edit_message(
            content=f"{self.opponent.mention} aceitou o desafio!",
            view=None
        )

        #  envia a mensagem de escolhas para cada jogador de forma privada
        await self.send_choice_buttons(self.origin_interaction, self.author)
        await self.send_choice_buttons(interaction, self.opponent)

    @discord.ui.button(label="Recusar Desafio", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            return await interaction.response.send_message("Você não foi convidado pra esse jogo!", ephemeral=True)

        await interaction.response.edit_message(
            content=f"{self.opponent.mention} recusou o desafio de {self.author.mention}.",
            view=None
        )

    async def send_choice_buttons(self, interaction: discord.Interaction, user: discord.User):
        view = RPSChoiceView(self, user)
        await interaction.followup.send(
            content=f"{user.mention}, escolha sua jogada:",
            ephemeral=True,
            view=view
        )

# ----------------- view de mensagem de escolha -----------------
class RPSChoiceView(discord.ui.View):
    def __init__(self, parent_view: RPSView, user: discord.User):
        super().__init__(timeout=30)
        self.parent_view = parent_view
        self.user = user

    @discord.ui.button(label="🗿 Pedra", style=discord.ButtonStyle.primary)
    async def pedra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "pedra")

    @discord.ui.button(label="📄 Papel", style=discord.ButtonStyle.primary)
    async def papel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "papel")

    @discord.ui.button(label="✂️ Tesoura", style=discord.ButtonStyle.primary)
    async def tesoura(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.make_choice(interaction, "tesoura")

    async def make_choice(self, interaction: discord.Interaction, choice: str):
        if interaction.user != self.user:
            return await interaction.response.send_message("Essa não é sua vez!", ephemeral=True)

        self.parent_view.choices[self.user.id] = choice
        await interaction.response.send_message(f"Você escolheu **{choice}**!", ephemeral=True)

        if all(self.parent_view.choices.values()):
            await self.declare_winner(interaction)

        self.stop()

    async def declare_winner(self, interaction: discord.Interaction):
        author = self.parent_view.author
        opponent = self.parent_view.opponent
        a_choice = self.parent_view.choices[author.id]
        b_choice = self.parent_view.choices[opponent.id]

        result = get_rps_result(a_choice, b_choice)

        if result == 0:
            outcome = "Empate!"
        elif result == 1:
            outcome = f"{author.mention} venceu!"
        else:
            outcome = f"{opponent.mention} venceu!"

        await interaction.channel.send(
            f"🎮 Resultado do Jogo:\n\n"
            f"→ {author.mention} escolheu **{a_choice}**\n"
            f"→ {opponent.mention} escolheu **{b_choice}**\n\n"
            f"🏆 {outcome}"
        )

# ----------------- o slash command -----------------
@bot.tree.command(name="jokenpo", description="Desafie alguém para pedra, papel e tesoura!")
@app_commands.describe(user="Quem você quer desafiar?")
async def jokenpo(interaction: discord.Interaction, user: discord.Member):
    if user.bot:
        return await interaction.response.send_message("Você não pode desafiar bots!", ephemeral=True)
    if user == interaction.user:
        return await interaction.response.send_message("Você não pode se desafiar!", ephemeral=True)

    view = RPSView(author=interaction.user, opponent=user, origin_interaction=interaction)
    await interaction.response.send_message(
        f"{user.mention}, você foi desafiado por {interaction.user.mention} para uma partida de Pedra, Papel e Tesoura!\nClique abaixo para aceitar ou recusar.",
        view=view
    )
##############



#  COMANDO DE SEPARAR TIMES
@bot.tree.command(name="time", description="Divide os membros do canal de voz em dois times aleatórios.")
async def time(interaction: discord.Interaction):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("Você precisa estar em um canal de voz pra usar esse comando!", ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel
    members = [member for member in voice_channel.members if not member.bot]

    if len(members) < 2:
        await interaction.response.send_message("Precisa ter pelo menos 2 pessoas no canal de voz pra formar times!", ephemeral=True)
        return

    random.shuffle(members)
    half = len(members) // 2
    time1 = members[:half]
    time2 = members[half:]

    def format_team(team):
        return '\n'.join(member.display_name for member in team)

    mensagem = (
        f"🎮 **Times formados!** 🎮\n\n"
        f"🔵 **Time 1:**\n{format_team(time1)}\n\n"
        f"🔴 **Time 2:**\n{format_team(time2)}"
    )
    await interaction.response.send_message(mensagem)



#  COMANDO DE SHIPPAR
# lista de respostas com frases e GIFs
respostas = [
    {
        "min": 91,
        "frase": "💖\u2003É o casal dos sonhos! Almas gêmeas confirmadas!",
        "gifs": [
            "https://64.media.tumblr.com/85e8ad832b9826c5a57bf3b5e8addbf9/tumblr_o8qidpQ7oB1uj0rk4o1_540.gif",
            "https://i.gifer.com/Xn.gif",
            "https://i.pinimg.com/originals/51/ab/4b/51ab4baaff2899eae721289e70615851.gif"
        ]
    },
    {
        "min": 71,
        "frase": "💕\u2003Esse casal tem tudo pra dar certo!",
        "gifs": [
            "https://i.pinimg.com/originals/c2/65/d5/c265d5457bf2e9ba76a9c9bf8b58c031.gif",
            "https://media.tenor.com/rZ9d2kPYoUAAAAAd/kaguya-shinomiya.gif"
        ]
    },
    {
        "min": 51,
        "frase": "💞\u2003Um casal ok! Tem química, talvez...",
        "gifs": [
            "https://64.media.tumblr.com/464ac39a4c20594774059d099a54f93e/5e773c36742b70a4-34/s540x810/edfe663bbe29e0e505cae9c80cb8d7bdc4f88d98.gif",
            "https://pa1.aminoapps.com/6411/eabf20824f154125844e475f5356c181d2978770_hq.gif"
        ]
    },
    {
        "min": 31,
        "frase": "💔\u2003Só amizade mesmo... mas vai que né?",
        "gifs": [
            "https://pa1.aminoapps.com/6030/9b9dad5b30dae4cc663613e364dfe165ec35ec66_hq.gif",
            "https://media.tenor.com/lUU2wbgHrioAAAAC/konata-luckystar.gif"
        ]
    },
    {
        "min": 0,
        "frase": "🚫\u2003Melhor deixar quieto...",
        "gifs": [
            "https://steamuserimages-a.akamaihd.net/ugc/436072181609430873/213D4A67E9A330BDF75E36D5941F548B2AF1558D/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false",
            "https://media.tenor.com/9T38EKSwugcAAAAd/anime-hatsune-miku.gif"
        ]
    }
]

@bot.tree.command(name="shipp", description="Junta dois usuários e dá uma nota de casal")
@app_commands.describe(user1="Primeira pessoa", user2="Segunda pessoa")
async def shipp(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode shippar a mesma pessoa com ela mesma!", ephemeral=True)
        return

    #  resposta especial se alguém shippar o bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            title="😳",
            color=discord.Color.from_rgb(158, 242, 255)
            )
        
        embed.set_image(url="https://media.tenor.com/KICzsB9HKQYAAAAC/fairy-tail-cat.gif")

        await interaction.response.send_message(embed=embed)
        return

    #  compatibilidade normal
    nota = random.randint(0, 100)
    resposta = next((r for r in respostas if nota >= r["min"]), respostas[-1])
    gif_escolhido = random.choice(resposta["gifs"])

    embed = discord.Embed(
        title="💟\u2003SHIP DETECTOR\u2003💟",
        description=f"""
    ➤\u2003**{user1.mention}** e **{user2.mention}**: `{nota}%` de compatibilidade!
    {resposta['frase']}""",
    
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)

    await interaction.response.send_message(embed=embed)



#  COMANDO KISS
@bot.tree.command(name="kiss", description="Beija alguém com estilo (ou o bot...)")
@app_commands.describe(user="Quem vai receber o beijo")
async def kiss(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode se beijar...", ephemeral=True)
        return

    #  resposta especial se beijar o bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            title="-_-",
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://i.gifer.com/66ac.gif")
        
        await interaction.response.send_message(embed=embed)
        return

    #  lista de GIFs aleatórios 
    gifs_beijo = [
        "https://i.gifer.com/KTGr.gif",
        "https://media.tenor.com/LOWcGLwNC2AAAAAM/dabi.gif",
        "https://i.gifer.com/8Sbz.gif",
        "https://i.pinimg.com/originals/88/1b/20/881b20d1ff94efbd69594c175597d53d.gif",
        "https://media.tenor.com/qnrnHJojgx8AAAAM/anime-lesbians.gif",
        "https://gifdb.com/images/high/anime-kissing-498-x-280-gif-h9dpoyzyiwm4okco.gif",
        "https://64.media.tumblr.com/5888c0c0592c29d750b3118e3260187e/tumblr_n8ieektmAA1rcv8zio1_500.gif",
        "https://64.media.tumblr.com/386629a5ea2079fb76dfc76e7216dec2/783ccc48501e3d96-b4/s540x810/3fa7d5db78585d42176f9ce4253fa05702be295b.gif",
        "https://64.media.tumblr.com/7e77b6772d0f6b3ce7f991fbcb902514/901973f6353964a3-bd/s540x810/656f303847a829fa52a7a126afd671addfe957cf.gif",
        "https://64.media.tumblr.com/f34fe7b01573743938f30c51d211227e/tumblr_oqgoupiCnF1slt45io1_500.gif",
        "https://gifdb.com/images/high/anime-kissing-498-x-278-gif-srvx1mau6f5dd3kj.gif",
        "https://31.media.tumblr.com/fcbf08c089b113985c9c9329deed735d/tumblr_mjitqkxXr31rjf4f5o1_500.gif",
        "https://gifsec.com/wp-content/uploads/2022/11/love-anime-gif-20.gif",
        "https://i.imgur.com/i3uwlmZ.gif",
        "https://i.pinimg.com/originals/0e/2d/6f/0e2d6f0b9936191a69335a3c68bdfabc.gif",
        "https://i.pinimg.com/originals/0c/af/1c/0caf1cd11ff39a16f0e86b4e9f914b74.gif",
        "https://i.gifer.com/2uEt.gif",
        "https://wethehunted.wordpress.com/wp-content/uploads/2015/11/katanagatari-kiss.gif",
        "https://i.gifer.com/XrqL.gif",
        "https://i.gifer.com/LxDu.gif"
    ]

    gif_escolhido = random.choice(gifs_beijo)

    embed = discord.Embed(
        description=f"💌\u2003{user1.mention} **beijou {user2.mention}!**\n",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)
    
    
#  BOTAO DE RETRIBUIR
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_beijou: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_beijou = quem_beijou
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu o beijo pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o beijo de {self.quem_beijou.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_beijo))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_beijou, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)

    

#  COMANDO ABRAÇAR
@bot.tree.command(name="hug", description="Abrace alguém (ou o bot...)")
@app_commands.describe(user="Quem vai receber o abraço")
async def hug(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode se abraçar sozinho...", ephemeral=True)
        return

    #  resposta especial se abraçar o bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            description=f"🥹\u2003{user1.mention} **abraçou {user2.mention}!**\n",
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://64.media.tumblr.com/95a69094fc81a22ebc4b13339efbc090/tumblr_mkipflKprA1s6slcbo1_500.gif")
        
        await interaction.response.send_message(embed=embed)
        return     
    

    #  lista de GIFs de abraço
    gifs_abraco = [
        "https://media.tenor.com/FgLRE4gi5VoAAAAd/hugs-cute.gif",
        "https://media.tenor.com/BFmsQg9J1ZMAAAAd/chikako-hugging-otohime-for-the-first-and-she-confused.gif",
        "https://media.tenor.com/2HxamDEy7XAAAAAd/yukon-child-form-embracing-ulquiorra.gif",
        "https://media.tenor.com/P-8xYwXoGX0AAAAd/anime-hug-hugs.gif",
        "https://media.tenor.com/J7eGDvGeP9IAAAAd/enage-kiss-anime-hug.gif",
        "https://media.tenor.com/HBTbcCNvLRIAAAAd/syno-i-love-you-syno.gif",
        "https://media.tenor.com/mB_y2KUsyuoAAAAd/cuddle-anime-hug.gif",
        "https://media.tenor.com/ZHeWMKzI39QAAAAd/hug-hugs.gif",
        "https://media.tenor.com/tbzuQSodu58AAAAd/oshi-no-ko-onk.gif",
        "https://media.tenor.com/sl3rfZ7mQBsAAAAd/anime-hug-canary-princess.gif",
        "https://media.tenor.com/Maq1tnCFd2UAAAAd/hug-anime.gif",
        "https://media.tenor.com/0QALoFNm07AAAAAd/kaname-hug-kaname-hug-yuki.gif",
        "https://media.tenor.com/dHn4BG7y014AAAAd/yang-hugs-ruby.gif",
        "https://media.tenor.com/ubTTvDJRtKwAAAAd/sora-no-method-celestial-method.gif"
    ]

    gif_escolhido = random.choice(gifs_abraco)

    embed = discord.Embed(
        description=f"💌\u2003{user1.mention} **abraçou {user2.mention}!**\n",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)

# botao de retribuir
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_abracou: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_abracou = quem_abracou
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu o abraço pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o abraço de {self.quem_abracou.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_abraco))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_abracou, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)



#  COMANDO DE TAPAS
@bot.tree.command(name="slap", description="Dá um tapa em alguém")
@app_commands.describe(user="Quem vai receber o tapa")
async def slap(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode se auto-agredir...", ephemeral=True)
        return

    #  resposta especial se tentar bater no bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            title=":(",
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://media.tenor.com/LVT7ipJn_C8AAAAd/happy-fairy-tail.gif")
        
        await interaction.response.send_message(embed=embed)
        return

    #  lista de GIFs de tapa
    gifs_tapa = [
        "https://media.tenor.com/AzIExqZBjNoAAAAd/anime-slap.gif",
        "https://media.tenor.com/FrEq8y-Qf78AAAAd/anime-slapping.gif",
        "https://imgur.com/EozsOgA.gif",
        "https://i.pinimg.com/originals/40/ef/24/40ef24388a01ba9be6da6dea69d30fda.gif",
        "https://mageinabarrel.com/wp-content/uploads/2014/06/akari-slap.gif",
        "https://i.gifer.com/2mqv.gif",
        "https://i.gifer.com/TgZ1.gif",
        "https://imgur.com/lAioGCC.gif"
    ]

    gif_escolhido = random.choice(gifs_tapa)

    embed = discord.Embed(
        description=f"👊\u2003{user1.mention} **deu um tapa em {user2.mention}!**",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)

    
# botao retribuir
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_deutapa: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_deutapa = quem_deutapa
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="👊 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu o tapa pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o tapa de {self.quem_deutapa.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_tapa))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_deutapa, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)



#  COMANDO PATPAT
@bot.tree.command(name="patpat", description="Faz carinho em alguém (ou no bot...)")
@app_commands.describe(user="Quem vai receber o carinho")
async def patpat(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode fazer patpat em si mesmo(a)!...", ephemeral=True)
        return

    #  resposta especial se fazer carinho no bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://giffiles.alphacoders.com/141/141690.gif")
        
        await interaction.response.send_message(embed=embed)
        return

    #  lista de GIFs aleatórios 
    gifs_patpat = [
        "https://i.pinimg.com/originals/4c/03/bb/4c03bbe17bc0825e064d049c5f8262f3.gif",
        "https://i.pinimg.com/originals/f4/1b/39/f41b3974036070fd1c498acf17a3a42e.gif",
        "https://imgur.com/q31lv2t.gif",
        "https://imgur.com/9TdPHN8.gif",
        "https://imgur.com/OrUiyCp.gif",
        "https://media.tenor.com/f5asRSsfl-wAAAAM/good-boy-pat-on-head.gif",
        "https://i0.wp.com/images.wikia.com/adventuretimewithfinnandjake/images/2/2e/Jake_pat.gif",
        "https://static.wikia.nocookie.net/shipping/images/d/dd/ZoNa_Zou_arc.gif",
        "https://imgur.com/qdMIRpZ.gif",
        "https://imgur.com/25PNMah.gif"
        ]

    gif_escolhido = random.choice(gifs_patpat)

    embed = discord.Embed(
        description=f"💌\u2003{user1.mention} **fez patpat em {user2.mention}!**\n",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)
    
    
#  BOTAO DE RETRIBUIR
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_fezpatpat: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_fezpatpat = quem_fezpatpat
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu o patpat pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o patpat de {self.quem_fezpatpat.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_patpat))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_fezpatpat, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)



#  COMANDO DE MORDIDA
@bot.tree.command(name="bite", description="Dê uma mordida em alguém (ou no bot...)")
@app_commands.describe(user="Quem vai receber a mordida")
async def bite(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode morder a si mesmo(a)!...", ephemeral=True)
        return

    #  resposta especial se morder o bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://giffiles.alphacoders.com/141/141597.gif")
        
        await interaction.response.send_message(embed=embed)
        return

    #  lista de GIFs aleatórios 
    gifs_bite = [
        "https://i.pinimg.com/originals/f3/08/e2/f308e2fe3f1b3a41754727f8629e5b56.gif",
    "https://media.tenor.comp82FpH4jzp0AAAAd/vampire-diabolik-lovers.gif",
    "https://i.gifer.com/QHEF.gif",
    "https://i.gifer.com/2qw6.gif",
    "https://i.makeagif.com/media/1-15-2016/7QJBkD.gif",
    "https://64.media.tumblr.com/bd7c3f0bb557197439c03b82354b8ba8/5833c15b778ca53f-ce/s640x960/a741fd75532af2e6e71446e8e392b5418d2a86e3.gif",
    "https://media.tenor.com/BMEjcm2O8zsAAAAM/anime-bite.gif"
        ]

    gif_escolhido = random.choice(gifs_bite)

    embed = discord.Embed(
        description=f"💌\u2003{user1.mention} **deu uma mordida em {user2.mention}!**\n",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)
    
    
#  BOTAO DE RETRIBUIR
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_mordeu: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_mordeu = quem_mordeu
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu a mordida pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu a mordida de {self.quem_mordeu.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_bite))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_mordeu, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)
    
    
    
#  COMANDO DE HIGH FIVE ( toca aqui! )
@bot.tree.command(name="highfive", description="Faz um toca aqui com alguém (ou com o bot...)")
@app_commands.describe(user="Quem vai receber o highfive")
async def highfive(interaction: discord.Interaction, user: discord.Member):
    user1 = interaction.user
    user2 = user

    if user1 == user2:
        await interaction.response.send_message("❌ Você não pode fazer toca aqui consigo mesmo(a)!...", ephemeral=True)
        return

    #  resposta especial se fazer carinho no bot
    if bot.user in [user1, user2]:
        outro_usuario = user1 if user2 == bot.user else user2
        embed = discord.Embed(
            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url="https://imgur.com/M4A0Yys.gif")
        
        await interaction.response.send_message(embed=embed)
        return

    #  lista de GIFs aleatórios 
    gifs_highfive = [
        "https://64.media.tumblr.com/bb330522676865e19a3323bae4911f0c/bed24f800fd76092-30/s640x960/1be36be488e76453fa0a62709e9f0548c33a606d.gif",
        "https://imgur.com/gYRdIJy.gif",
        "https://64.media.tumblr.com/670b47fe8f7da2a49e8089ccfa233c9d/tumblr_pc1t0wl1xR1wn2b96o1_1280.gif",
        "https://media.tenor.com/F7JahZ_ntfUAAAAd/fairy-tail-high-five.gif",
        "https://imgur.com/jqvfgq0.gif",
        "https://imgur.com/6PzAerS.gif",
        "https://imgur.com/vO5SgfO.gif"
        ]

    gif_escolhido = random.choice(gifs_highfive)

    embed = discord.Embed(
        description=f"💌\u2003{user1.mention} **fez um toca aqui com {user2.mention}!**\n",
        color=discord.Color.pink()
    )
    embed.set_image(url=gif_escolhido)
    
    
#  BOTAO DE RETRIBUIR
    class RetribuirButton(discord.ui.View):
        def __init__(self, quem_deuhighfive: discord.Member, quem_recebeu: discord.Member, combo: int = 1):
            super().__init__(timeout=None)  # botão permanente
            self.quem_deuhighfive = quem_deuhighfive
            self.quem_recebeu = quem_recebeu
            self.combo = combo

        @discord.ui.button(label="💞 Retribuir", style=discord.ButtonStyle.secondary)
        async def retribuir(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.quem_recebeu.id:
                await interaction.response.send_message("❌ Só quem recebeu o toca aqui pode retribuir!", ephemeral=True)
                return

            novo_combo = self.combo + 1

            descricao = f"💌\u2003{self.quem_recebeu.mention} **retribuiu o toca aqui de {self.quem_deuhighfive.mention}!**"
            if novo_combo >= 3:
                descricao += f"  **(Combo {novo_combo}x!)**"

            novo_embed = discord.Embed(
                description=descricao,
                color=discord.Color.pink()
            )
            novo_embed.set_image(url=random.choice(gifs_highfive))

            nova_view = RetribuirButton(self.quem_recebeu, self.quem_deuhighfive, combo=novo_combo)
            await interaction.response.send_message(embed=novo_embed, view=nova_view)

    view = RetribuirButton(user1, user2)
    await interaction.response.send_message(embed=embed, view=view)



#  COMANDO A MIMIR
@bot.tree.command(name="amimir", description="Happy a mimir")
async def amimir(interaction: discord.Interaction):
    gifs_amimir = ["https://i.pinimg.com/originals/d6/39/40/d639408ae1f0365b63d5afbfb4d5a6a4.gif",
           "https://media.tenor.com/m/VySTk2IGD9wAAAAd/fairy-tail-sleeping.gif"]
    
    gif_escolhido = random.choice(gifs_amimir)

    embed = discord.Embed(

        color=discord.Color.from_rgb(158, 242, 255)
    )
    embed.set_image(url=gif_escolhido)

    # envia a resposta e salva a mensagem retornada
    await interaction.response.send_message(embed=embed)
    response = await interaction.original_response()

    # reage com emoji a mimir
    await response.add_reaction("😴")


    
#  COMANDO DANCE
@bot.tree.command(name="dance", description="Happy dançandinho")
async def dance(interaction: discord.Interaction):
    gifs_dance = ["https://64.media.tumblr.com/42c1aadb9e924a58c7578045d306fe5c/tumblr_on78agNv5W1vefoo6o1_540.gif",
           "https://media.tenor.com/GM-JoUIZ_ZgAAAAM/fairy-tail-happy.gif",
           "https://i.pinimg.com/originals/75/c2/81/75c2816899af78fba491c893125e16aa.gif"]
    
    gif_escolhido = random.choice(gifs_dance)

    embed = discord.Embed(

        color=discord.Color.from_rgb(158, 242, 255)
    )
    embed.set_image(url=gif_escolhido)

    # envia a resposta e salva a mensagem retornada
    await interaction.response.send_message(embed=embed)
    response = await interaction.original_response()

    # reage com emoji de dança
    await response.add_reaction("💃")



#  COMANDO DE LIMPAR O CHAT
@bot.hybrid_command(name='clear', description='Limpa mensagens do chat (até 100)') #  por ser hibrido funciona como cmd normal e cmd slash ao mesmo tempo
@app_commands.describe(count='Quantidade de mensagens a deletar (1-100)') #  descricao
@commands.has_permissions(manage_messages=True)
async def clear(ctx, count: int):
        if count < 1 or count > 100:
            await ctx.send("⚠️ Você pode limpar apenas entre 1 e 100 mensagens.", delete_after=8)
            return
    
        await ctx.channel.purge(limit=count + 1)
        # await asyncio.sleep(1)
        await ctx.send(f"{count} mensagens foram deletadas por {ctx.author.mention}", delete_after=8)
    
#  erros
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão pra usar esse comando!", delete_after=8)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Use um número válido. Ex: `.clear 10` ou `/clear amount: 10`", delete_after=8)



#  ENVIA O QUE FOR DIGITADO NO CAMPO DE MENSAGEM
@bot.tree.command(name="text", description='Envia o texto que for digitado como Happy')
async def text(interact:discord.Interaction, texto:str):
    await interact.response.send_message(texto)









# bot.run precisa estar em ULTIMO para analisar todo o código e poder rodar
bot.run("MTQwNDU4NjU1NDk2NTM2NDczNg.GN8wTs.Bf8mtfl08TKq_PiVZieZSFU6FA_XmCfpmnKF0w")
