from collections import Counter
from pathlib import Path
import json
import warnings

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer



# 1. CONFIGURAÇÕES E CAMINHOS

PASTA_PROJETO = Path(__file__).resolve().parents[2]


PASTA_DADOS = PASTA_PROJETO / "data" / "processed"


PASTA_RESULTADOS = PASTA_PROJETO / "data" / "modeling"

ARQUIVO_OCUPACOES = PASTA_DADOS / "ESCO_occupations_processed.csv"
ARQUIVO_RELACOES = PASTA_DADOS / "ESCO_relations_processed.csv"

PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

SEED = 42
TEST_SIZE = 0.20
QUANTIDADES_ROTULOS = [30, 50, 100]


# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS

def carregar_dados():
    """Carrega as ocupações e relações da ESCO."""
    if not ARQUIVO_OCUPACOES.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_OCUPACOES}")

    if not ARQUIVO_RELACOES.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_RELACOES}")

    ocupacoes = pd.read_csv(ARQUIVO_OCUPACOES, encoding="utf-8-sig")
    relacoes = pd.read_csv(ARQUIVO_RELACOES, encoding="utf-8-sig")

    return ocupacoes, relacoes


def preparar_dataset(ocupacoes, relacoes):
    """
    Monta uma linha por ocupação e associa a lista de competências essenciais.

    A escolha de competências essenciais é uma decisão de escopo do primeiro
    experimento. Relações opcionais e conhecimentos ficam fora desta versão.
    """

    # Mantém somente relações essenciais do tipo competência.
    relacoes_alvo = relacoes[
        (relacoes["relationType"].str.lower() == "essencial")
        & (relacoes["skillType"].str.lower() == "competência")
    ].copy()

    # Uma ocupação pode ter várias competências; cada URI é um rótulo.
    competencias_por_ocupacao = (
        relacoes_alvo.groupby("occupationUri")["skillUri"]
        .apply(lambda valores: sorted(set(valores)))
        .to_dict()
    )

    # Remove duplicações de ocupação pela URI, preservando a primeira ocorrência.
    ocupacoes = ocupacoes.drop_duplicates(
        subset="conceptUri",
        keep="first"
    ).copy()

    # Normaliza os campos textuais utilizados como entrada.
    for coluna in ["preferredLabel", "altLabels", "description"]:
        ocupacoes[coluna] = ocupacoes[coluna].fillna("").astype(str)

    ocupacoes["texto_entrada"] = (
        ocupacoes["preferredLabel"]
        + " "
        + ocupacoes["altLabels"].str.replace("\n", " ", regex=False)
        + " "
        + ocupacoes["description"]
    )

    ocupacoes["texto_entrada"] = (
        ocupacoes["texto_entrada"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    ocupacoes["competencias"] = ocupacoes["conceptUri"].map(
        competencias_por_ocupacao
    )

    # Exclui ocupações sem competência essencial associada.
    dataset = ocupacoes.dropna(subset=["competencias"]).copy()
    dataset = dataset[dataset["texto_entrada"].ne("")].copy()

    # Evita linhas com lista vazia de rótulos.
    dataset = dataset[
        dataset["competencias"].apply(lambda lista: len(lista) > 0)
    ].copy()

    dataset = dataset.reset_index(drop=True)

    return dataset, relacoes_alvo



# 3. DIVISÃO ENTRE TREINO E TESTE

def separar_treino_teste(dataset):
    """Separa ocupações sem colocar a mesma ocupação nos dois conjuntos."""
    indices = list(range(len(dataset)))

    indices_treino, indices_teste = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=SEED,
        shuffle=True,
    )

    treino = dataset.iloc[indices_treino].reset_index(drop=True)
    teste = dataset.iloc[indices_teste].reset_index(drop=True)

    return treino, teste


def diagnosticar_divisao(treino, teste):
    """Verifica a distribuição das competências entre treino e teste."""

    frequencias_treino = Counter(
        competencia
        for lista in treino["competencias"]
        for competencia in lista
    )

    frequencias_teste = Counter(
        competencia
        for lista in teste["competencias"]
        for competencia in lista
    )

    rotulos = selecionar_rotulos_frequentes(treino, 100)

    diagnostico = pd.DataFrame([
        {
            "competencia": rotulo,
            "frequencia_treino": frequencias_treino[rotulo],
            "frequencia_teste": frequencias_teste[rotulo],
        }
        for rotulo in rotulos
    ])

    sem_exemplos_teste = diagnostico[
        diagnostico["frequencia_teste"] == 0
    ]

    print("\n=== DIAGNÓSTICO DA DIVISÃO ===")

    print(
        "Competências selecionadas:",
        len(diagnostico)
    )

    print(
        "Competências sem exemplos no teste:",
        len(sem_exemplos_teste)
    )

    print(
        "Menor frequência no treinamento:",
        diagnostico["frequencia_treino"].min()
    )

    print(
        "Menor frequência no teste:",
        diagnostico["frequencia_teste"].min()
    )

    print("\nCompetências com menor frequência no teste:")

    print(
        diagnostico
        .sort_values("frequencia_teste")
        .head(15)
        .to_string(index=False)
    )

    diagnostico.to_csv(
        PASTA_RESULTADOS / "diagnostico_divisao.csv",
        index=False,
        encoding="utf-8-sig",
    )


# 4. MATRIZ MULTIRRÓTULO

def selecionar_rotulos_frequentes(treino, quantidade):
    """
    Seleciona os rótulos mais frequentes usando somente o conjunto de treino.

    Isso evita utilizar informações do conjunto de teste para definir
    quais competências o modelo aprenderá.
    """
    frequencias = Counter(
        competencia
        for lista in treino["competencias"]
        for competencia in lista
    )

    return [
        competencia
        for competencia, _ in frequencias.most_common(quantidade)
    ]


def transformar_rotulos(dataset, rotulos):
    """Converte as listas de competências em uma matriz binária."""
    conjunto_rotulos = set(rotulos)

    listas_filtradas = [
        [rotulo for rotulo in lista if rotulo in conjunto_rotulos]
        for lista in dataset["competencias"]
    ]

    binarizador = MultiLabelBinarizer(classes=rotulos)
    matriz = binarizador.fit_transform(listas_filtradas)

    return matriz



# 5. TREINAMENTO E AVALIAÇÃO

def criar_modelo():
    """Cria o classificador multirrótulo."""
    classificador_base = LogisticRegression(
        max_iter=1000,
        C=2.0,
        class_weight="balanced",
        solver="liblinear",
    )

    return OneVsRestClassifier(classificador_base)


def avaliar_modelo(y_real, y_previsto):
    """Calcula métricas globais de classificação multirrótulo."""
    return {
        "f1_micro": f1_score(
            y_real, y_previsto, average="micro", zero_division=0
        ),
        "f1_macro": f1_score(
            y_real, y_previsto, average="macro", zero_division=0
        ),
        "f1_samples": f1_score(
            y_real, y_previsto, average="samples", zero_division=0
        ),
        "precisao_micro": precision_score(
            y_real, y_previsto, average="micro", zero_division=0
        ),
        "revocacao_micro": recall_score(
            y_real, y_previsto, average="micro", zero_division=0
        ),
    }


def executar_experimento(treino, teste, quantidade_rotulos):
    """Treina e avalia um modelo para uma quantidade de rótulos."""
    rotulos = selecionar_rotulos_frequentes(treino, quantidade_rotulos)

    y_treino = transformar_rotulos(treino, rotulos)
    y_teste = transformar_rotulos(teste, rotulos)

    vetorizar = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_features=50000,
        sublinear_tf=True,
    )

    x_treino = vetorizar.fit_transform(treino["texto_entrada"])
    x_teste = vetorizar.transform(teste["texto_entrada"])

    modelo = criar_modelo()
    modelo.fit(x_treino, y_treino)

    previsoes = modelo.predict(x_teste)
    metricas = avaliar_modelo(y_teste, previsoes)

    metricas["quantidade_rotulos"] = quantidade_rotulos
    metricas["ocupacoes_treino"] = len(treino)
    metricas["ocupacoes_teste"] = len(teste)
    metricas["vocabulario"] = len(vetorizar.vocabulary_)

    return metricas, modelo, vetorizar, rotulos, y_teste, previsoes



