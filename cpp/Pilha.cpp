#ifndef PILHA_CPP
#define PILHA_CPP

#include "Pilha.hpp"

template <typename T>
Pilha<T>::Pilha(std::size_t cap) : capacidade(cap), topo(0) {
    if (cap == 0) {
        throw TipoErro("A capacidade deve ser maior que zero.");
    }
    dados = new T[capacidade];
}

template <typename T>
Pilha<T>::~Pilha() {
    delete[] dados;
}

template <typename T>
void Pilha<T>::empilha(T dado) {
    if (pilha_esta_cheia()) {
        throw PilhaCheiaErro("A pilha atingiu a capacidade máxima.");
    }
    dados[topo++] = dado;
}

template <typename T>
T Pilha<T>::desempilha() {
    if (pilha_esta_vazia()) {
        throw PilhaVaziaErro("A pilha está vazia.");
    }
    return dados[--topo];
}

template <typename T>
bool Pilha<T>::pilha_esta_vazia() const {
    return topo == 0;
}

template <typename T>
bool Pilha<T>::pilha_esta_cheia() const {
    return topo == capacidade;
}

template <typename T>
void Pilha<T>::troca() {
    if (topo < 2) {
        throw PilhaVaziaErro("A pilha necessita de ao menos dois elementos para efetuar a troca.");
    }
    T temp = dados[topo - 1];
    dados[topo - 1] = dados[topo - 2];
    dados[topo - 2] = temp;
}

template <typename T>
std::size_t Pilha<T>::tamanho() const {
    return topo;
}

#endif