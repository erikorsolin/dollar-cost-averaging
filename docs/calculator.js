// Estado da aplicação
let classes = [];
let contadorClasses = 0;

// Elementos DOM
const aporteTotalInput = document.getElementById('aporte-total');
const classesContainer = document.getElementById('classes-container');
const addClasseBtn = document.getElementById('add-classe');
const exemploPresetBtn = document.getElementById('exemplo-preset');
const calcularBtn = document.getElementById('calcular');
const limparBtn = document.getElementById('limpar');
const resultadoDiv = document.getElementById('resultado');
const totalPercentualSpan = document.getElementById('total-percentual');
const warningPercentual = document.getElementById('warning-percentual');

// Inicialização
document.addEventListener('DOMContentLoaded', function () {
    // Adicionar eventos
    addClasseBtn.addEventListener('click', function () {
        adicionarClasse();
    });
    exemploPresetBtn.addEventListener('click', carregarExemplo);
    calcularBtn.addEventListener('click', calcularAporte);
    limparBtn.addEventListener('click', limparTudo);

    // Inicializar sem exemplo - página limpa
    atualizarTotalPercentual();
});

function adicionarClasse(nome = '', valorAtual = '', metaPercentual = '') {
    contadorClasses++;
    const classeId = `classe-${contadorClasses}`;

    const classeDiv = document.createElement('div');
    classeDiv.className = 'classe-item';
    classeDiv.id = classeId;

    classeDiv.innerHTML = `
        <div class="classe-header">
            <div class="classe-numero">${contadorClasses}</div>
            <button type="button" class="remove-classe" onclick="removerClasse('${classeId}')">×</button>
        </div>
        <div class="classe-fields">
            <div class="form-group">
                <label>Nome da Classe:</label>
                <input type="text" class="nome-classe" placeholder="Ex: Renda Fixa, Ações Brasil..." value="${nome}">
            </div>
            <div class="form-group">
                <label>Valor Atual (R$):</label>
                <input type="number" class="valor-atual" min="0" step="0.01" placeholder="0.00" value="${valorAtual}">
            </div>
            <div class="form-group">
                <label>Meta (%):</label>
                <input type="number" class="meta-percentual" min="0" max="100" step="0.01" placeholder="0.0" value="${metaPercentual}">
            </div>
        </div>
    `;

    classesContainer.appendChild(classeDiv);

    // Adicionar eventos de mudança para atualizar total
    const inputs = classeDiv.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', atualizarTotalPercentual);
    });

    atualizarTotalPercentual();
}

function removerClasse(classeId) {
    const classeDiv = document.getElementById(classeId);
    if (classeDiv) {
        classeDiv.remove();
        renumerarClasses();
        atualizarTotalPercentual();
    }
}

function renumerarClasses() {
    const classeItems = document.querySelectorAll('.classe-item');
    contadorClasses = classeItems.length;

    classeItems.forEach((item, index) => {
        const numeroDiv = item.querySelector('.classe-numero');
        if (numeroDiv) {
            numeroDiv.textContent = index + 1;
        }

        // Atualizar o ID e onclick do botão remover
        const novoId = `classe-${index + 1}`;
        item.id = novoId;
        const removeBtn = item.querySelector('.remove-classe');
        if (removeBtn) {
            removeBtn.setAttribute('onclick', `removerClasse('${novoId}')`);
        }
    });
}

function atualizarTotalPercentual() {
    const metasInputs = document.querySelectorAll('.meta-percentual');
    let total = 0;

    metasInputs.forEach(input => {
        const valor = parseFloat(input.value) || 0;
        total += valor;
    });

    totalPercentualSpan.textContent = total.toFixed(1);

    if (Math.abs(total - 100) > 0.01) {
        warningPercentual.classList.remove('hidden');
        totalPercentualSpan.style.color = '#dc3545';
    } else {
        warningPercentual.classList.add('hidden');
        totalPercentualSpan.style.color = '#28a745';
    }
}

function carregarExemplo() {
    // Limpar classes existentes
    classesContainer.innerHTML = '';
    contadorClasses = 0;

    // Adicionar exemplo padrão
    adicionarClasse('CDBs', '2240.00', '65.0');
    adicionarClasse('ETFs', '1100.00', '35.0');

    // Definir aporte exemplo
    aporteTotalInput.value = '800.00';
}

function limparTudo() {
    classesContainer.innerHTML = '';
    contadorClasses = 0;
    aporteTotalInput.value = '';
    resultadoDiv.classList.add('hidden');
    atualizarTotalPercentual();
}

function coletarDados() {
    const aporteMensalTotal = parseFloat(aporteTotalInput.value) || 0;
    const classesAtivos = [];

    const classeItems = document.querySelectorAll('.classe-item');

    classeItems.forEach(item => {
        const nome = item.querySelector('.nome-classe').value.trim();
        const valorAtual = parseFloat(item.querySelector('.valor-atual').value) || 0;
        const metaPercentual = parseFloat(item.querySelector('.meta-percentual').value) || 0;

        if (nome) {
            classesAtivos.push({
                nome: nome,
                valorAtual: valorAtual,
                metaPercentual: metaPercentual
            });
        }
    });

    return {
        aporteMensalTotal: aporteMensalTotal,
        classesAtivos: classesAtivos
    };
}

function validarDados(dados) {
    const erros = [];

    if (dados.aporteMensalTotal <= 0) {
        erros.push('Aporte mensal deve ser maior que zero');
    }

    if (dados.classesAtivos.length === 0) {
        erros.push('Adicione pelo menos uma classe de ativo');
    }

    const totalPercentual = dados.classesAtivos.reduce((total, classe) => total + classe.metaPercentual, 0);
    if (Math.abs(totalPercentual - 100) > 0.01) {
        erros.push(`Os percentuais das metas somam ${totalPercentual.toFixed(1)}% ao invés de 100%`);
    }

    return erros;
}

