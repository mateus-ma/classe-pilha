import numpy as np
from excecoes import PilhaCheiaErro, PilhaVaziaErro, TipoErro


import numpy as np


class PontoArray:

  def __init__(self, capacidade=1):
    self.capacidade = capacidade
    self.DTYPE = np.dtype([('x', 'int64'), ('y', 'int64')])
    self.buffer = np.zeros(capacidade, dtype=self.DTYPE)
    self.ultimo = 0

  def append(self, obj):
    if self.ultimo >= self.capacidade:
      raise IndexError('PontoArray cheio')
    self.buffer[self.ultimo] = obj
    self.ultimo += 1

  def pop(self):
    if self.ultimo == 0:
      raise IndexError('pop de PontoArray vazio')
    self.ultimo -= 1
    return self.buffer[self.ultimo]

  def __len__(self):
    return self.ultimo

  def __getitem__(self, ind):
    # Trata índice negativo com base nos elementos inseridos (self.ultimo)
    if ind < 0:
      ind += self.ultimo
    if ind < 0 or ind >= self.ultimo:
      raise IndexError('Índice fora dos limites do PontoArray')
    return self.buffer[ind]

  def __setitem__(self, ind, valor):
    # Trata índice negativo com base nos elementos inseridos (self.ultimo)
    if ind < 0:
      ind += self.ultimo
    if ind < 0 or ind >= self.ultimo:
      raise IndexError('Índice fora dos limites do PontoArray')
    self.buffer[ind] = valor

class Pilha:

  def __init__(self, capacidade: int):
    if capacidade <= 0:
      raise TipoErro('A capacidade deve ser um número inteiro positivo.')

    self._capacidade = capacidade
    self._dados = PontoArray(capacidade)

  def empilha(self, dado):
    if self.pilha_esta_cheia():
      raise PilhaCheiaErro(
          'A pilha está cheia. Não é possível empilhar mais elementos.'
      )

    try:
      self._dados.append(dado)
    except (TypeError, ValueError) as err:
      raise TipoErro(f"O dado '{dado}' não é compatível com PontoArray.") from err

  def desempilha(self):
    if self.pilha_esta_vazia():
      raise PilhaVaziaErro('A pilha está vazia. Não é possível desempilhar.')
    return self._dados.pop()

  def pilha_esta_vazia(self) -> bool:
    return len(self._dados) == 0

  def pilha_esta_cheia(self) -> bool:
    return len(self._dados) >= self._capacidade

  def troca(self):
    """Troca o elemento do topo com o elemento imediatamente abaixo."""
    if len(self._dados) < 2:
      raise PilhaVaziaErro('A pilha necessita de pelo menos dois elementos para efetuar a troca.')
      # Usa cópias/variável temporária para não sobrescrever a memória do ndarray
      
    topo = self._dados[-1].copy()
    abaixo = self._dados[-2].copy()
 
    self._dados[-1] = abaixo
    self._dados[-2] = topo

    self._dados[-1], self._dados[-2] = abaixo, topo

  def tamanho(self) -> int:
    return len(self._dados)