# 6. EXECUÇÃO PRINCIPAL

def main():
    print("=" * 72)
    print("TED 03 - PREPARAÇÃO, TREINAMENTO E AVALIAÇÃO")
    print("=" * 72)

    ocupacoes, relacoes = carregar_dados()

    print("\n[1/5] Preparando os dados...")
    dataset, relacoes_alvo = preparar_dataset(ocupacoes, relacoes)

    print(f"Ocupações originais: {len(ocupacoes)}")
    print(f"Ocupações únicas por URI: {ocupacoes['conceptUri'].nunique()}")
    print(f"Relações essenciais de competência: {len(relacoes_alvo)}")
    print(f"Ocupações utilizadas no modelo: {len(dataset)}")

    treino, teste = separar_treino_teste(dataset)
    diagnosticar_divisao(treino, teste)

    print("\n[2/5] Divisão dos dados:")
    print(f"Treinamento: {len(treino)} ({len(treino) / len(dataset):.0%})")
    print(f"Teste: {len(teste)} ({len(teste) / len(dataset):.0%})")

    # Salva uma cópia tabular do conjunto preparado para inspeção.
    dataset_exportacao = dataset[
        ["conceptUri", "preferredLabel", "texto_entrada", "competencias"]
    ].copy()
    dataset_exportacao["competencias"] = dataset_exportacao[
        "competencias"
    ].apply(json.dumps)

    dataset_exportacao.to_csv(
        PASTA_RESULTADOS / "dataset_modelagem.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\n[3/5] Comparando modelos com 30, 50 e 100 competências...")
    resultados = []
    modelos = {}

    for quantidade in QUANTIDADES_ROTULOS:
        print(f"\nTreinando modelo com {quantidade} rótulos...")
        resultado = executar_experimento(treino, teste, quantidade)
        metricas, modelo, vetorizar, rotulos, y_teste, previsoes = resultado

        resultados.append(metricas)
        modelos[quantidade] = (
            modelo, vetorizar, rotulos, y_teste, previsoes
        )

        print(f"F1 Micro: {metricas['f1_micro']:.4f}")
        print(f"F1 Macro: {metricas['f1_macro']:.4f}")
        print(f"Precisão Micro: {metricas['precisao_micro']:.4f}")
        print(f"Revocação Micro: {metricas['revocacao_micro']:.4f}")

    comparacao = pd.DataFrame(resultados)
    comparacao.to_csv(
        PASTA_RESULTADOS / "comparacao_modelos.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # A primeira versão utiliza 100 rótulos, permitindo comparar o resultado
    # com os experimentos menores sem tentar cobrir toda a cauda longa da ESCO.
    quantidade_escolhida = 100
    modelo, vetorizar, rotulos, y_teste, previsoes = modelos[
        quantidade_escolhida
    ]

    print("\n[4/5] Salvando métricas detalhadas...")
    precisao, revocacao, f1, suporte = precision_recall_fscore_support(
        y_teste,
        previsoes,
        average=None,
        zero_division=0,
    )

    nomes_competencias = (
        relacoes_alvo[["skillUri", "skillLabel"]]
        .drop_duplicates("skillUri")
        .set_index("skillUri")["skillLabel"]
        .to_dict()
    )

    relatorio = pd.DataFrame({
        "skillUri": rotulos,
        "competencia": [
            nomes_competencias.get(uri, uri) for uri in rotulos
        ],
        "precisao": precisao,
        "revocacao": revocacao,
        "f1": f1,
        "suporte_teste": suporte,
    })

    relatorio.to_csv(
        PASTA_RESULTADOS / "metricas_por_competencia.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\n[5/5] Salvando modelo e configurações...")
    pacote_modelo = {
        "vetorizador": vetorizar,
        "modelo": modelo,
        "rotulos": rotulos,
        "nomes_competencias": nomes_competencias,
        "quantidade_rotulos": quantidade_escolhida,
        "seed": SEED,
    }

    joblib.dump(
        pacote_modelo,
        PASTA_RESULTADOS / "modelo_competencias_esco.joblib",
    )

    configuracao = {
        "fonte": "ESCO",
        "entrada": [
            "preferredLabel",
            "altLabels",
            "description",
        ],
        "alvo": "relationType=essencial e skillType=competência",
        "abordagem": "Classificação multirrótulo",
        "vetorizacao": "TF-IDF (unigramas e bigramas)",
        "algoritmo": "One-vs-Rest com Regressão Logística",
        "divisao_treino_teste": "80/20",
        "random_state": SEED,
        "rotulos_modelo_final": quantidade_escolhida,
    }

    with open(
        PASTA_RESULTADOS / "configuracao_experimento.json",
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(configuracao, arquivo, ensure_ascii=False, indent=4)

    print("\n" + "=" * 72)
    print("EXPERIMENTO CONCLUÍDO")
    print("=" * 72)
    print(comparacao.to_string(index=False))
    print(f"\nArquivos salvos em: {PASTA_RESULTADOS}")


if __name__ == "__main__":
    main()
