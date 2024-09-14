# imports
from sys import argv, exit

'''
    - T1: Algoritmos e Estruturas de Dados II
    - Alexya Ungarattim, Gabrielle Guarani da Silva e Maria Rita Rodrigues
'''

# arquivo que vamos ler
caminho_arquivo = "./casos/casod30.txt"

def ler_arquivo_texto(caminho_arquivo):
    print("lendo o arquivo...")
    with open(caminho_arquivo) as arquivo:
        texto = arquivo.readlines()  # lendo todas as linhas
    
    texto = remover_linhas_vazias(texto)  # removendo linhas vazias do texto
    print("arquivo lido com sucesso!...")
    return texto

def remover_linhas_vazias(texto):
    # removendo linhas vazias e espaços em branco das linhas
    return [linha.rstrip('\n') for linha in texto if linha.strip()]

'''
    -------- MATRIZ --------
'''

def construir_matriz(texto):
    print("construindo a matriz...")
    matriz = []
    
    for linha in texto:
        fila = []
        for caractere in linha:
            fila.append(caractere)  # adicionando cada caractere do texto à fila
        matriz.append(fila)  # adicionando a fila à matriz
        
    print("matriz criada com sucesso!...\n")
    return matriz

def imprimir_matriz(matriz):
    for linha in matriz:
        print(''.join(linha)) # imprimindo a matriz formatada (arvore!!)

def encontrar_raiz(matriz):
    ultima_linha = matriz[-1]  # pegamos a última linha da matriz
    for coluna, caractere in enumerate(ultima_linha):
        if caractere != ' ':  # vemos se o caractere não é um espaço vazio
            print("raiz (elemento): " + caractere)
            return coluna  # retornamos a coluna em que a raiz foi encontrada
    return None

'''
    -------- CAMINHAR --------
'''

def caminhar(matriz, raizCol):
    print("caminhando na matriz...")

    def explorar_galho(linha, coluna, direcao,parte_trifurcacao=False):
        total = 0
        
        while linha >= 0 and coluna >= 0 and coluna < len(matriz[linha]):
            caractere = matriz[linha][coluna]

            # se encontrar uma folha, retorna o total acumulado
            if caractere == '#':
                print(f"\ntotal acumulado no galho ({direcao}): {total}")
                return total

            # acumula o valor se for um número
            if caractere.isdigit():
                total += int(caractere)

            # se encontrar uma bifurcação 'V', explora ambos os galhos
            if caractere == 'V':
                origem = f"galho de uma trifurcação 'W' ({direcao})" if parte_trifurcacao else "galho direto"
                print(f"\nbifurcação 'V' encontrada no {origem}, na linha {linha}, coluna {coluna}")
                
                # explora o galho esquerdo da bifurcação 'V'
                totalE = explorar_galho(linha - 1, coluna - 1, "esquerda")
                
                # backtrack para a bifurcação 'V'
                print(f"retornando à bifurcação 'V' na linha {linha}, coluna {coluna}")
                
                # explora o galho direito da bifurcação 'V'
                totalD = explorar_galho(linha - 1, coluna + 1, "direita")
                
                # printando os totais da'V'
                print(f"\ntotal acumulado na bifurcação 'V': esquerda={totalE}, direita={totalD}")
                return totalE + totalD

            # move para o próximo caractere na direção especificada
            linha -= 1
            if direcao == "esquerda":
                coluna -= 1
            elif direcao == "direita":
                coluna += 1

        return total

    # começa a exploração a partir da linha da raiz
    linha_raiz = len(matriz) - 1

    maiores_totais = {
        "esquerda": 0,
        "meio": 0,
        "direita": 0
    }

    while linha_raiz >= 0:
        if 0 <= raizCol < len(matriz[linha_raiz]):
            caractere = matriz[linha_raiz][raizCol]

            # processa trifurcações 'W'
            if caractere == 'W':  
                totalE = explorar_galho(linha_raiz - 1, raizCol - 1, "esquerda",parte_trifurcacao=True)
                total_meio = explorar_galho(linha_raiz - 1, raizCol, "meio",parte_trifurcacao=True)
                totalD = explorar_galho(linha_raiz - 1, raizCol + 1, "direita",parte_trifurcacao=True)
                maiores_totais = {
                    "esquerda": totalE,
                    "meio": total_meio,
                    "direita": totalD
                }
                print(f"total acumulado nos galhos: esquerda={totalE}, meio={total_meio}, direita={totalD}")
                break

            elif caractere == 'V':
                totalE = explorar_galho(linha_raiz - 1, raizCol - 1, "esquerda")
                totalD = explorar_galho(linha_raiz - 1, raizCol + 1, "direita")
                maiores_totais = {
                    "esquerda": totalE,
                    "direita": totalD
                }
                print(f"\ntotal acumulado na bifurcação 'V': esquerda={totalE}, direita={totalD}")
                break
        else:
            print(f"\níndice raizCol {raizCol} fora dos limites na linha {linha_raiz}.")
        
        linha_raiz -= 1

    # Comparar os ramos e retornar o maior
    galho_vencedor = max(maiores_totais, key=maiores_totais.get)
    print(f"O galho com maior pontuação é o da {galho_vencedor}, com {maiores_totais[galho_vencedor]} pontos.")
    return galho_vencedor, maiores_totais[galho_vencedor]


def contar_linhas(texto):
    return len(texto)  # conta e retorna o número de linhas no texto

# linhas quant
texto = ler_arquivo_texto(caminho_arquivo)
num_linhas = contar_linhas(texto) 
print(f"\no texto tem {num_linhas} linhas\n")

# testando o código
texto = ler_arquivo_texto(caminho_arquivo) 
matriz = construir_matriz(texto) 
imprimir_matriz(matriz)
raizCol = encontrar_raiz(matriz)
print(f"a raiz encontrada é: {raizCol}")

caminhar(matriz, raizCol)