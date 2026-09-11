import sys


class TorreDeHanoi:

    def __init__(self, n_discos: int, passos_por_visualizacao: int = 1):
        self.n_discos = n_discos
        self.M = passos_por_visualizacao
        self.total_movimentos = 0

        # As três hastes/pinos representadas como pilhas (listas)
        # O disco N é o maior e o 1 é o menor.
        self.pinos = {
            "A": list(range(n_discos, 0, -1)),  # Pino Origem
            "B": [],  # Pino Auxiliar
            "C": [],  # Pino Destino
        }

    def desenhar_pinos(self):
        """Renderiza as pilhas de discos verticalmente no terminal."""
        largura_maxima = self.n_discos * 2 + 1
        altura_maxima = self.n_discos + 1

        print(f"\nEstado Atual ({self.total_movimentos} passos):")

        # Desenhar da camada mais alta para a base
        for nivel in range(altura_maxima - 1, -1, -1):
            linha = ""
            for nome_pino in ["A", "B", "C"]:
                pilha = self.pinos[nome_pino]
                if nivel < len(pilha):
                    disco = pilha[nivel]
                    # Representação do disco usando caracteres '#'
                    corpo_disco = "#" * (disco * 2 - 1)
                    desenho = corpo_disco.center(largura_maxima)
                else:
                    # Haste vazia
                    desenho = "|".center(largura_maxima)
                linha += desenho + " "
            print(linha)

        # Base dos pinos
        base_pino = "=" * largura_maxima
        print(f"{base_pino} {base_pino} {base_pino}")
        print(
            f"{'Pino A'.center(largura_maxima)} {'Pino B'.center(largura_maxima)} {'Pino C'.center(largura_maxima)}"
        )
        print()

    def aguardar_usuario(self):
        """Aguarda o usuário pressionar ENTER para continuar."""
        input("Pressione [ENTER] para continuar...")

    def mover_disco(self, origem: str, destino: str):
        """Move o disco do topo de uma haste para outra."""
        disco = self.pinos[origem].pop()
        self.pinos[destino].append(disco)
        self.total_movimentos += 1

        # Exibe o estado se o número acumulado de movimentos for múltiplo de M
        if self.total_movimentos % self.M == 0:
            self.desenhar_pinos()
            self.aguardar_usuario()

    def resolver_recursivo(
        self, n: int, origem: str, destino: str, auxiliar: str
    ):
        """Algoritmo recursivo para solucionar a Torre de Hanói."""
        if n == 1:
            self.mover_disco(origem, destino)
            return

        # 1. Mover n-1 discos da Origem para o Auxiliar
        self.resolver_recursivo(n - 1, origem, auxiliar, destino)

        # 2. Mover o maior disco restante da Origem para o Destino
        self.mover_disco(origem, destino)

        # 3. Mover os n-1 discos do Auxiliar para o Destino
        self.resolver_recursivo(n - 1, auxiliar, destino, origem)

    def executar(self):
        # Apresentação Inicial
        print("--- POSIÇÃO INICIAL ---")
        self.desenhar_pinos()
        self.aguardar_usuario()

        # Resolução
        self.resolver_recursivo(self.n_discos, "A", "C", "B")

        # Garantir exibição final caso o total de passos não seja múltiplo de M
        if self.total_movimentos % self.M != 0:
            print("--- POSIÇÃO FINAL ---")
            self.desenhar_pinos()
        else:
            print("--- POSIÇÃO FINAL ALCANÇADA ---")

        print(
            f"Problema resolvido em {self.total_movimentos} movimentos totais!"
        )


def main():
    print("========================================")
    print("      SIMULADOR - TORRE DE HANÓI        ")
    print("========================================\n")

    try:
        n = int(input("Informe o número N de discos: "))
        if n <= 0:
            print("O número de discos deve ser maior que zero.")
            return

        m_input = input("Informe o número M de passos por visualização (padrão = 1): ").strip()
        m = int(m_input) if m_input else 1
        if m <= 0:
            print("O valor de M deve ser pelo menos 1.")
            return

    except ValueError:
        print("Entrada inválida. Digite valores inteiros válidos.")
        return

    hanoi = TorreDeHanoi(n_discos=n, passos_por_visualizacao=m)
    hanoi.executar()


if __name__ == "__main__":
    main()