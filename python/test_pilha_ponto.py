import time
import unittest
from excecoes import PilhaCheiaErro, PilhaVaziaErro, TipoErro
import numpy as np
from pilha_ponto import Pilha
from pilha_ponto import PontoArray


class TestPilhaUnitario(unittest.TestCase):

  def test_operacoes_basicas(self):
    # Pilha adaptada para guardar pontos (x, y)
    p = Pilha(capacidade=3)
    self.assertTrue(p.pilha_esta_vazia())

    ponto1 = np.array((10, 20), dtype=PontoArray().DTYPE)
    ponto2 = np.array((30, 40), dtype=PontoArray().DTYPE)

    p.empilha(ponto1)
    p.empilha(ponto2)
    self.assertEqual(p.tamanho(), 2)
    self.assertFalse(p.pilha_esta_vazia())

    res2 = p.desempilha()
    res1 = p.desempilha()

    self.assertEqual(res2['x'], 30)
    self.assertEqual(res2['y'], 40)
    self.assertEqual(res1['x'], 10)
    self.assertEqual(res1['y'], 20)
    self.assertTrue(p.pilha_esta_vazia())

  def test_excecao_pilha_cheia(self):
    p = Pilha(capacidade=2)
    p.empilha(np.array((1, 2), dtype=PontoArray().DTYPE))
    p.empilha(np.array((3, 4), dtype=PontoArray().DTYPE))
    self.assertTrue(p.pilha_esta_cheia())

    with self.assertRaises(PilhaCheiaErro):
      p.empilha(np.array((5, 6), dtype=PontoArray().DTYPE))

  def test_excecao_pilha_vazia(self):
    p = Pilha(capacidade=2)
    with self.assertRaises(PilhaVaziaErro):
      p.desempilha()

  def test_excecao_tipo_incompativel(self):
    p = Pilha(capacidade=5)
    with self.assertRaises(TipoErro):
      # Passando um tipo que não pode ser convertido para a struct Ponto (ex: texto)
      p.empilha('texto_invalido')

  def test_metodo_troca(self):
    p = Pilha(capacidade=5)
    p.empilha(np.array((100, 101), dtype=PontoArray().DTYPE))
    p.empilha(np.array((200, 201), dtype=PontoArray().DTYPE))

    p.troca()

    top1 = p.desempilha()
    top2 = p.desempilha()

    self.assertEqual(int(top1['x']), 100)
    self.assertEqual(int(top1['y']), 101)

    self.assertEqual(int(top2['x']), 200)
    self.assertEqual(int(top2['y']), 201)

  def test_troca_com_poucos_elementos(self):
    p = Pilha(capacidade=5)
    p.empilha(np.array((1, 1), dtype=PontoArray().DTYPE))
    with self.assertRaises(PilhaVaziaErro):
      p.troca()


class TestPilhaEstresse(unittest.TestCase):

  def test_estresse_1m_elementos(self):
    n = 1_000_000
    p = Pilha(capacidade=n)
    dtype_ponto = PontoArray().DTYPE

    inicio = time.time()
    for i in range(n):
      # Empilha tuplas/registros no formato (x, y)
      p.empilha(np.array((i, i * 2), dtype=dtype_ponto))
    tempo_empilhar = time.time() - inicio

    self.assertTrue(p.pilha_esta_cheia())
    self.assertEqual(p.tamanho(), n)

    inicio = time.time()
    for i in range(n - 1, -1, -1):
      val = p.desempilha()
      assert val['x'] == i
      assert val['y'] == i * 2
    tempo_desempilhar = time.time() - inicio

    print(f'\n[Python Estresse (PontoArray) - {n} elementos]')
    print(f'Tempo de Empilhar: {tempo_empilhar:.4f}s')
    print(f'Tempo de Desempilhar: {tempo_desempilhar:.4f}s')


if __name__ == '__main__':
  unittest.main()