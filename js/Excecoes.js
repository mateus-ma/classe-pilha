class PilhaCheiaErro extends Error {
    constructor(message = "Pilha Cheia") {
        super(message);
        this.name = "PilhaCheiaErro";
    }
}

class PilhaVaziaErro extends Error {
    constructor(message = "Pilha Vazia") {
        super(message);
        this.name = "PilhaVaziaErro";
    }
}

class TipoErro extends TypeError {
    constructor(message = "Tipo Incompatível") {
        super(message);
        this.name = "TipoErro";
    }
}

module.exports = { PilhaCheiaErro, PilhaVaziaErro, TipoErro };