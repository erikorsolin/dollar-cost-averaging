# Interface Web - Calculadora Dollar Cost Averaging

Esta é a versão web da calculadora de Dollar Cost Averaging (Método Burro), que permite realizar os mesmos cálculos da aplicação CLI diretamente no navegador com um visual profissional e limpo.

## Como usar

1. **Abra o arquivo `index.html`** no seu navegador
2. **Configure o aporte mensal** no campo "Aporte Mensal Total"
3. **Adicione suas classes de ativos**:
   - Nome da classe (ex: "CDBs", "ETFs", "Ações Brasil")
   - Valor atual em reais
   - Meta percentual desejada
4. **Clique em "Calcular Aporte"** para ver a recomendação

## Funcionalidades

- ✅ **Cálculo automático** do aporte ideal para cada classe
- ✅ **Validação** dos percentuais (devem somar 100%)
- ✅ **Exemplo pré-carregado** para demonstração
- ✅ **Interface responsiva** - funciona em desktop e mobile
- ✅ **Resultado detalhado** mostrando carteira antes e depois

## Estrutura dos arquivos

```
web/
├── index.html      # Interface principal
├── style.css       # Estilos e layout responsivo
├── calculator.js   # Lógica de cálculo e manipulação DOM
└── README.md       # Este arquivo
```

## Exemplo de uso

1. **Carregue o exemplo padrão** clicando em "Carregar Exemplo"
2. **Modifique os valores** conforme sua carteira atual
3. **Ajuste as metas** para seus objetivos de alocação
4. **Calculate** para ver exatamente quanto aportar em cada classe

## Compatibilidade

- 🌐 **Funciona offline** - não precisa de servidor
- 📱 **Mobile-friendly** - interface adaptada para celular
- ⚡ **Cálculo instantâneo** - resultado em tempo real
- 🎯 **Standalone** - não depende de arquivos externos
- 💼 **Visual profissional** - design limpo e minimalista

## Algoritmo

O algoritmo implementado é exatamente o mesmo da versão CLI:

1. **Calcula o valor ideal** de cada classe baseado na meta percentual
2. **Determina a necessidade** de aporte para cada classe
3. **Distribui o aporte** priorizando classes mais distantes da meta
4. **Rebalanceia automaticamente** mantendo as proporções desejadas

---

💡 **Dica:** Esta interface web tem design profissional e é completamente independente, calculando tudo baseado nos valores inseridos nos formulários!