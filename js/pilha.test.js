const assert = require('assert');
const Pilha = require('./Pilha');
const { PilhaCheiaErro, PilhaVaziaErro, TipoErro } = require('./Excecoes');

function executarTestesUnitarios() {
    console.log("Executando testes unitários (JavaScript)...");

    // Testes básicos
    const p = new Pilha(3, Int32Array);
    assert.strictEqual(p.pilha_esta_vazia(), true);
    
    p.empilha(10);
    p.empilha(20);
    assert.strictEqual(p.tamanho(), 2);
    assert.strictEqual(p.desempilha(), 20);

    // Teste de Troca
    p.empilha(30); // Estado atual: [10, 30]
    p.troca();     // Estado atual: [30, 10]
    assert.strictEqual(p.desempilha(), 10);
    assert.strictEqual(p.desempilha(), 30);

    // Teste PilhaCheiaErro
    const pCheia = new Pilha(1);
    pCheia.empilha(100);
    assert.throws(() => pCheia.empilha(200), PilhaCheiaErro);

    // Teste PilhaVaziaErro
    const pVazia = new Pilha(1);
    assert.throws(() => pVazia.desempilha(), PilhaVaziaErro);

    // Teste TipoErro (Apenas numeros sao permitidos em TypedArray)
    const pTipo = new Pilha(5);
    assert.throws(() => pTipo.empilha("texto"), TipoErro);
    assert.throws(() => pTipo.empilha(NaN), TipoErro);

    console.log("OK!");
}

function executarTesteEstresse() {
    const n = 10_000_000; // 5 Milhões
    console.log(`\n[JS Estresse - ${n} elementos]`);
    const p = new Pilha(n, Float64Array);

    const inicioEmpilhar = performance.now();
    for (let i = 0; i < n; i++) {
        p.empilha(i);
    }
    const fimEmpilhar = performance.now();

    const inicioDesempilhar = performance.now();
    for (let i = 0; i < n; i++) {
        p.desempilha();
    }
    const fimDesempilhar = performance.now();

    console.log(`Tempo Empilhar: ${((fimEmpilhar - inicioEmpilhar) / 1000).toFixed(4)}s`);
    console.log(`Tempo Desempilhar: ${((fimDesempilhar - inicioDesempilhar) / 1000).toFixed(4)}s`);
}

executarTestesUnitarios();
executarTesteEstresse();