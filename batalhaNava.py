from __future__ import print_function
import random

# Este bloco permite rodar o jogo tanto no Python 2 quanto no Python 3.
try:
    lerEntrada = raw_input
except NameError:
    lerEntrada = input


# O PDF permite tabuleiro 5x10 ou 10x10.
# Usamos 10x10 porque o desafio tem navios grandes, como o Porta-avioes.
LINHAS = 10
COLUNAS = 10


# Cada item da lista representa um navio do desafio.
# Formato: [nome do navio, letra usada no tabuleiro oculto, tamanho do navio]
NAVIOS_INFO = [
    ["Porta-avioes", "P", 5],
    ["Navio-tanque", "N", 4],
    ["Contratorpedeiro", "C", 3],
    ["Submarino", "S", 2],
    ["Destroier", "D", 1]
]


def criarTabuleiro():
    # Cria uma matriz 10x10 preenchida com 0.
    # A matriz representa o tabuleiro porque o jogo usa linha e coluna.
    tabuleiro = []

    for i in range(LINHAS):
        linha = []

        for j in range(COLUNAS):
            linha.append(0)

        tabuleiro.append(linha)

    return tabuleiro


def criarFrota():
    # Cria uma frota nova com todos os navios do desafio.
    # Cada navio guarda suas posicoes, quantidade de acertos e se ja afundou.
    frota = []

    for info in NAVIOS_INFO:
        navio = {
            "nome": info[0],
            "letra": info[1],
            "tamanho": info[2],
            "posicoes": [],
            "acertos": 0,
            "afundado": False
        }

        frota.append(navio)

    return frota


def mostrarTabuleiro(tabuleiro, nome, restantes, preGame):
    # Mostra o tabuleiro de um jeito mais facil de ler.
    # Nos tabuleiros visiveis:
    # 0 significa posicao ainda nao atacada.
    # X significa acerto.
    # O significa erro.
    print("\nTabuleiro do", nome)
    print("    1  2  3  4  5  6  7  8  9 10")
    print("   ------------------------------")

    for linha in range(LINHAS):
        numeroLinha = linha + 1

        if numeroLinha < 10:
            print(" " + str(numeroLinha) + "|", end=" ")
        else:
            print(str(numeroLinha) + "|", end=" ")

        for coluna in range(COLUNAS):
            print(tabuleiro[linha][coluna], end="  ")

        print()

    if not preGame:
        print("Embarcacoes restantes:", restantes)


def mostrarStatus(tabuleiroComputadorVisivel, tabuleiroJogadorVisivel, frotaComputador, frotaJogador):
    # Mostra os dois tabuleiros visiveis e a quantidade de navios restantes.
    # O tabuleiro oculto nunca e mostrado ao adversario.
    print("\n============================================================")
    mostrarTabuleiro(tabuleiroComputadorVisivel, "Computador", contarRestantes(frotaComputador), False)
    mostrarTabuleiro(tabuleiroJogadorVisivel, "Jogador", contarRestantes(frotaJogador), False)
    print("============================================================")


def posicaoValida(linha, coluna):
    # Verifica se linha e coluna estao dentro do tabuleiro.
    if linha < 0 or linha >= LINHAS:
        return False

    if coluna < 0 or coluna >= COLUNAS:
        return False

    return True


def lerNumero(mensagem):
    # O usuario digita de 1 a 10.
    # O Python usa indices de 0 a 9, por isso subtraimos 1.
    while True:
        try:
            return int(lerEntrada(mensagem)) - 1

        except ValueError:
            print("Erro: digite apenas numeros.")


def lerDirecao():
    # H posiciona o navio na horizontal.
    # V posiciona o navio na vertical.
    while True:
        direcao = lerEntrada("Digite a direcao (H para horizontal, V para vertical): ")
        direcao = direcao.upper()

        if direcao == "H" or direcao == "V":
            return direcao

        print("Direcao invalida. Digite H ou V.")


