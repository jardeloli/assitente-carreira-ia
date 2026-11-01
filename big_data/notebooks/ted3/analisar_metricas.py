from pathlib import Path
import pandas as pd


PASTA_PROJETO = Path(__file__).resolve().parents[2]

ARQUIVO_METRICAS = (
    PASTA_PROJETO
    / "data"
    / "modeling"
    / "metricas_por_competencia.csv"
)


def analisar_metricas():
    metricas = pd.read_csv(ARQUIVO_METRICAS)

    print("\n=== RESUMO DAS MÉTRICAS ===")

    print(
        metricas[["precisao", "revocacao", "f1", "suporte_teste"]]
        .describe()
        .round(4)
    )

    # Correlação entre suporte e F1
    correlacao_pearson = metricas["suporte_teste"].corr(
        metricas["f1"],
        method="pearson"
    )

    correlacao_spearman = metricas["suporte_teste"].corr(
        metricas["f1"],
        method="spearman"
    )

    print("\n=== CORRELAÇÃO ENTRE SUPORTE E F1 ===")

    print(f"Pearson: {correlacao_pearson:.4f}")
    print(f"Spearman: {correlacao_spearman:.4f}")

    # Agrupa competências por quantidade de exemplos no teste
    metricas["grupo_suporte"] = pd.cut(
        metricas["suporte_teste"],
        bins=[0, 10, 20, 30, float("inf")],
        labels=[
            "Até 10 exemplos",
            "11 a 20 exemplos",
            "21 a 30 exemplos",
            "Mais de 30 exemplos",
        ],
    )

    resumo = (
        metricas
        .groupby("grupo_suporte", observed=False)
        .agg(
            quantidade_competencias=("competencia", "count"),
            suporte_medio=("suporte_teste", "mean"),
            f1_medio=("f1", "mean"),
            precisao_media=("precisao", "mean"),
            revocacao_media=("revocacao", "mean"),
        )
        .round(4)
    )

    print("\n=== DESEMPENHO POR GRUPO DE SUPORTE ===")
    print(resumo)

    resumo.to_csv(
        PASTA_PROJETO
        / "data"
        / "modeling"
        / "analise_suporte.csv",
        encoding="utf-8-sig",
    )


if __name__ == "__main__":
    analisar_metricas()