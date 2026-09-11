import os
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox, colorchooser
from pilha import Pilha  # Usa a classe Pilha original

# Eleva o limite de recursão para permitir preenchimento de imagens grandes
sys.setrecursionlimit(100000)

TAMANHO_PIXEL = 15  # Dimensão em pixels de cada célula da grade na tela

class PilhaPosicao:
    """
    Adaptador que empacota a classe Pilha original
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
    """Valida o arquivo e carrega a matriz de caracteres do bitmap."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado.")

    matriz = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            conteudo = linha.strip()
            if conteudo:
                matriz.append(list(conteudo))

    if not matriz:
        raise ValueError("O arquivo da matriz está vazio.")

    num_cols = len(matriz[0])
    for idx, l in enumerate(matriz):
        if len(l) != num_cols:
            raise ValueError(f"Matriz inconsistente na linha {idx + 1}.")

    return matriz


class PaintBitmapApp:
    def __init__(self, root, caminho_arquivo: str, passos_p: int = 10):
        self.root = root
        self.root.title("MS-Paint Bitmap - Preenchimento de Região com Pilha e Recursão")
        
        # 1. Carrega e Valida a Matriz
        self.matriz = carregar_e_validar_matriz(caminho_arquivo)
        self.linhas = len(self.matriz)
        self.colunas = len(self.matriz[0])
        self.passos_p = passos_p
        
        # Mapeamento inicial de caracteres para cores hexadecimais
        self.cor_preenchimento = "#0000FF"  # Cor padrão inicial: Azul
        self.mapa_cores = {
            '1': '#FFFFFF',  # Branco (fundo preenchível)
            '0': '#000000',  # Preto (bordas / paredes)
        }
        
        self.contador_passos = 0
        self.pixels_canvas = {}

        # 2. Interface Gráfica
        self._criar_interface()
        self._desenhar_bitmap_inicial()

    def _criar_interface(self):
        """Monta o painel de controles e a área do Canvas (Bitmap)."""
        painel_topo = tk.Frame(self.root, bg="#DDDDDD", padx=5, pady=5)
        painel_topo.pack(side=tk.TOP, fill=tk.X)
        # Botão para trocar a cor ativa (igual ao MS-Paint)
        btn_cor = tk.Button(painel_topo, text="Escolher Cor", command=self._selecionar_cor)
        btn_cor.pack(side=tk.LEFT, padx=5)

        self.indicador_cor = tk.Label(painel_topo, text="   ", bg=self.cor_preenchimento, relief=tk.SUNKEN)
        self.indicador_cor.pack(side=tk.LEFT, padx=5)

        lbl_info = tk.Label(painel_topo, text="Clique em qualquer pixel para iniciar o Flood Fill")
        lbl_info.pack(side=tk.LEFT, padx=15)

        # Canvas onde os pixels são renderizados
        largura_px = self.colunas * TAMANHO_PIXEL
        altura_px = self.linhas * TAMANHO_PIXEL
        
        self.canvas = tk.Canvas(self.root, width=largura_px, height=altura_px, bg="#888888")
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._ao_clicar_no_pixel)

    def _selecionar_cor(self):
        """Abre a paleta de cores do sistema."""
        cor = colorchooser.askcolor(title="Selecione a cor para preencher")[1]
        if cor:
            self.cor_preenchimento = cor
            self.indicador_cor.config(bg=cor)

    def _desenhar_bitmap_inicial(self):
        """Desenha a matriz inteira como pixels de um Bitmap no Canvas."""
        for r in range(self.linhas):
            for c in range(self.colunas):
                char = self.matriz[r][c]
                cor = self.mapa_cores.get(char, "#FFFFFF")
                
                x1, y1 = c * TAMANHO_PIXEL, r * TAMANHO_PIXEL
                x2, y2 = x1 + TAMANHO_PIXEL, y1 + TAMANHO_PIXEL
                
                # Guarda a referência do retângulo retornado pelo Canvas
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="#CCCCCC")
                self.pixels_canvas[(r, c)] = rect_id

    def _ao_clicar_no_pixel(self, event):
        """Identifica a posição clicada e dispara a rotina com a Pilha."""
        coluna = event.x // TAMANHO_PIXEL
        linha = event.y // TAMANHO_PIXEL

        # Validação da Posição
        if not (0 <= linha < self.linhas and 0 <= coluna < self.colunas):
            messagebox.showerror("Erro", "Posição fora dos limites da matriz.")
            return

        char_alvo = self.matriz[linha][coluna]
        if char_alvo == '0':
            messagebox.showwarning("Aviso", "Não é possível preencher em cima das bordas (0).")
            return

        # Prepara a Pilha original[cite: 1] para a rotina recursiva
        pilha = PilhaPosicao(capacidade=self.linhas * self.colunas, num_colunas=self.colunas)
        pilha.empilhar(linha, coluna)

        self.contador_passos = 0
        self._preenchimento_recursivo_pilha(pilha, char_alvo)

    def _preenchimento_recursivo_pilha(self, pilha: PilhaPosicao, char_alvo: str):
        """
        Rotina RECURSIVA guiada pela classe PILHA[cite: 1] que atualiza os pixels na tela.
        """
        if pilha.esta_vazia():
            return

        r, c = pilha.desempilhar()

        if 0 <= r < self.linhas and 0 <= c < self.colunas and self.matriz[r][c] == char_alvo:
            # 1. Atualiza o estado lógico da matriz
            self.matriz[r][c] = '0'
            self.contador_passos += 1

            # 2. Atualiza a cor do pixel visualmente no Bitmap
            rect_id = self.pixels_canvas[(r, c)]
            self.canvas.itemconfig(rect_id, fill=self.cor_preenchimento)

            # 3. Pausa intermediária a cada P passos (atualiza a tela em tempo real)
            if self.passos_p > 0 and self.contador_passos % self.passos_p == 0:
                self.root.update()

            # 4. Empilha e chama recursivamente para os 4 vizinhos
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in direcoes:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.linhas and 0 <= nc < self.colunas and self.matriz[nr][nc] == char_alvo:
                    pilha.empilhar(nr, nc)
                    self._preenchimento_recursivo_pilha(pilha, char_alvo)


if __name__ == "__main__":
    ARQUIVO = "matriz_B.txt"
    PASSOS_P = 20  # Atualiza a interface gráfica a cada P pixels pintados

    root = tk.Tk()
    try:
        app = PaintBitmapApp(root, caminho_arquivo=Path(__file__).resolve().parent / ARQUIVO, passos_p=PASSOS_P)
        root.mainloop()
    except Exception as err:
        messagebox.showerror("Erro de Inicialização", str(err))