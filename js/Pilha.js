const { PilhaCheiaErro, PilhaVaziaErro, TipoErro } = require('./Excecoes');

class Pilha {
    /**
     * @param {number} capacidade - Capacidade máxima da pilha.
     * @param {Function} TypedArrayConstr - Construtor de TypedArray (ex: Int32Array, Float64Array).
     */
    constructor(capacidade, TypedArrayConstr = Int32Array) {
        if (capacidade <= 0) {
            throw new Error("Capacidade deve ser maior que zero.");
        }
        this._capacidade = capacidade;
        this._dados = new TypedArrayConstr(capacidade);
        this._topo = 0; // Quantidade atual de elementos
    }

    empilha(dado) {
        if (this.pilha_esta_cheia()) {
            throw new PilhaCheiaErro("A pilha atingiu a sua capacidade máxima.");
        }

        if (typeof dado !== 'number' || Number.isNaN(dado)) {
            throw new TipoErro(`Dado inválido ou tipo incompatível: ${dado}`);
        }

        this._dados[this._topo] = dado;
        this._topo++;
    }

    desempilha() {
        if (this.pilha_esta_vazia()) {
            throw new PilhaVaziaErro("A pilha está vazia.");
        }

        this._topo--;
        const elemento = this._dados[this._topo];
        return elemento;
    }

    pilha_esta_vazia() {
        return this._topo === 0;
    }

    pilha_esta_cheia() {
        return this._topo === this._capacidade;
    }

    troca() {
        if (this._topo < 2) {
            throw new PilhaVaziaErro("Pilha precisa de pelo menos 2 elementos para efetuar a troca.");
        }

        const temp = this._dados[this._topo - 1];
        this._dados[this._topo - 1] = this._dados[this._topo - 2];
        this._dados[this._topo - 2] = temp;
    }

    tamanho() {
        return this._topo;
    }
}

module.exports = Pilha;