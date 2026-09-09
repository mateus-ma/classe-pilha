import time
import unittest
import array
from excecoes import PilhaCheiaErro, PilhaVaziaErro, TipoErro
from pilha import Pilha

class TestPilhaUnitario(unittest.TestCase):
    def test_operacoes_basicas(self):
        p = Pilha(capacidade=3, typecode='i')
        self.assertTrue(p.pilha_esta_vazia())
        
        p.empilha(10)
        p.empilha(20)
        self.assertEqual(p.tamanho(), 2)
        self.assertFalse(p.pilha_esta_vazia())
        
        self.assertEqual(p.desempilha(), 20)
        self.assertEqual(p.desempilha(), 10)
        self.assertTrue(p.pilha_esta_vazia())

    def test_excecao_pilha_cheia(self):
        p = Pilha(capacidade=2, typecode='i')
        p.empilha(1)
        p.empilha(2)
        self.assertTrue(p.pilha_esta_cheia())
        with self.assertRaises(PilhaCheiaErro):
            p.empilha(3)

    def test_excecao_pilha_vazia(self):
        p = Pilha(capacidade=2, typecode='i')
        with self.assertRaises(PilhaVaziaErro):
            p.desempilha()

    def test_excecao_tipo_incompativel(self):
        p = Pilha(capacidade=5, typecode='i')  # Apenas inteiros
        with self.assertRaises(TipoErro):
            p.empilha("texto_invalido")

    def test_metodo_troca(self):
        p = Pilha(capacidade=5, typecode='i')
        p.empilha(100)
        p.empilha(200)
        p.troca()
        self.assertEqual(p.desempilha(), 100)
        self.assertEqual(p.desempilha(), 200)

    def test_troca_com_poucos_elementos(self):
        p = Pilha(capacidade=5, typecode='i')
        p.empilha(1)
        with self.assertRaises(PilhaVaziaErro):
            p.troca()


class TestPilhaEstresse(unittest.TestCase):
    def test_estresse_1m_elementos(self):
        n = 1_000_000
        p = Pilha(capacidade=n, typecode='i')
        
        inicio = time.time()
        for i in range(n):
            p.empilha(i)
        tempo_empilhar = time.time() - inicio
        
        self.assertTrue(p.pilha_esta_cheia())
        self.assertEqual(p.tamanho(), n)
        
        inicio = time.time()
        for i in range(n - 1, -1, -1):
            val = p.desempilha()
            assert val == i
        tempo_desempilhar = time.time() - inicio
        
        print(f"\n[Python Estresse - {n} elementos]")
        print(f"Tempo de Empilhar: {tempo_empilhar:.4f}s")
        print(f"Tempo de Desempilhar: {tempo_desempilhar:.4f}s")


if __name__ == "__main__":
    unittest.main()