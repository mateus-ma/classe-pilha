import os
import sys
from pathlib import Path
from pilha import Pilha  # Importa a classe Pilha original[cite: 1]

# Eleva o limite de recursão para permitir o processamento de matrizes grandes
sys.setrecursionlimit(100000)

class PilhaPosicao:
    """
    Adaptador que empacota a classe Pilha original baseada em 'array'[cite: 1]
    para armazenar e recuperar coordenadas (linha, coluna) como inteiros.
    """
    def __init__(self, capacidade: int, num_colunas: int):
        self._pilha = Pilha(capacidade, typecode='i')
        self._cols = num_colunas

    def empilhar(self, linha: int, coluna: int):
        pos_id = linha * self._cols + coluna
        self._pilha.empilha(pos_id)

    def desempilhar(self) -> tuple[int, int]:
        pos_id = self._pilha.desempilha()
        linha = pos_id // self._cols
        coluna = pos_id % self._cols
        return linha, coluna

    def esta_vazia(self) -> bool:
        return self._pilha.pilha_esta_vazia()


def carregar_e_validar_matriz(caminho_arquivo: str) -> list[list[str]]:
    """
    Lê o arquivo e valida se é uma matriz de caracteres retangular e consistente.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")

    matriz = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for num_linha, linha in enumerate(f, start=1):
            conteudo = linha.strip()
            if not conteudo:
                continue  # Ignora linhas vazias
            
            # Validação: Garante que os elementos sejam apenas caracteres
            linha_chars = list(conteudo)
            matriz.append(linha_chars)

    if not matriz:
        raise ValueError("Erro: O arquivo da matriz está vazio.")

    # Validação: Verifica se todas as linhas têm o mesmo número de colunas (matriz retangular)
    num_colunas = len(matriz[0])
    for idx, linha in enumerate(matriz):
        if len(linha) != num_colunas:
            raise ValueError(
                f"Erro na linha {idx + 1}: Matriz inconsistente. "
                f"A primeira linha possui {num_colunas} caracteres, mas a linha {idx + 1} possui {len(linha)}."
            )

    return matriz


def validar_posicao_inicial(matriz: list[list[str]], linha: int, coluna: int):
    """
    Verifica se a posição inicial (linha, coluna) informada existe na matriz.
    """
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])

    if not (0 <= linha < num_linhas) or not (0 <= coluna < num_colunas):
        raise IndexError(
            f"Erro: A posição inicial ({linha}, {coluna}) está fora dos limites da matriz. "
            f"A matriz possui dimensão {num_linhas}x{num_colunas} (índices válidos: linhas 0 a {num_linhas - 1}, colunas 0 a {num_colunas - 1})."
        )


def exibir_matriz(matriz: list[list[str]], titulo: str = ""):
    """
    Apresenta a matriz formatada na tela do terminal.
    Conforme o enunciado: troca '1' por espaço em branco e '0' por '#' para melhor visualização.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    if titulo:
        print(f"=== {titulo} ===")
    
    for linha in matriz:
        linha_fmt = "".join(linha).replace('1', ' ').replace('0', '#')
        print(linha_fmt)
    print("=" * 45)


# Variável global para controle de exibição a cada P passos
contador_passos = 0

def flood_fill_recursivo(matriz: list[list[str]], pilha: PilhaPosicao, passos_p: int):
    """
    Rotina RECURSIVA de preenchimento que utiliza a classe PILHA para gerenciar as posições.
    """
    global contador_passos

    # Caso base da recursão
    if pilha.esta_vazia():
        return

    r, c = pilha.desempilhar()
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])

    # O preenchimento ocorre nas células contendo '1' ou na posição inicial 'X'
    if 0 <= r < num_linhas and 0 <= c < num_colunas and matriz[r][c] in ('1', 'X'):
        matriz[r][c] = '0'
        contador_passos += 1

        # Apresentação intermediária a cada P passos
        if passos_p > 0 and contador_passos % passos_p == 0:
            exibir_matriz(matriz, f"Evolução: Passo {contador_passos}")
            input("Pressione [ENTER] para prosseguir aos próximos passos...")

        # Vizinhos nas 4 direções (Cima, Baixo, Esquerda, Direita)
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in direcoes:
            nr, nc = r + dr, c + dc
            if 0 <= nr < num_linhas and 0 <= nc < num_colunas:
                if matriz[nr][nc] in ('1', 'X'):
                    pilha.empilhar(nr, nc)
                    flood_fill_recursivo(matriz, pilha, passos_p)


def executar_preenchimento(caminho_arquivo: str, linha_inicial: int, coluna_inicial: int, passos_p: int):
    """
    Função principal que recebe os parâmetros de entrada, executa as validações e o algoritmo.
    """
    global contador_passos
    contador_passos = 0

    # 1. Carrega e valida o arquivo da matriz
    matriz = carregar_e_validar_matriz(caminho_arquivo)

    # 2. Valida se a posição inicial existe dentro da matriz
    validar_posicao_inicial(matriz, linha_inicial, coluna_inicial)

    # 3. Apresentação inicial da matriz antes de modificar
    exibir_matriz(matriz, "MATRIZ INICIAL")
    print(f"Posição inicial selecionada: ({linha_inicial}, {coluna_inicial})")
    print(f"Intervalo de parada P: {passos_p} passos (0 = sem paradas intermediárias)")
    input("\nPressione [ENTER] para começar o preenchimento...")

    # 4. Inicializa a Pilha com capacidade para toda a matriz
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])
    pilha = PilhaPosicao(capacidade=num_linhas * num_colunas, num_colunas=num_colunas)

    # Empilha a posição de início informada
    pilha.empilhar(linha_inicial, coluna_inicial)

    # 5. Executa a rotina recursiva com a pilha
    flood_fill_recursivo(matriz, pilha, passos_p)

    # 6. Apresentação final da matriz após o término
    exibir_matriz(matriz, "MATRIZ FINAL")
    print(f"Rotina concluída com sucesso. Total de posições preenchidas: {contador_passos}")


if __name__ == "__main__":
    # --- PARÂMETROS DE ENTRADA ---
    ARQUIVO = "matriz_B.txt"
    # INFORME AQUI A POSIÇÃO INICIAL (linha, coluna) PARA O PREENCHIMENTO
    LINHA_INICIAL = 7
    COLUNA_INICIAL = 23
    PASSOS_P = 20  # Informe 0 para executar sem paradas intermediárias

    try:
        executar_preenchimento(
            caminho_arquivo=Path(__file__).resolve().parent / ARQUIVO,
            linha_inicial=LINHA_INICIAL,
            coluna_inicial=COLUNA_INICIAL,
            passos_p=PASSOS_P
        )
    except (FileNotFoundError, ValueError, IndexError) as err:
        print(f"\n[FALHA NA VALIDAÇÃO]: {err}")