def calcularPosicoesNavio(linha, coluna, tamanho, direcao):
    # Calcula todas as casas que um navio vai ocupar.
    # Exemplo: tamanho 3 na horizontal ocupa 3 colunas seguidas.
    posicoes = []

    for parte in range(tamanho):
        if direcao == "H":
            posicoes.append([linha, coluna + parte])
        else:
            posicoes.append([linha + parte, coluna])

    return posicoes


def podeColocarNavio(tabuleiro, linha, coluna, tamanho, direcao):
    # Confere se o navio cabe no tabuleiro e se nao fica em cima de outro.
    posicoes = calcularPosicoesNavio(linha, coluna, tamanho, direcao)

    for posicao in posicoes:
        linhaAtual = posicao[0]
        colunaAtual = posicao[1]

        if not posicaoValida(linhaAtual, colunaAtual):
            return False

        if tabuleiro[linhaAtual][colunaAtual] != 0:
            return False

    return True


def colocarNavio(tabuleiro, linha, coluna, tamanho, direcao, letra):
    # Coloca a letra do navio em todas as casas ocupadas por ele.
    # Isso acontece apenas no tabuleiro oculto.
    posicoes = calcularPosicoesNavio(linha, coluna, tamanho, direcao)

    for posicao in posicoes:
        linhaAtual = posicao[0]
        colunaAtual = posicao[1]
        tabuleiro[linhaAtual][colunaAtual] = letra

    return posicoes


def posicionarJogador(tabuleiro, frota):
    # O jogador posiciona cada embarcacao da frota.
    # O programa valida para nao deixar navio fora do tabuleiro nem sobreposto.
    for navio in frota:
        while True:
            print("\nPosicionando embarcacao:", navio["nome"])
            print("Tamanho:", navio["tamanho"])
            print("Letra:", navio["letra"])

            linha = lerNumero("Digite a linha inicial: ")
            coluna = lerNumero("Digite a coluna inicial: ")

            if navio["tamanho"] == 1:
                direcao = "H"
            else:
                direcao = lerDirecao()

            if podeColocarNavio(tabuleiro, linha, coluna, navio["tamanho"], direcao):
                navio["posicoes"] = colocarNavio(tabuleiro, linha, coluna, navio["tamanho"], direcao, navio["letra"])
                print("Embarcacao posicionada com sucesso.")
                mostrarTabuleiro(tabuleiro, "Jogador", 0, True)
                break

            print("Posicao invalida ou ocupada. Tente novamente.")


def posicionarComputador(tabuleiro, frota):
    # O computador sorteia posicao e direcao ate conseguir colocar cada navio.
    for navio in frota:
        while True:
            linha = random.randint(0, LINHAS - 1)
            coluna = random.randint(0, COLUNAS - 1)

            if random.randint(1, 2) == 1:
                direcao = "H"
            else:
                direcao = "V"

            if podeColocarNavio(tabuleiro, linha, coluna, navio["tamanho"], direcao):
                navio["posicoes"] = colocarNavio(tabuleiro, linha, coluna, navio["tamanho"], direcao, navio["letra"])
                break


def procurarNavio(frota, letra):
    # Procura qual navio tem a letra encontrada no tabuleiro oculto.
    for navio in frota:
        if navio["letra"] == letra:
            return navio

    return None


def contarRestantes(frota):
    # Conta quantos navios ainda nao foram afundados.
    restantes = 0

    for navio in frota:
        if not navio["afundado"]:
            restantes += 1

    return restantes


def verificarAfundou(navio):
    # Um navio so afunda quando todas as partes dele foram acertadas.
    if navio["acertos"] >= navio["tamanho"]:
        navio["afundado"] = True
        return True

    return False


