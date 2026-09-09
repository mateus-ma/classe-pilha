import array
from excecoes import PilhaCheiaErro, PilhaVaziaErro, TipoErro

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
            raise ValueError("A capacidade deve ser um número inteiro positivo.")
        
        self._capacidade = capacidade
        self._typecode = typecode
        self._dados = array.array(typecode)

    def empilha(self, dado):
        if self.pilha_esta_cheia():
            raise PilhaCheiaErro("A pilha está cheia. Não é possível empilhar mais elementos.")
        
        try:
            self._dados.append(dado)
        except (TypeError, ValueError) as err:
            raise TipoErro(f"O dado '{dado}' não é compatível com o tipo estipulado '{self._typecode}'.") from err

    def desempilha():
        """Desempilha o dado do topo e o retorna."""
        if self.pilha_esta_vazia():
            raise PilhaVaziaErro("A pilha está vazia. Não é possível desempilhar.")
        return self._dados.pop()

    # Ajustado de acordo com a interface solicitada:
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