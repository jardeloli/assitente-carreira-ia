from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_RESULTADOS = PASTA_PROJETO / "data" / "modeling"
PASTA_GRAFICOS = PASTA_RESULTADOS / "graficos"

ARQUIVO_COMPARACAO = PASTA_RESULTADOS / "comparacao_modelos.csv"
ARQUIVO_METRICAS = PASTA_RESULTADOS / "metricas_por_competencia.csv"



def carregar_csv(caminho: Path) -> pd.DataFrame:
    """Carrega um CSV e verifica se o arquivo existe."""

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}\n"
            "Execute primeiro o script modelagem.py."
        )

    return pd.read_csv(caminho)


def converter_para_percentual(serie: pd.Series) -> pd.Series:
    """Converte métricas entre 0 e 1 para percentual."""

    serie = pd.to_numeric(serie, errors="coerce")

    if serie.max() <= 1:
        return serie * 100

    return serie


def salvar_grafico(nome: str) -> None:
    """Salva o gráfico na pasta de resultados."""

    caminho = PASTA_GRAFICOS / nome

    plt.savefig(
        caminho,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Gráfico salvo: {caminho}")



# GRÁFICO COMPARAÇÃO DAS MÉTRICAS

def gerar_comparacao_metricas() -> None:

    dados = carregar_csv(ARQUIVO_COMPARACAO)

    colunas = [
        "quantidade_rotulos",
        "f1_micro",
        "f1_macro",
        "f1_samples"
    ]

    for coluna in colunas:
        if coluna not in dados.columns:
            raise ValueError(
                f"Coluna '{coluna}' não encontrada em "
                "comparacao_modelos.csv."
            )

    dados = dados.sort_values("quantidade_rotulos")

    metricas = ["f1_micro", "f1_macro", "f1_samples"]

    for metrica in metricas:
        dados[metrica] = converter_para_percentual(dados[metrica])

    ax = dados.set_index("quantidade_rotulos")[metricas].plot(
        kind="bar",
        figsize=(10, 6),
        width=0.8
    )

    ax.set_title("Comparação das métricas F1 por experimento")
    ax.set_xlabel("Quantidade de competências")
    ax.set_ylabel("Resultado (%)")
    ax.set_ylim(0, 100)

    ax.set_xticklabels(
        [str(int(valor)) for valor in dados["quantidade_rotulos"]],
        rotation=0
    )

    ax.legend(
        ["F1 Micro", "F1 Macro", "F1 Samples"],
        title="Métricas"
    )

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    salvar_grafico("comparacao_metricas.png")



# GRÁFICO DISTRIBUIÇÃO DO F1 POR COMPETÊNCIA

def gerar_distribuicao_f1() -> None:

    dados = carregar_csv(ARQUIVO_METRICAS)

    if "f1" not in dados.columns:
        raise ValueError(
            "Coluna 'f1' não encontrada em "
            "metricas_por_competencia.csv."
        )

    f1 = converter_para_percentual(dados["f1"]).dropna()

    faixas = [
        0, 40, 50, 60, 70, 80, 90, 100.000001
    ]

    nomes_faixas = [
        "0–40%",
        "40–50%",
        "50–60%",
        "60–70%",
        "70–80%",
        "80–90%",
        "90–100%"
    ]

    distribuicao = pd.cut(
        f1,
        bins=faixas,
        labels=nomes_faixas,
        include_lowest=True
    )

    contagem = (
        distribuicao
        .value_counts(sort=False)
    )

    ax = contagem.plot(
        kind="bar",
        figsize=(10, 6),
        width=0.75
    )

    ax.set_title("Distribuição do F1 por competência")
    ax.set_xlabel("Faixa de desempenho")
    ax.set_ylabel("Quantidade de competências")

    ax.tick_params(axis="x", rotation=0)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Exibe a quantidade acima de cada barra.
    for barra in ax.patches:
        altura = barra.get_height()

        ax.annotate(
            str(int(altura)),
            (barra.get_x() + barra.get_width() / 2, altura),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    salvar_grafico("distribuicao_f1.png")



# GRÁFICO PRECISÃO E REVOCAÇÃO

def gerar_precisao_revocacao() -> None:

    dados = carregar_csv(ARQUIVO_COMPARACAO)

    colunas = [
        "quantidade_rotulos",
        "precisao_micro",
        "revocacao_micro"
    ]

    for coluna in colunas:
        if coluna not in dados.columns:
            raise ValueError(
                f"Coluna '{coluna}' não encontrada em "
                "comparacao_modelos.csv."
            )

    dados = dados.sort_values("quantidade_rotulos")

    dados["precisao_micro"] = converter_para_percentual(
        dados["precisao_micro"]
    )

    dados["revocacao_micro"] = converter_para_percentual(
        dados["revocacao_micro"]
    )

    ax = dados.set_index("quantidade_rotulos")[
        ["precisao_micro", "revocacao_micro"]
    ].plot(
        kind="bar",
        figsize=(10, 6),
        width=0.75
    )

    ax.set_title("Comparação entre Precisão e Revocação")
    ax.set_xlabel("Quantidade de competências")
    ax.set_ylabel("Resultado (%)")
    ax.set_ylim(0, 100)

    ax.set_xticklabels(
        [str(int(valor)) for valor in dados["quantidade_rotulos"]],
        rotation=0
    )

    ax.legend(
        ["Precisão (Precision)", "Revocação (Recall)"]
    )

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    salvar_grafico("precisao_revocacao.png")


def main():

    PASTA_GRAFICOS.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\nGerando gráficos dos experimentos...\n")

    gerar_comparacao_metricas()
    gerar_distribuicao_f1()
    gerar_precisao_revocacao()

    print("\nTodos os gráficos foram gerados com sucesso!")


if __name__ == "__main__":
    main()
