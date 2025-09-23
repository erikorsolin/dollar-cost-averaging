# Calculadora Dollar Cost Averaging

Calculadora de aportes mensais usando o "Método Burro" - estratégia que rebalanceia automaticamente sua carteira a cada aporte, mantendo as proporções desejadas.

## Versões Disponíveis

### 📁 CLI (Linha de Comando)
Aplicação Python que lê configurações de um arquivo JSON e calcula os aportes.

**Como usar:**
```bash
# Executar
make
# ou
python3 calculator.py
```

**Configuração (dados_carteira.json):**
```json
{
    "aporteMensalTotal": 800.0,
    "classesAtivos": [
        {
            "nome": "Renda Fixa",
            "valorAtual": 2000.00,
            "metaPercentual": 65.0
        },
        {
            "nome": "Renda Variável",
            "valorAtual": 1000.00,
            "metaPercentual": 35.0
        }
    ]
}
```

### 🌐 Interface Web
Versão web com interface gráfica - não depende de arquivos JSON.

**Como usar:**
```bash
# Abrir no navegador
open docs/index.html
# ou servidor local
cd docs/
python3 -m http.server 8000
```

📖 **Documentação completa:** [docs/README.md](docs/README.md)

## Algoritmo

1. Calcula valor ideal de cada classe baseado na meta percentual
2. Determina necessidade de aporte para cada classe  
3. Distribui o aporte priorizando classes mais distantes da meta
4. Rebalanceia automaticamente mantendo proporções desejadas

## Requisitos

- Python 3.6+
- Módulos padrão: `json`, `os`, `datetime`

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