def ataqueJogador(tabuleiro_oculto, tabuleiro_visivel, frota):
    # O jogador escolhe uma posicao para atacar.
    # O programa nao permite atacar fora do tabuleiro nem repetir ataque.
    while True:
        linha = lerNumero("Digite a linha para atacar: ")
        coluna = lerNumero("Digite a coluna para atacar: ")

        if not posicaoValida(linha, coluna):
            print("Posicao invalida.")
        elif tabuleiro_visivel[linha][coluna] != 0:
            print("Essa posicao ja foi atacada.")
        else:
            break

    conteudo = tabuleiro_oculto[linha][coluna]

    if conteudo == 0:
        print("\nNao foi dessa vez!")
        tabuleiro_visivel[linha][coluna] = "O"
        return "errou"

    print("\nParabens! Voce acertou!")
    tabuleiro_visivel[linha][coluna] = "X"

    navio = procurarNavio(frota, conteudo)
    navio["acertos"] += 1

    if verificarAfundou(navio):
        print("Voce afundou o", navio["nome"])
        return "afundou"

    return "acertou"


def ataqueComputador(tabuleiro_oculto, tabuleiro_visivel, frota):
    # O computador sorteia uma posicao ainda nao atacada.
    while True:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)

        if tabuleiro_visivel[linha][coluna] == 0:
            break

    print("\nComputador escolheu a linha", linha + 1)
    print("Computador escolheu a coluna", coluna + 1)

    conteudo = tabuleiro_oculto[linha][coluna]

    if conteudo == 0:
        print("Computador errou!")
        tabuleiro_visivel[linha][coluna] = "O"
        return "errou"

    print("Computador acertou!")
    tabuleiro_visivel[linha][coluna] = "X"

    navio = procurarNavio(frota, conteudo)
    navio["acertos"] += 1

    if verificarAfundou(navio):
        print("O computador afundou seu", navio["nome"])
        return "afundou"

    return "acertou"


def jogar():
    # Tabuleiros ocultos:
    # guardam os navios reais de cada jogador.
    tabuleiroJogadorOculto = criarTabuleiro()
    tabuleiroComputadorOculto = criarTabuleiro()

    # Tabuleiros visiveis:
    # guardam apenas o resultado dos ataques.
    tabuleiroJogadorVisivel = criarTabuleiro()
    tabuleiroComputadorVisivel = criarTabuleiro()

    frotaJogador = criarFrota()
    frotaComputador = criarFrota()

    print("Bem vindo ao Batalha Naval!")
    print("Modo: jogador contra computador")
    print("Tabuleiro: 10 x 10")

    posicionarJogador(tabuleiroJogadorOculto, frotaJogador)
    posicionarComputador(tabuleiroComputadorOculto, frotaComputador)

    vezJogador = True

    # O jogo continua enquanto os dois jogadores ainda tiverem navios.
    while contarRestantes(frotaJogador) > 0 and contarRestantes(frotaComputador) > 0:
        mostrarStatus(tabuleiroComputadorVisivel, tabuleiroJogadorVisivel, frotaComputador, frotaJogador)

        if vezJogador:
            print("\nVez do jogador")
            resultado = ataqueJogador(tabuleiroComputadorOculto, tabuleiroComputadorVisivel, frotaComputador)

            # Regra extra: quem afunda uma embarcacao joga novamente.
            if resultado == "afundou":
                vezJogador = True
            else:
                vezJogador = False
        else:
            print("\nVez do computador")
            resultado = ataqueComputador(tabuleiroJogadorOculto, tabuleiroJogadorVisivel, frotaJogador)

            if resultado == "afundou":
                vezJogador = False
            else:
                vezJogador = True

    mostrarStatus(tabuleiroComputadorVisivel, tabuleiroJogadorVisivel, frotaComputador, frotaJogador)

    if contarRestantes(frotaComputador) == 0:
        print("\nParabens! Voce afundou todas as embarcacoes do inimigo!")
    else:
        print("\nO computador venceu!")

    print("Jogo desenvolvido por: Gabriel Leite Ramon e Nome 2")
    print("Obrigado por jogar nosso jogo!")


jogar()
