# Calculadora Dollar Cost Averaging

<img width="918" height="912" alt="image" src="https://github.com/user-attachments/assets/3df72602-f9fd-43e3-9013-3224d0c432f9" />


## Como usar

1. **Abra o arquivo `index.html`** no seu navegador
2. **Configure o aporte mensal** no campo "Aporte Mensal Total"
3. **Adicione suas classes de ativos** clicando em "+ Adicionar Classe":
   - Nome da classe (ex: "CDBs", "ETFs", "Ações Brasil")
   - Valor atual em reais
   - Meta percentual desejada
4. **Clique em "Carregar Exemplo"** se quiser ver um exemplo pronto
5. **Clique em "Calcular Aporte"** para ver a recomendação

## Funcionalidades

- **Cálculo automático** do aporte ideal para cada classe
- **Validação** dos percentuais (devem somar 100%)
- **Página inicia limpa** - adicione suas classes conforme necessário
- **Numeração automática** - as classes são renumeradas automaticamente
- **Interface responsiva** - funciona em desktop e mobile
- **Resultado detalhado** mostrando carteira antes e depois

## Estrutura dos arquivos

```
dollar-cost-averaging/
├── index.html      # Interface principal
├── style.css       # Estilos e layout responsivo
├── calculator.js   # Lógica de cálculo e manipulação DOM
└── README.md       # Este arquivo
```

## Exemplo de uso

1. **Carregue o exemplo padrão** clicando em "Carregar Exemplo"
2. **Modifique os valores** conforme sua carteira atual
3. **Ajuste as metas** para seus objetivos de alocação
4. **Ajuste o aporte** para refletir seu aporte
5. **Clique em "Caclular aporte"** para ver exatamente quanto aportar em cada classe/ativo


## Algoritmo

1. **Calcula o valor ideal** de cada classe baseado na meta percentual
2. **Determina a necessidade** de aporte para cada classe
3. **Distribui o aporte** priorizando classes mais distantes da meta
4. **Rebalanceia automaticamente** mantendo as proporções desejadas

---
