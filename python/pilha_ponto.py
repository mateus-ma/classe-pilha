import array
from excecoes import PilhaCheiaErro, PilhaVaziaErro, TipoErro
import numpy as np

class PontoArray:
    def __init__(self, capacidade = 1):
        self.capacidade = capacidade

        self.DTYPE = np.dtype([
            ('x', 'int64'),
            ('y', 'int64')
        ])

        self.buffer = np.zeros(capacidade, dtype=self.DTYPE)

        self.ultimo = 0

    def set(self, ind,  obj = np.dtype([
            ('x', 'int64'),
            ('y', 'int64')
        ])):
        self.buffer[ind] = obj

    def get(self, ind):
        return self.buffer[ind]

    def append(self, obj):
        self.buffer.set(self.ultimo, obj)
        self.ultimo += 1

class Pilha:
    """
    Implementação de Pilha sobre a biblioteca padrão 'array' de Python.
    
    Códigos de tipo ('typecode'):
      - 'i': inteiro assinado (int)
      - 'd': ponto flutuante de dupla precisão (float)
      - 'u': caractere unicode (char)
    """
    
    def __init__(self, capacidade: int, typecode: str = 'i'):
        if capacidade <= 0:
            raise TipoErro("A capacidade deve ser um número inteiro positivo.")

        self._capacidade = capacidade
        self._typecode = typecode
        self._dados = PontoArray(typecode, capacidade)

    def empilha(self, dado):
        if self.pilha_esta_cheia():
            raise PilhaCheiaErro("A pilha está cheia. Não é possível empilhar mais elementos.")
        
        try:
            self._dados.append(dado)
        except (TypeError, ValueError) as err:
            raise TipoErro(f"O dado '{dado}' não é compatível com o tipo estipulado '{self._typecode}'.") from err


    def desempilha(self):
        if self.pilha_esta_vazia():
            raise PilhaVaziaErro("A pilha está vazia. Não é possível desempilhar.")
        return self._dados.pop()

    def pilha_esta_vazia(self) -> bool:
        return len(self._dados) == 0

    def pilha_esta_cheia(self) -> bool:
        return len(self._dados) >= self._capacidade

    def troca(self):
        """Troca o elemento do topo com o elemento imediatamente abaixo."""
        if len(self._dados) < 2:
            raise PilhaVaziaErro("A pilha necessita de pelo menos dois elementos para efetuar a troca.")
        
        self._dados[-1], self._dados[-2] = self._dados[-2], self._dados[-1]

    def tamanho(self) -> int:
        return len(self._dados)

if __name__ == '__main__':
    x = PontoArray(10)
    pt = (1, 2)
    x.set(0, pt)
    print(x.get(0))