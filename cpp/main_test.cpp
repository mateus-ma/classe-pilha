#include <iostream>
#include <cassert>
#include <chrono>
#include "Pilha.hpp"
#include "Excecoes.hpp"

void test_unitarios() {
    std::cout << "Executando testes unitarios (C++)... ";
    
    // Teste basico
    Pilha<int> p(3);
    assert(p.pilha_esta_vazia() == true);
    p.empilha(10);
    p.empilha(20);
    assert(p.tamanho() == 2);
    assert(p.desempilha() == 20);
    
    // Teste Troca
    p.empilha(30);
    p.troca(); // topo tem 30 e 10. Apos troca: topo tem 10 e 30
    assert(p.desempilha() == 10);
    assert(p.desempilha() == 30);
    
    // Teste Excecao PilhaCheiaErro
    Pilha<int> p_cheia(1);
    p_cheia.empilha(100);
    try {
        p_cheia.empilha(200);
        assert(false); // Nao deve chegar aqui
    } catch (const PilhaCheiaErro& e) {
        // Sucesso
    }

    // Teste Excecao PilhaVaziaErro
    Pilha<int> p_vazia(2);
    try {
        p_vazia.desempilha();
        assert(false);
    } catch (const PilhaVaziaErro& e) {
        // Sucesso
    }

    std::cout << "OK!" << std::endl;
}

void test_estresse() {
    std::size_t n = 10000000; // 10 Milhões
    std::cout << "\n[C++ Estresse - " << n << " elementos]" << std::endl;
    
    Pilha<long long> p(n);

    auto t1 = std::chrono::high_resolution_clock::now();
    for (std::size_t i = 0; i < n; ++i) {
        p.empilha(static_cast<long long>(i));
    }
    auto t2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> dur_empilha = t2 - t1;

    auto t3 = std::chrono::high_resolution_clock::now();
    for (std::size_t i = 0; i < n; ++i) {
        p.desempilha();
    }
    auto t4 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> dur_desempilha = t4 - t3;

    std::cout << "Tempo Empilhar: " << dur_empilha.count() << "s" << std::endl;
    std::cout << "Tempo Desempilhar: " << dur_desempilha.count() << "s" << std::endl;
}

int main() {
    test_unitarios();
    test_estresse();
    return 0;
}