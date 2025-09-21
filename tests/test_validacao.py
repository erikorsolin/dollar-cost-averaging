import sys
import os

# Adicionar o diretório pai ao path para importar o módulo calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import calcular_aporte


class TestValidacao:
    """Testes de validação de entrada e consistência"""

    def test_percentuais_somam_100_exato(self):
        """Testa cálculo com percentuais que somam exatamente 100%"""
        classes = [
            {"nome": "A", "valorAtual": 1000.0, "metaPercentual": 25.0},
            {"nome": "B", "valorAtual": 1000.0, "metaPercentual": 25.0},
            {"nome": "C", "valorAtual": 1000.0, "metaPercentual": 25.0},
            {"nome": "D", "valorAtual": 1000.0, "metaPercentual": 25.0}
        ]
        
        resultado = calcular_aporte(classes, 400.0)
        
        # Verificar que cálculo funciona normalmente
        assert resultado["totalAtualCarteira"] == 4000.0
        assert resultado["totalFinalCarteira"] == 4400.0
        
        # Cada classe deveria receber 100 para ficar com 1100 (25% de 4400)
        for aporte in resultado["aportes"]:
            assert abs(aporte["aporte"] - 100.0) < 0.01
            assert abs(aporte["novoValor"] - 1100.0) < 0.01



    def test_metas_percentuais_zero(self):
        """Testa classes com meta percentual zero"""
        classes = [
            {"nome": "Principal", "valorAtual": 1000.0, "metaPercentual": 100.0},
            {"nome": "Zero", "valorAtual": 500.0, "metaPercentual": 0.0}
        ]
        
        resultado = calcular_aporte(classes, 200.0)
        
        # Classe Zero deveria ter valor ideal = 0
        # Principal deveria receber todo valor
        
        principal = next(ap for ap in resultado["aportes"] if ap["nome"] == "Principal")
        zero = next(ap for ap in resultado["aportes"] if ap["nome"] == "Zero")
        
        # Zero já tem valor > 0, mas meta é 0, então aporte = 0
        assert zero["aporte"] == 0.0
        # Todo aporte vai para Principal
        assert abs(principal["aporte"] - 200.0) < 0.01


    def test_uma_classe_apenas(self):
        """Testa comportamento com apenas uma classe de ativo"""
        classes = [
            {"nome": "Unica", "valorAtual": 2000.0, "metaPercentual": 100.0}
        ]
        
        resultado = calcular_aporte(classes, 500.0)
        
        assert len(resultado["aportes"]) == 1
        assert resultado["totalAtualCarteira"] == 2000.0
        assert resultado["totalFinalCarteira"] == 2500.0
        
        unica = resultado["aportes"][0]
        assert unica["nome"] == "Unica"
        assert abs(unica["aporte"] - 500.0) < 0.01
        assert abs(unica["novoValor"] - 2500.0) < 0.01

    def test_muitas_classes_pequenas(self):
        """Testa comportamento com muitas classes de valores pequenos"""
        classes = []
        for i in range(10):
            classes.append({
                "nome": f"Classe_{i}",
                "valorAtual": 100.0,
                "metaPercentual": 10.0
            })
        
        resultado = calcular_aporte(classes, 1000.0)
        
        assert len(resultado["aportes"]) == 10
        assert resultado["totalAtualCarteira"] == 1000.0  # 10 * 100
        assert resultado["totalFinalCarteira"] == 2000.0
        
        # Cada classe deveria ficar com 200 (10% de 2000)
        # Então cada uma precisa de aporte = 100
        for aporte in resultado["aportes"]:
            assert abs(aporte["aporte"] - 100.0) < 0.01
            assert abs(aporte["novoValor"] - 200.0) < 0.01

    def test_consistencia_matematica(self):
        """Teste geral de consistência matemática"""
        classes = [
            {"nome": "A", "valorAtual": 1234.56, "metaPercentual": 33.33},
            {"nome": "B", "valorAtual": 2345.67, "metaPercentual": 44.44},
            {"nome": "C", "valorAtual": 3456.78, "metaPercentual": 22.23}
        ]
        
        aporte_total = 987.65
        resultado = calcular_aporte(classes, aporte_total)
        
        # Verificações de consistência
        total_inicial = sum(c["valorAtual"] for c in classes)
        assert abs(resultado["totalAtualCarteira"] - total_inicial) < 0.01
        
        total_final_esperado = total_inicial + aporte_total
        assert abs(resultado["totalFinalCarteira"] - total_final_esperado) < 0.01
        
        # Soma dos aportes deve ser igual ao aporte total
        soma_aportes = sum(a["aporte"] for a in resultado["aportes"])
        assert abs(soma_aportes - aporte_total) < 0.01
        
        # Soma dos novos valores deve ser igual ao total final
        soma_novos_valores = sum(a["novoValor"] for a in resultado["aportes"])
        assert abs(soma_novos_valores - resultado["totalFinalCarteira"]) < 0.01
        
        # Valor atual + aporte = novo valor (para cada classe)
        for i, aporte in enumerate(resultado["aportes"]):
            classe_original = classes[i]
            valor_esperado = classe_original["valorAtual"] + aporte["aporte"]
            assert abs(aporte["novoValor"] - valor_esperado) < 0.01