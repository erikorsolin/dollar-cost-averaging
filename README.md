# 💸 Calculadora de Aporte Mensal

Este projeto implementa uma calculadora de aportes mensais baseada no **"Método Burro"** de investimentos, uma estratégia simples para manter uma carteira diversificada e balanceada ao longo do tempo.

## O que é o "Método Burro"?

O "Método Burro" (também conhecido como Dollar Cost Averaging ou DCA) é uma estratégia de investimento que consiste em:

1. **Aportes regulares**: Investir uma quantia fixa mensalmente, independente das condições do mercado
2. **Manutenção de proporções**: Manter sempre a mesma proporção entre diferentes classes de ativos
3. **Rebalanceamento automático**: Usar os aportes mensais para reequilibrar a carteira

### Por que "Método Burro"?

É chamado de "burro" porque não requer análise complexa de mercado, timing perfeito ou conhecimento avançado. Você simplesmente:
- Define sua alocação desejada (ex: 65% Renda Fixa, 35% Renda Variável)
- Aporta sempre o mesmo valor mensalmente
- Direciona o aporte para rebalancear automaticamente a carteira

## Como Funciona

A calculadora analisa sua carteira atual e determina como distribuir seu aporte mensal para manter as proporções desejadas:

1. **Carrega os dados** da sua carteira atual do arquivo JSON
2. **Calcula a alocação ideal** após o aporte
3. **Determina quanto aportar** em cada classe de ativo
4. **Atualiza o arquivo** com os novos valores para o próximo mês

### Exemplo Prático

Se sua meta é uma carteira diversificada com 4 classes de ativos:
- **Carteira atual**: R$ 3.500 total (desbalanceada)
- **Aporte mensal**: R$ 770
- **Metas**: 50% Renda Fixa, 30% Renda Variavel Nacional, 15% Renda Variavel Internacional, 5% REITs
- **Carteira após aporte**: R$ 4.270 total
- **Resultado**: Carteira automaticamente rebalanceada para as proporções desejadas

## Configuração Inicial

### 1. Arquivo de Dados (dados_carteira.json)

Crie um arquivo `dados_carteira.json` com suas classes de ativos e configurações:

```json
{
    "_comment": "Configuração da carteira - você pode adicionar quantas classes de ativos quiser. Os percentuais devem somar 100%.",
    "aporteMensalTotal": 770.0,
    "classesAtivos": [
        {
            "nome": "Renda Fixa",
            "valorAtual": 2000.00,
            "metaPercentual": 50.0
        },
        {
            "nome": "Renda Variável Nacional",
            "valorAtual": 800.00,
            "metaPercentual": 30.0
        },
        {
            "nome": "Renda Variável Internacional",
            "valorAtual": 500.00,
            "metaPercentual": 15.0
        },
        {
            "nome": "REITs",
            "valorAtual": 200.00,
            "metaPercentual": 5.0
        }
    ]
}
```

### 2. Configuração dos Parâmetros

**Estrutura Geral:**
- **aporteMensalTotal**: Valor que você pretende aportar mensalmente
- **classesAtivos**: Array com todas as suas classes de ativos

**Para cada Classe de Ativo:**
- **nome**: Nome descritivo da classe (ex: "Renda Fixa", "Ações Brasil", "Cripto")
- **valorAtual**: Valor atual investido nesta classe
- **metaPercentual**: Percentual desejado para esta classe (todos devem somar 100%)



## Como Usar

### Versão CLI (Linha de Comando)

#### Execução

```bash
make
```
ou

```bash
python3 calculator.py
```

### Versão Web (Interface Gráfica)

Para uma experiência mais intuitiva, você pode usar a **interface web**:

1. **Abra o arquivo** `web/index.html` no seu navegador
2. **Configure seus dados** diretamente na interface
3. **Veja os resultados** em tempo real

#### Funcionalidades da Interface Web:
- ✅ Cálculo em tempo real
- ✅ Interface responsiva (mobile-friendly)
- ✅ Validação automática dos percentuais
- ✅ Exemplo pré-carregado
- ✅ Funciona offline
- ✅ Totalmente independente (não usa arquivos externos)

📁 **Mais detalhes:** Veja [web/README.md](web/README.md) para documentação completa da interface web.

#### Saída Esperada (CLI)

```
==================================================
 ANÁLISE DE APORTE MENSAL
==================================================

CARTEIRA ANTES DO APORTE:

   Renda Fixa: R$ 2000.00 (57.1%)
   Renda Variável Nacional: R$ 800.00 (22.9%)
   Renda Variável Internacional: R$ 500.00 (14.3%)
   REITs: R$ 200.00 (5.7%)

PATRIMÔNIO TOTAL: R$ 3500.00

--------------------------------------------------

🎯 RECOMENDAÇÃO DE APORTE:

   ➡️  Renda Fixa: R$ 135.00
   ➡️  Renda Variável Nacional: R$ 481.00
   ➡️  Renda Variável Internacional: R$ 140.50
   ➡️  REITs: R$ 13.50

TOTAL APORTADO: R$ 770.00

--------------------------------------------------

CARTEIRA DEPOIS DO APORTE:

   Renda Fixa: R$ 2135.00 (50.0% | Meta: 50.0%) ✅
   Renda Variável Nacional: R$ 1281.00 (30.0% | Meta: 30.0%) ✅
   Renda Variável Internacional: R$ 640.50 (15.0% | Meta: 15.0%) ✅
   REITs: R$ 213.50 (5.0% | Meta: 5.0%) ✅

NOVO PATRIMÔNIO TOTAL: R$ 4270.00
==================================================

AVISO: O arquivo 'dados_carteira.json' foi atualizado com os novos totais!
```

## Fluxo de Trabalho Mensal

1. **Atualize os saldos reais** no arquivo `dados_carteira.json` com os valores atuais da sua carteira
2. **Execute o script** para obter a recomendação de aporte
3. **Faça os investimentos** conforme recomendado
4. **O arquivo será atualizado** automaticamente com os novos valores

## Personalização

Você pode ajustar facilmente:
- **Valor do aporte mensal**
- **Quantas classes de ativos quiser** (2, 5, 10+...)
- **Percentuais de alocação** para cada classe
- **Nomes das classes** (use os que fizerem sentido para você)

## Estrutura do Projeto

```
dollar-costa-averaging/
├── calculator.py              # Aplicação principal (CLI)
├── dados_carteira.json        # Configuração da carteira
├── Makefile                   # Comandos de build e execução
├── README.md                  # Documentação principal
├── LICENSE                    # Licença MIT
├── Dockerfile                 # Container para aplicação
├── docker-compose.yml         # Orquestração de containers
├── requirements.txt           # Dependências Python
├── tests/                     # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_calcular_aporte.py
│   ├── test_arquivo_json.py
│   ├── test_validacao.py
│   └── test_edge_cases.py
└── web/                       # Interface Web
    ├── index.html             # Página principal
    ├── style.css              # Estilos CSS
    ├── calculator.js          # Lógica JavaScript
    └── README.md              # Documentação da interface web
```


## Requisitos

- Python 3.6+
- Make (opcional, para facilitar a execução)
- Módulos padrão: `json`, `os`, `datetime`

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
