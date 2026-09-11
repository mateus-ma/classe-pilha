#ifndef PILHA_HPP
#define PILHA_HPP

#include <cstddef>
#include "Excecoes.hpp"

template <typename T>
class Pilha {
private:
    T* dados;
    std::size_t capacidade;
    std::size_t topo;

public:
    explicit Pilha(std::size_t cap);
    ~Pilha();

    // Desabilita cópia rasa para prevenir vazamento e double-free
    Pilha(const Pilha&) = delete;
    Pilha& operator=(const Pilha&) = delete;

    void empilha(T dado);
    T desempilha();
    bool pilha_esta_vazia() const;
    bool pilha_esta_cheia() const;
    void troca();
    std::size_t tamanho() const;
};

// Inclui a implementação das funções-membro baseadas em template
#include "Pilha.cpp"

#endif