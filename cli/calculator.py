import json
import os
from datetime import datetime

NOME_ARQUIVO_DADOS = "dados_carteira.json"


def carregar_dados_json():
    """Lê o arquivo de dados .json e retorna como um dicionário Python."""
    if not os.path.exists(NOME_ARQUIVO_DADOS):
        raise FileNotFoundError(f"Arquivo '{NOME_ARQUIVO_DADOS}' não encontrado. Crie o arquivo com os dados iniciais.")

    with open(NOME_ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        
    total_percentual = sum(classe["metaPercentual"] for classe in dados["classesAtivos"])
    if abs(total_percentual - 100.0) > 0.01:
        print(f"AVISO: Os percentuais das metas somam {total_percentual}% ao invés de 100%!")
        
    return dados


def salvar_dados_json(dados_carteira):
    """Gera e salva o novo conteúdo no arquivo de dados .json para o próximo mês."""
    dados_para_salvar = {
        "_comment": f"Valores atualizados automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. No proximo mes, atualize estes saldos antes de rodar o script.",
        "aporteMensalTotal": dados_carteira["aporteMensalTotal"],
        "classesAtivos": []
    }
    
    # Copiar classes de ativos com valores atualizados
    for classe in dados_carteira["classesAtivos"]:
        dados_para_salvar["classesAtivos"].append({
            "nome": classe["nome"],
            "valorAtual": round(classe["valorAtual"], 2),
            "metaPercentual": classe["metaPercentual"]
        })
    
    with open(NOME_ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
    print(f"\nAVISO: O arquivo '{NOME_ARQUIVO_DADOS}' foi atualizado com os novos totais!")


def calcular_aporte(classes_ativos, aporte_total):
    """Calcula quanto aportar em cada classe de ativo para rebalancear a carteira."""
    
    # Calcular totais atuais
    total_atual_carteira = sum(classe["valorAtual"] for classe in classes_ativos)
    total_final_carteira = total_atual_carteira + aporte_total
    
    # Calcular aportes necessários para cada classe
    aportes = []
    aporte_restante = aporte_total
    
    # Calcular o quanto cada classe precisa para atingir a meta
    necessidades = []
    for classe in classes_ativos:
        valor_ideal = total_final_carteira * (classe["metaPercentual"] / 100)
        necessidade = valor_ideal - classe["valorAtual"]
        necessidades.append({
            "nome": classe["nome"],
            "valorAtual": classe["valorAtual"],
            "metaPercentual": classe["metaPercentual"],
            "valorIdeal": valor_ideal,
            "necessidade": necessidade
        })
    
    # Calcular aportes respeitando o limite do aporte total
    for i, necessidade in enumerate(necessidades):
        if aporte_restante <= 0:
            aporte_classe = 0
        elif necessidade["necessidade"] <= 0:
            aporte_classe = 0
        else:
            aporte_classe = min(aporte_restante, necessidade["necessidade"])
        
        aporte_restante -= aporte_classe
        
        aportes.append({
            "nome": necessidade["nome"],
            "valorAtual": necessidade["valorAtual"],
            "metaPercentual": necessidade["metaPercentual"],
            "aporte": aporte_classe,
            "novoValor": necessidade["valorAtual"] + aporte_classe
        })
    
    # Se ainda sobrou aporte, distribuir proporcionalmente
    if aporte_restante > 0:
        total_percentual = sum(classe["metaPercentual"] for classe in classes_ativos)
        for aporte in aportes:
            proporcao = aporte["metaPercentual"] / total_percentual
            aporte_adicional = aporte_restante * proporcao
            aporte["aporte"] += aporte_adicional
            aporte["novoValor"] += aporte_adicional
    
    return {
        "totalAtualCarteira": total_atual_carteira,
        "totalFinalCarteira": total_final_carteira,
        "aportes": aportes
    }


if __name__ == "__main__":
    dados_carteira = carregar_dados_json()

    resultado = calcular_aporte(
        dados_carteira["classesAtivos"],
        dados_carteira["aporteMensalTotal"]
    )

    print("=" * 50)
    print(" ANÁLISE DE APORTE MENSAL")
    print("=" * 50)
    
    # Mostrar carteira ANTES do aporte
    print("\nCARTEIRA ANTES DO APORTE:\n")
    for aporte in resultado["aportes"]:
        percentual_atual = (aporte["valorAtual"] / resultado["totalAtualCarteira"] * 100) if resultado["totalAtualCarteira"] > 0 else 0
        print(f"   {aporte['nome']}: R$ {aporte['valorAtual']:.2f} ({percentual_atual:.1f}%)")
    print(f"\nPATRIMÔNIO TOTAL: R$ {resultado['totalAtualCarteira']:.2f}\n")
    
    # Mostrar recomendação de aportes
    print("-" * 50)
    print("\n🎯 RECOMENDAÇÃO DE APORTE:\n")
    total_aporte = sum(aporte["aporte"] for aporte in resultado["aportes"])
    for aporte in resultado["aportes"]:
        if aporte["aporte"] > 0:
            print(f"   ➡️  {aporte['nome']}: R$ {aporte['aporte']:.2f}")
        else:
            print(f"   ⚪  {aporte['nome']}: R$ 0.00 (não necessário)")
    print(f"\nTOTAL APORTADO: R$ {total_aporte:.2f}\n")

    
    # Mostrar carteira DEPOIS do aporte
    print("-" * 50)
    print("\nCARTEIRA DEPOIS DO APORTE:\n")
    for aporte in resultado["aportes"]:
        percentual_novo = (aporte["novoValor"] / resultado["totalFinalCarteira"] * 100)
        meta = aporte["metaPercentual"]
        status = "✅" if abs(percentual_novo - meta) < 1 else "⚠️"
        print(f"   {aporte['nome']}: R$ {aporte['novoValor']:.2f} ({percentual_novo:.1f}% | Meta: {meta:.1f}%) {status}")
    print(f"\nNOVO PATRIMÔNIO TOTAL: R$ {resultado['totalFinalCarteira']:.2f}")
    
    print("=" * 50)

    # Atualizar dados para salvar
    for i, aporte in enumerate(resultado["aportes"]):
        dados_carteira["classesAtivos"][i]["valorAtual"] = aporte["novoValor"]
    
    salvar_dados_json(dados_carteira)