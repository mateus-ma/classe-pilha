#ifndef PILHA_HPP
#define PILHA_HPP

#include <cstddef>
#include "Excecoes.hpp"

template <typename T>
class Pilha {
private:
    T* dados;
    std::size_t capacidade;
    std::size_t topo; // Indica a quantidade de elementos atual

public:
    explicit Pilha(std::size_t cap) : capacidade(cap), topo(0) {
        if (cap == 0) {
            throw std::invalid_argument("A capacidade deve ser maior que zero.");
        }
        dados = new T[capacidade];
    }

    ~Pilha() {
        delete[] dados;
    }

    // Desabilita cópia rasa para evitar vazamento / double free
    Pilha(const Pilha&) = delete;
    Pilha& operator=(const Pilha&) = delete;

    void empilha(T dado) {
        if (pilha_esta_cheia()) {
            throw PilhaCheiaErro("A pilha atingiu a capacidade máxima.");
        }
        dados[topo++] = dado;
    }

    T desempilha() {
        if (pilha_esta_vazia()) {
            throw PilhaVaziaErro("A pilha está vazia.");
        }
        return dados[--topo];
    }

    bool pilha_esta_vazia() const {
        return topo == 0;
    }

    bool pilha_esta_cheia() const {
        return topo == capacidade;
    }

    void troca() {
        if (topo < 2) {
            throw PilhaVaziaErro("Pilha necessita de ao menos dois elementos para efetuar troca.");
        }
        T temp = dados[topo - 1];
        dados[topo - 1] = dados[topo - 2];
        dados[topo - 2] = temp;
    }

    std::size_t tamanho() const {
        return topo;
    }
};

#endif