# imports
import time
import os
from sys import argv, exit

'''
    - Algoritmos e Estruturas de Dados II: Trabalho 1
    - Por: Alexya Ungaratti, Gabriela Guarani da Silva e Maria Rita Rodrigues
'''

def leitura(caminho_arquivo):
    try:
        with open(caminho_arquivo) as arquivo:
            texto = arquivo.readlines()  # lendo todas as linhas
        return remover_linhas_vazias(texto)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        exit(1)
    except IOError:
        print(f"Erro: Não foi possível ler o arquivo '{caminho_arquivo}'.")
        exit(1)

def remover_linhas_vazias(texto):
    # removendo linhas vazias e espaços em branco das linhas
    return [linha.rstrip('\n') for linha in texto if linha.strip()]

'''
    -------- MATRIZ --------
'''
def construir_matriz(texto):
    matriz = []
    
    for linha in texto:
        fila_char = []
        for caractere in linha:
            fila_char.append(caractere) # adicionando cada caractere do texto à fila
        matriz.append(fila_char) # adicionando a fila à matriz
        
    print("matriz criada com sucesso!...\n")
    return matriz

def imprimir_matriz(matriz, simbolo_atual = None, posicao = None):
    os.system('cls' if os.name == 'nt' else 'clear')  # limpando o terminal a cada vez que a matriz é impressa (win e linux)
    for i, linha in enumerate(matriz):
        for j, caractere in enumerate(linha):
            if simbolo_atual and posicao == (i, j):
                print(f"\033[92m{caractere}\033[0m", end="")  # imprime o simbolo atual na cor verde
            else:
                print(caractere, end="")
        print()  # nova linha
    time.sleep(0.05)  # tempo de impressão

def encontrar_raiz(matriz):
    ultima_linha = matriz[-1] # pegamos a última linha da matriz
    for coluna, caractere in enumerate(ultima_linha):
        if caractere != ' ':  # vemos se o caractere não é um espaço vazio
            return coluna  # retornamos a coluna em que a raiz foi encontrada
    return None

'''
    -------- CAMINHAR --------
'''

def galhos(matriz, linha, coluna, direcao):
    total = 0
    pilha = []

    while linha >= 0 and 0 <= coluna < len(matriz[linha]):
        caractere = matriz[linha][coluna]
        pilha.append((caractere, linha, coluna))
        
        # imprimindo o símbolo atual e posição
        imprimir_matriz(matriz, simbolo_atual = caractere, posicao = (linha, coluna))

        # se encontrar um nodo folha
        if caractere == '#':
            return total, pilha

        # acumula o valor se for um número
        if caractere.isdigit():
            total += int(caractere)

        # explorando as ramificações
        if caractere == 'V' or caractere == 'W':
            # vai para o galho da esquerda
            totalE, pilhaE = galhos(matriz, linha - 1, coluna - 1, "esquerda")
            
            # explora o galho do centro (só funfa no 'W')
            if caractere == 'W':
                totalC, pilhaM = galhos(matriz, linha - 1, coluna, "centro")
            else:
                totalC = -1  # desabilita o centro, caso não seja um 'W'
                
            # explora o galho da direita
            totalD, pilhaD = galhos(matriz, linha - 1, coluna + 1, "direita")

            # qual galho tem a maior pontuação?
            if caractere == 'W':
                if totalE >= totalC and totalE >= totalD:
                    return totalE, pilhaE
                elif totalC >= totalE and totalC >= totalD:
                    return totalC, pilhaM
                else:
                    return totalD, pilhaD
                
            elif caractere == 'V':
                if totalE >= totalD:
                    return totalE, pilhaE
                else:
                    return totalD, pilhaD

        # definindo as direções
        linha -= 1
        if direcao == "esquerda":
            coluna -= 1
        elif direcao == "direita":
            coluna += 1
            
    return total, pilha

def caminhar(matriz, raizCol):
    linha_raiz = len(matriz) - 1
    total, caminho = galhos(matriz, linha_raiz, raizCol, "centro")

    print(f"Pontuação do melhor caminho: {total}")
    return caminho

'''
    -------- MAIN --------
'''
if __name__ == "__main__":
    if len(argv) != 2:
        print("Digite: python frutinhasMalditas.py caminho_do_caso")
        exit(1)
    
    caminho_arquivo = argv[1]
    texto = leitura(caminho_arquivo)
    matriz = construir_matriz(texto)
    imprimir_matriz(matriz)
    raizCol = encontrar_raiz(matriz)
    caminhar(matriz, raizCol)