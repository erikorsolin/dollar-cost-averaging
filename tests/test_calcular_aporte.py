import sys
import os
from unittest.mock import patch
import json
import tempfile

# Adicionar o diretório pai ao path para importar o módulo calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.calculator import calcular_aporte


class TestCalcularAporte:
    """Testes para a função calcular_aporte"""

    def test_carteira_balanceada_sem_aporte_necessario(self, sample_classes_simples):
        """Testa carteira já balanceada - aporte deve ser proporcional"""
        # Carteira: RF=1000 (66.7%), RV=500 (33.3%)
        # Metas: RF=70%, RV=30%
        # Com aporte de 300, deveria ficar RF=1050 (70%), RV=450 (30%)
        
        resultado = calcular_aporte(sample_classes_simples, 300.0)
        
        # Verificar totais
        assert resultado["totalAtualCarteira"] == 1500.0
        assert resultado["totalFinalCarteira"] == 1800.0
        
        # Verificar aportes
        aportes = resultado["aportes"]
        assert len(aportes) == 2
        
        # RF deveria receber mais aporte para chegar aos 70%
        rf_aporte = next(a for a in aportes if a["nome"] == "Renda Fixa")
        rv_aporte = next(a for a in aportes if a["nome"] == "Renda Variável")
        
        # RF: valor ideal = 1800 * 0.7 = 1260, então precisa 260
        # RV: valor ideal = 1800 * 0.3 = 540, então precisa 40
        # Total: 260 + 40 = 300 ✓
        
        assert abs(rf_aporte["aporte"] - 260.0) < 0.01
        assert abs(rv_aporte["aporte"] - 40.0) < 0.01
        assert abs(rf_aporte["novoValor"] - 1260.0) < 0.01
        assert abs(rv_aporte["novoValor"] - 540.0) < 0.01

    def test_carteira_diversificada_rebalanceamento(self, sample_classes_diversificada):
        """Testa rebalanceamento de carteira diversificada"""
        # Carteira total: 3500 (RF=2000, RVN=800, RVI=500, REITs=200)
        # Após aporte 770: total = 4270
        # Metas: RF=50%, RVN=30%, RVI=15%, REITs=5%
        
        resultado = calcular_aporte(sample_classes_diversificada, 770.0)
        
        assert resultado["totalAtualCarteira"] == 3500.0
        assert resultado["totalFinalCarteira"] == 4270.0
        
        aportes = resultado["aportes"]
        
        # Valores ideais após aporte
        rf_ideal = 4270 * 0.5  # 2135
        rvn_ideal = 4270 * 0.3  # 1281
        rvi_ideal = 4270 * 0.15  # 640.5
        reits_ideal = 4270 * 0.05  # 213.5
        
        rf = next(a for a in aportes if a["nome"] == "Renda Fixa")
        rvn = next(a for a in aportes if a["nome"] == "RV Nacional")
        rvi = next(a for a in aportes if a["nome"] == "RV Internacional")
        reits = next(a for a in aportes if a["nome"] == "REITs")
        
        # Verificar aportes necessários
        assert abs(rf["aporte"] - (rf_ideal - 2000)) < 0.01  # 135
        assert abs(rvn["aporte"] - (rvn_ideal - 800)) < 0.01  # 481
        assert abs(rvi["aporte"] - (rvi_ideal - 500)) < 0.01  # 140.5
        assert abs(reits["aporte"] - (reits_ideal - 200)) < 0.01  # 13.5
        
        # Verificar novos valores
        assert abs(rf["novoValor"] - rf_ideal) < 0.01
        assert abs(rvn["novoValor"] - rvn_ideal) < 0.01
        assert abs(rvi["novoValor"] - rvi_ideal) < 0.01
        assert abs(reits["novoValor"] - reits_ideal) < 0.01
        
        # Verificar que total dos aportes = aporte solicitado
        total_aportes = sum(a["aporte"] for a in aportes)
        assert abs(total_aportes - 770.0) < 0.01

    def test_carteira_muito_desbalanceada(self, sample_classes_desbalanceada):
        """Testa carteira muito desbalanceada"""
        # RF=5000 (98%), RV=100 (2%)
        # Metas: RF=40%, RV=60%
        
        resultado = calcular_aporte(sample_classes_desbalanceada, 1000.0)
        
        total_final = 6100.0  # 5100 + 1000
        rf_ideal = total_final * 0.4  # 2440
        rv_ideal = total_final * 0.6  # 3660
        
        aportes = resultado["aportes"]
        rf = next(a for a in aportes if a["nome"] == "Renda Fixa")
        rv = next(a for a in aportes if a["nome"] == "Renda Variável")
        
        # RF precisa diminuir (aporte = 0), RV precisa aumentar muito
        # Como RF já tem mais que o ideal, aporte = 0
        # Todo aporte vai para RV
        assert rf["aporte"] == 0.0
        assert abs(rv["aporte"] - 1000.0) < 0.01
        
        # Novos valores
        assert rf["novoValor"] == 5000.0  # Não mudou
        assert rv["novoValor"] == 1100.0  # 100 + 1000

    def test_classes_zeradas(self, sample_classes_zeradas):
        """Testa classes com valor atual zero"""
        # RF=1000, RV=0, Int=0
        # Metas: RF=60%, RV=25%, Int=15%
        
        resultado = calcular_aporte(sample_classes_zeradas, 500.0)
        
        total_final = 1500.0
        rf_ideal = total_final * 0.6  # 900
        rv_ideal = total_final * 0.25  # 375
        int_ideal = total_final * 0.15  # 225
        
        aportes = resultado["aportes"]
        
        # RF precisa diminuir, então aporte = 0
        # RV e Int precisam de aporte total
        rf = next(a for a in aportes if a["nome"] == "Renda Fixa")
        rv = next(a for a in aportes if a["nome"] == "Renda Variável")
        int_ativo = next(a for a in aportes if a["nome"] == "Internacional")
        
        # RF já tem mais que o ideal (1000 > 900), então aporte = 0
        assert rf["aporte"] == 0.0
        
        # Todo aporte vai para RV e Internacional
        assert abs(rv["aporte"] - 375.0) < 0.01
        assert abs(int_ativo["aporte"] - 125.0) < 0.01  # 500 - 375
        
        # Verificar total
        total_aportes = sum(a["aporte"] for a in aportes)
        assert abs(total_aportes - 500.0) < 0.01

    def test_aporte_zero(self, sample_classes_simples):
        """Testa comportamento com aporte zero"""
        resultado = calcular_aporte(sample_classes_simples, 0.0)
        
        # Sem aporte, valores não devem mudar
        for aporte in resultado["aportes"]:
            assert aporte["aporte"] == 0.0
            
        # Buscar valores originais
        original_rf = next(c for c in sample_classes_simples if c["nome"] == "Renda Fixa")["valorAtual"]
        original_rv = next(c for c in sample_classes_simples if c["nome"] == "Renda Variável")["valorAtual"]
        
        rf = next(a for a in resultado["aportes"] if a["nome"] == "Renda Fixa")
        rv = next(a for a in resultado["aportes"] if a["nome"] == "Renda Variável")
        
        assert rf["novoValor"] == original_rf
        assert rv["novoValor"] == original_rv

    def test_preservacao_metadados(self, sample_classes_simples):
        """Testa se metadados das classes são preservados"""
        resultado = calcular_aporte(sample_classes_simples, 100.0)
        
        for aporte in resultado["aportes"]:
            original = next(c for c in sample_classes_simples if c["nome"] == aporte["nome"])
            assert aporte["nome"] == original["nome"]
            assert aporte["valorAtual"] == original["valorAtual"]
            assert aporte["metaPercentual"] == original["metaPercentual"]

    def test_soma_aportes_igual_total(self, sample_classes_diversificada):
        """Testa se a soma dos aportes individuais é igual ao aporte total"""
        aporte_total = 1000.0
        resultado = calcular_aporte(sample_classes_diversificada, aporte_total)
        
        soma_aportes = sum(a["aporte"] for a in resultado["aportes"])
        assert abs(soma_aportes - aporte_total) < 0.01