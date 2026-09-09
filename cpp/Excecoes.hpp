#ifndef EXCECOES_HPP
#define EXCECOES_HPP

#include <stdexcept>
#include <string>

class PilhaCheiaErro : public std::runtime_error {
public:
    explicit PilhaCheiaErro(const std::string& msg = "Pilha Cheia") 
        : std::runtime_error(msg) {}
};

class PilhaVaziaErro : public std::runtime_error {
public:
    explicit PilhaVaziaErro(const std::string& msg = "Pilha Vazia") 
        : std::runtime_error(msg) {}
};

class TipoErro : public std::invalid_argument {
public:
    explicit TipoErro(const std::string& msg = "Tipo Incompativel") 
        : std::invalid_argument(msg) {}
};

#endif