function calcularAporteAlgoritmo(classesAtivos, aporteTotal) {
    // Implementação do mesmo algoritmo do Python
    const totalAtualCarteira = classesAtivos.reduce((total, classe) => total + classe.valorAtual, 0);
    const totalFinalCarteira = totalAtualCarteira + aporteTotal;

    const aportes = [];
    let aporteRestante = aporteTotal;

    // Calcular necessidades para cada classe
    const necessidades = classesAtivos.map(classe => {
        const valorIdeal = totalFinalCarteira * (classe.metaPercentual / 100);
        const necessidade = valorIdeal - classe.valorAtual;

        return {
            nome: classe.nome,
            valorAtual: classe.valorAtual,
            metaPercentual: classe.metaPercentual,
            valorIdeal: valorIdeal,
            necessidade: necessidade
        };
    });

    // Primeira passada: distribuir aporte baseado nas necessidades
    necessidades.forEach(necessidade => {
        let aporteClasse = 0;

        if (aporteRestante > 0 && necessidade.necessidade > 0) {
            aporteClasse = Math.min(aporteRestante, necessidade.necessidade);
            aporteRestante -= aporteClasse;
        }

        aportes.push({
            nome: necessidade.nome,
            valorAtual: necessidade.valorAtual,
            metaPercentual: necessidade.metaPercentual,
            aporte: aporteClasse,
            novoValor: necessidade.valorAtual + aporteClasse
        });
    });

    // Se ainda sobrou aporte, distribuir proporcionalmente
    if (aporteRestante > 0) {
        const totalPercentual = classesAtivos.reduce((total, classe) => total + classe.metaPercentual, 0);

        aportes.forEach(aporte => {
            const proporcao = aporte.metaPercentual / totalPercentual;
            const aporteAdicional = aporteRestante * proporcao;
            aporte.aporte += aporteAdicional;
            aporte.novoValor += aporteAdicional;
        });
    }

    return {
        totalAtualCarteira: totalAtualCarteira,
        totalFinalCarteira: totalFinalCarteira,
        aportes: aportes
    };
}

function calcularAporte() {
    const dados = coletarDados();
    const erros = validarDados(dados);

    if (erros.length > 0) {
        alert('Erros encontrados:\n' + erros.join('\n'));
        return;
    }

    const resultado = calcularAporteAlgoritmo(dados.classesAtivos, dados.aporteMensalTotal);
    exibirResultado(resultado);
}

function exibirResultado(resultado) {
    // Carteira ANTES
    const carteiraAntes = document.getElementById('carteira-antes');
    carteiraAntes.innerHTML = '';

    resultado.aportes.forEach(aporte => {
        const percentualAtual = resultado.totalAtualCarteira > 0 ?
            (aporte.valorAtual / resultado.totalAtualCarteira * 100) : 0;

        const div = document.createElement('div');
        div.className = 'classe-resultado';
        div.innerHTML = `
            <span><strong>${aporte.nome}:</strong> R$ ${aporte.valorAtual.toFixed(2)}</span>
            <span>(${percentualAtual.toFixed(1)}%)</span>
        `;
        carteiraAntes.appendChild(div);
    });

    document.getElementById('total-antes').textContent = resultado.totalAtualCarteira.toFixed(2);

    // Recomendação de APORTE
    const recomendacaoAporte = document.getElementById('recomendacao-aporte');
    recomendacaoAporte.innerHTML = '';

    resultado.aportes.forEach(aporte => {
        const div = document.createElement('div');
        div.className = aporte.aporte > 0 ? 'aporte-item' : 'aporte-item zero';

        const texto = aporte.aporte > 0 ?
            `${aporte.nome}: R$ ${aporte.aporte.toFixed(2)}` :
            `${aporte.nome}: R$ 0.00 (não necessário)`;

        div.innerHTML = `<span>${texto}</span>`;
        recomendacaoAporte.appendChild(div);
    });

    const totalAporte = resultado.aportes.reduce((total, aporte) => total + aporte.aporte, 0);
    document.getElementById('total-aporte-calculado').textContent = totalAporte.toFixed(2);

    // Carteira DEPOIS
    const carteiraDepois = document.getElementById('carteira-depois');
    carteiraDepois.innerHTML = '';

    resultado.aportes.forEach(aporte => {
        const percentualNovo = (aporte.novoValor / resultado.totalFinalCarteira * 100);
        const meta = aporte.metaPercentual;
        const status = Math.abs(percentualNovo - meta) < 1 ? 'OK' : 'DESBALANCEADO';
        const classeStatus = Math.abs(percentualNovo - meta) < 1 ? '' : 'warning';

        const div = document.createElement('div');
        div.className = `classe-resultado ${classeStatus}`;
        div.innerHTML = `
            <span><strong>${aporte.nome}:</strong> R$ ${aporte.novoValor.toFixed(2)}</span>
            <span>(${percentualNovo.toFixed(1)}% | Meta: ${meta.toFixed(1)}%) [${status}]</span>
        `;
        carteiraDepois.appendChild(div);
    });

    document.getElementById('total-depois').textContent = resultado.totalFinalCarteira.toFixed(2);

    // Mostrar resultado
    resultadoDiv.classList.remove('hidden');
    resultadoDiv.scrollIntoView({ behavior: 'smooth' });
}