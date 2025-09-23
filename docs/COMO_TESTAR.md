# Como testar a Interface Web

## Opção 1: Servidor Python local

No diretório `web/`, execute:

```bash
cd web/
python3 -m http.server 8000
```

Depois abra no navegador: http://localhost:8000

## Opção 2: Abrir diretamente

Abra o arquivo `web/index.html` diretamente no seu navegador:

- **Windows**: Duplo clique no arquivo ou use Ctrl+O no navegador
- **Linux/Mac**: Clique direito → "Abrir com" → Navegador ou use Ctrl+O no navegador

## Exemplo de teste

1. A página carrega com um exemplo pré-configurado
2. Clique em "Carregar Exemplo" se quiser resetar
3. Modifique os valores conforme sua carteira
4. Clique em "Calcular Aporte" para ver o resultado

## Funcionalidades para testar

- ✅ Adicionar/remover classes de ativos
- ✅ Validação automática (percentuais devem somar 100%)
- ✅ Cálculo em tempo real
- ✅ Interface responsiva (teste no celular)
- ✅ Exemplo pré-carregado

## Teste completo

1. Use a interface web para configurar uma carteira
2. Teste com diferentes valores e proporções
3. Verifique se os cálculos estão corretos
4. Teste a validação (tente deixar percentuais diferentes de 100%)
5. Teste em dispositivos móveis