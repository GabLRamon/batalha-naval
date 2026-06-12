from __future__ import print_function
import random

LINHAS = 10
COLUNAS = 10


# nao sei se e necessario, a gente pode so colocar no info direto e boa, mas fica mais bonito assim
NAVIOS_INFO = [
    ["Porta-avioes", "P", 5],
    ["Navio-tanque", "N", 4],
    ["Contratorpedeiro", "C", 3],
    ["Submarino", "S", 2],
    ["Destroier", "D", 1]
]


def criarTabuleiro():
    tabuleiro = []

    for i in range(LINHAS):
        linha = []

        for j in range(COLUNAS):
            linha.append(0)

        tabuleiro.append(linha)

    return tabuleiro


def criarFrota():

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

    #nao sei se precisa do preGame, caso volte pro codigo em uma data posterior, verificar possiblidade de fazer variavel estatica

    print("\nTabuleiro do", nome)
    # vai ficar hardcoded mesmo, preguiça de resolver

    # print("   ------------------------------")
    # for quantidadeLinha in range(LINHAS):
    #     print("  " + str(quantidadeLinha), end=" ")

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

    print("\n============================================================")
    mostrarTabuleiro(tabuleiroComputadorVisivel, "Computador", contarRestantes(frotaComputador), False)
    mostrarTabuleiro(tabuleiroJogadorVisivel, "Jogador", contarRestantes(frotaJogador), False)
    print("============================================================")

def posicaoValida(linha, coluna):

    if linha < 0 or linha >= LINHAS:
        return False

    if coluna < 0 or coluna >= COLUNAS:
        return False

    return True

def lerNumero(mensagem):

    while True:
        try:
            return int(input(mensagem)) - 1

        except ValueError:
            print("Erro: digite apenas numeros.")


def lerDirecao():

    while True:
        direcao = input("Digite a direcao (H para horizontal, V para vertical): ")
        direcao = direcao.upper()

        if direcao == "H" or direcao == "V":
            return direcao

        print("Direcao invalida. Digite H ou V.")


def calcularPosicoesNavio(linha, coluna, tamanho, direcao):
    posicoes = []

    for parte in range(tamanho):
        if direcao == "H":
            posicoes.append([linha, coluna + parte])
        else:
            posicoes.append([linha + parte, coluna])

    return posicoes


def podeColocarNavio(tabuleiro, linha, coluna, tamanho, direcao):
 
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

    posicoes = calcularPosicoesNavio(linha, coluna, tamanho, direcao)

    for posicao in posicoes:
        linhaAtual = posicao[0]
        colunaAtual = posicao[1]
        tabuleiro[linhaAtual][colunaAtual] = letra

    return posicoes


def posicionarJogador(tabuleiro, frota):
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

    for navio in frota:
        if navio["letra"] == letra:
            return navio

    return None


def contarRestantes(frota):

    restantes = 0

    for navio in frota:
        if not navio["afundado"]:
            restantes += 1

    return restantes


def verificarAfundou(navio):

    if navio["acertos"] >= navio["tamanho"]:
        navio["afundado"] = True
        return True

    return False


def ataqueJogador(tabuleiroOculto, tabuleiroVisivel, frota):

    #todo esse codigo ficou muito mal legivel, dar uma olhada dps

    while True:
        linha = lerNumero("Digite a linha para atacar: ")
        coluna = lerNumero("Digite a coluna para atacar: ")

        if not posicaoValida(linha, coluna):
            print("Posicao invalida.")
        elif tabuleiroVisivel[linha][coluna] != 0:
            print("Essa posicao ja foi atacada.")
        else:
            break

    conteudo = tabuleiroOculto[linha][coluna]

    if conteudo == 0:
        print("\nNao foi dessa vez!")
        tabuleiroVisivel[linha][coluna] = "O"
        return "errou"

    print("\nParabens! Voce acertou!")
    tabuleiroVisivel[linha][coluna] = "X"

    navio = procurarNavio(frota, conteudo)
    navio["acertos"] += 1

    if verificarAfundou(navio):
        print("Voce afundou o", navio["nome"])
        return "afundou"

    return "acertou"


def ataqueComputador(tabuleiro_oculto, tabuleiro_visivel, frota):

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

    tabuleiroJogadorOculto = criarTabuleiro()
    tabuleiroComputadorOculto = criarTabuleiro()


    tabuleiroJogadorVisivel = criarTabuleiro()
    tabuleiroComputadorVisivel = criarTabuleiro()

    frotaJogador = criarFrota()
    frotaComputador = criarFrota()

    print("Bem vindo ao Batalha Naval!")
    print("Modo: jogador contra computador")
    print("Tabuleiro: 10 x 10")

    mostrarTabuleiro(tabuleiroJogadorOculto, "Jogador", 0, True);

    posicionarJogador(tabuleiroJogadorOculto, frotaJogador)
    posicionarComputador(tabuleiroComputadorOculto, frotaComputador)

    vezJogador = True


    while contarRestantes(frotaJogador) > 0 and contarRestantes(frotaComputador) > 0:
        mostrarStatus(tabuleiroComputadorVisivel, tabuleiroJogadorVisivel, frotaComputador, frotaJogador)

        if vezJogador:
            print("\nVez do jogador")
            resultado = ataqueJogador(tabuleiroComputadorOculto, tabuleiroComputadorVisivel, frotaComputador)


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

    print("Jogo desenvolvido por: Gabriel Leite Ramon e Gustavo Machado Garcia")
    print("Obrigado por jogar nosso jogo!")


jogar()
