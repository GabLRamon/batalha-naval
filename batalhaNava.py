import random

LINHAS = 5
COLUNAS = 10
#TODO verficiar se há possibilidade de aumentar
NAVIOS = 5

estadoPreJogo = False
estadoJogando = False

def criarTabuleiro():
    tabuleiro = []
    for i in range(LINHAS):
        linha = []
        for j in range(COLUNAS):
            linha.append(0)
        tabuleiro.append(linha)
    return tabuleiro


def mostrarTabuleiro(tabuleiro, nome, restantes, preGame):
    print("\nTabuleiro do", nome)
    for linha in tabuleiro:
        print(linha)

    if not preGame:
        print("++++++++++++++++++++++++++++++++++")
        # TODO em caso de implementação de desafio, mudar para embarcações
        print("Navios restantes:", restantes)



def posicaoValida(linha, coluna):
    return linha >= 0 and linha < LINHAS and coluna >= 0 and coluna < COLUNAS


def lerNumero(mensagem):
    while True:
        try:
            return int(input(mensagem)) - 1

        except ValueError:
            print("Erro: Digite apenas numeros")

def posicionarJogador(tabuleiro):
    colocados = 0

    while colocados < NAVIOS:
        print("\nPosicionando embarcação", colocados + 1)
        linha = lerNumero("Digite a linha: ")
        coluna = lerNumero("Digite a coluna: ")

        if not posicaoValida(linha, coluna):
            print("Posição inválida.")
        elif tabuleiro[linha][coluna] == "N":
            print("Já existe embarcação nessa posição.")
        else:
            tabuleiro[linha][coluna] = "N"
            colocados += 1
            mostrarTabuleiro(tabuleiro, "Jogador", 0, True)




def posicionarComputador(tabuleiro):
    colocados = 0

    while colocados < NAVIOS:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)

        if tabuleiro[linha][coluna] == 0:
            tabuleiro[linha][coluna] = "N"
            colocados += 1


def ataqueJogador(tabuleiro_oculto, tabuleiro_visivel):
    while True:
        linha = lerNumero("Digite a linha: ")
        coluna = lerNumero("Digite a coluna: ")

        if not posicaoValida(linha, coluna):
            print("Posição inválida.")
        elif tabuleiro_visivel[linha][coluna] != 0:
            print("Essa posição já foi atacada.")
        else:
            break

    if tabuleiro_oculto[linha][coluna] == "N":
        print("\nParabéns! Você acertou!")
        tabuleiro_visivel[linha][coluna] = "X"
        tabuleiro_oculto[linha][coluna] = "X"
        return True
    else:
        print("\nNão foi dessa vez!")
        tabuleiro_visivel[linha][coluna] = "."
        return False


def ataqueComputador(tabuleiro_oculto, tabuleiro_visivel):
    while True:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)

        if tabuleiro_visivel[linha][coluna] == 0:
            break

    print("\nComputador escolheu a linha", linha)
    print("Computador escolheu a coluna", coluna)

    if tabuleiro_oculto[linha][coluna] == "N":
        print("Computador acertou!")
        tabuleiro_visivel[linha][coluna] = "X"
        tabuleiro_oculto[linha][coluna] = "X"
        return True
    else:
        print("Computador errou!")
        tabuleiro_visivel[linha][coluna] = "."
        return False


def jogar():
    tabuleiroJogadorOculto = criarTabuleiro()
    tabuleiroComputadorOculto = criarTabuleiro()

    tabuleiroJogadorVisivel = criarTabuleiro()
    tabuleiroComputadorVisivel = criarTabuleiro()

    restantesJogador = NAVIOS
    restantesComputador = NAVIOS

    print("Bem vindo ao Batalha Naval!")

    posicionarJogador(tabuleiroJogadorOculto)
    posicionarComputador(tabuleiroComputadorOculto)

    while restantesJogador > 0 and restantesComputador > 0:

        mostrarTabuleiro(tabuleiroComputadorVisivel, "Computador", restantesComputador, False)
        mostrarTabuleiro(tabuleiroJogadorVisivel, "Jogador", restantesJogador, False)

        acertou = ataqueJogador(tabuleiroComputadorOculto, tabuleiroComputadorVisivel)

        if acertou:
            restantesComputador -= 1

        if restantesComputador == 0:
            break

        acertou = ataqueComputador(tabuleiroJogadorOculto, tabuleiroJogadorVisivel)

        if acertou:
            restantesJogador -= 1

    mostrarTabuleiro(tabuleiroComputadorVisivel, "Computador", restantesComputador, False)
    mostrarTabuleiro(tabuleiroJogadorVisivel, "Jogador", restantesJogador, False)

    if restantesComputador == 0:
        print("\nParabéns! Você afundou todas as embarcações do inimigo!")
    else:
        print("\nO computador venceu!")

    print("Jogo desenvolvido por: Gabriel Leite Ramon e ")
    print("Obrigado por jogar nosso jogo!")


jogar()