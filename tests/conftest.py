import pytest
import sys
import os

# Adicionar o diretório pai ao path para importar o módulo calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_classes_simples():
    """Fixture com classes de ativos simples (2 classes)"""
    return [
        {"nome": "Renda Fixa", "valorAtual": 1000.0, "metaPercentual": 70.0},
        {"nome": "Renda Variável", "valorAtual": 500.0, "metaPercentual": 30.0}
    ]

@pytest.fixture
def sample_classes_diversificada():
    """Fixture com carteira diversificada (4 classes)"""
    return [
        {"nome": "Renda Fixa", "valorAtual": 2000.0, "metaPercentual": 50.0},
        {"nome": "RV Nacional", "valorAtual": 800.0, "metaPercentual": 30.0},
        {"nome": "RV Internacional", "valorAtual": 500.0, "metaPercentual": 15.0},
        {"nome": "REITs", "valorAtual": 200.0, "metaPercentual": 5.0}
    ]

@pytest.fixture
def sample_classes_desbalanceada():
    """Fixture com carteira muito desbalanceada"""
    return [
        {"nome": "Renda Fixa", "valorAtual": 5000.0, "metaPercentual": 40.0},
        {"nome": "Renda Variável", "valorAtual": 100.0, "metaPercentual": 60.0}
    ]

@pytest.fixture
def sample_classes_zeradas():
    """Fixture com algumas classes zeradas"""
    return [
        {"nome": "Renda Fixa", "valorAtual": 1000.0, "metaPercentual": 60.0},
        {"nome": "Renda Variável", "valorAtual": 0.0, "metaPercentual": 25.0},
        {"nome": "Internacional", "valorAtual": 0.0, "metaPercentual": 15.0}
    ]