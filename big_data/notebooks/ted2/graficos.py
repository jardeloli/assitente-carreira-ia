import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



# Localização deste arquivo: notebooks/graficos.py
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Pasta onde estão as bases processadas
PASTA_DADOS = PASTA_PROJETO / "data" / "processed"

# Pasta onde os gráficos serão salvos
PASTA_GRAFICOS = PASTA_DADOS / "graficos"

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True
)


# Leituras das bases 
print("=" * 70)
print("CARREGAMENTO DAS BASES")
print("=" * 70)


cbo_ocupacao = pd.read_csv(
    PASTA_DADOS / "CBO_ocupacao_processed.csv",
    encoding="utf-8-sig"
)

cbo_sinonimo = pd.read_csv(
    PASTA_DADOS / "CBO_sinonimo_processed.csv",
    encoding="utf-8-sig"
)

cbo_perfil = pd.read_csv(
    PASTA_DADOS / "CBO_perfil_processed.csv",
    encoding="utf-8-sig"
)

esco_occupations = pd.read_csv(
    PASTA_DADOS / "ESCO_occupations_processed.csv",
    encoding="utf-8-sig"
)

esco_skills = pd.read_csv(
    PASTA_DADOS / "ESCO_skills_processed.csv",
    encoding="utf-8-sig"
)

esco_relations = pd.read_csv(
    PASTA_DADOS / "ESCO_relations_processed_traduzido.csv",
    encoding="utf-8-sig"
)


print("Bases carregadas com sucesso.")


# Função auxiliar para salvar o gráfico

def salvar_grafico(nome_arquivo):
    caminho = PASTA_GRAFICOS / nome_arquivo

    plt.tight_layout()

    plt.savefig(
        caminho,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Gráfico salvo: {caminho}")

    plt.close()


print("\n")
print("=" * 70)
print("GRÁFICO 1 - CBO: OCUPAÇÕES POR GRANDE GRUPO")
print("=" * 70)


# Extrai o primeiro dígito do código da ocupação
cbo_ocupacao["GRANDE_GRUPO"] = (
    cbo_ocupacao["CODIGO"]
    .astype(str)
    .str.strip()
    .str[0]
)


ocupacoes_grande_grupo = (
    cbo_ocupacao["GRANDE_GRUPO"]
    .value_counts()
    .sort_index()
)


plt.figure(figsize=(10, 6))

plt.bar(
    ocupacoes_grande_grupo.index,
    ocupacoes_grande_grupo.values
)

plt.title(
    "Figura 1 – Ocupações CBO por Grande Grupo"
)

plt.xlabel(
    "Grande Grupo"
)

plt.ylabel(
    "Quantidade de ocupações"
)

plt.grid(
    axis="y",
    alpha=0.3
)

salvar_grafico(
    "01_cbo_ocupacoes_por_grande_grupo.png"
)


print("\n")
print("=" * 70)
print("GRÁFICO 2 - CBO: SINÔNIMOS POR OCUPAÇÃO")
print("=" * 70)


sinonimos_por_ocupacao = (
    cbo_sinonimo
    .groupby("CODIGO")
    .size()
)


plt.figure(figsize=(10, 6))

plt.hist(
    sinonimos_por_ocupacao,
    bins=20
)

plt.title(
    "Figura 2 – Distribuição de Sinônimos por Ocupação"
)

plt.xlabel(
    "Quantidade de sinônimos por ocupação"
)

plt.ylabel(
    "Quantidade de ocupações"
)

plt.grid(
    axis="y",
    alpha=0.3
)

salvar_grafico(
    "02_cbo_distribuicao_sinonimos.png"
)



print("\n")
print("=" * 70)
print("GRÁFICO 3 - CBO: ATIVIDADES POR OCUPAÇÃO")
print("=" * 70)


atividades_por_ocupacao = (
    cbo_perfil
    .groupby("COD_OCUPACAO")
    .size()
)


plt.figure(figsize=(10, 6))

plt.hist(
    atividades_por_ocupacao,
    bins=20
)

plt.title(
    "Figura 3 – Distribuição de Atividades por Ocupação"
)

plt.xlabel(
    "Quantidade de atividades por ocupação"
)

plt.ylabel(
    "Quantidade de ocupações"
)

plt.grid(
    axis="y",
    alpha=0.3
)

salvar_grafico(
    "03_cbo_distribuicao_atividades.png"
)


print("\n")
print("=" * 70)
print("GRÁFICO 4 - ESCO: RELAÇÕES POR OCUPAÇÃO")
print("=" * 70)


relacoes_por_ocupacao = (
    esco_relations
    .groupby("occupationUri")
    .size()
)


plt.figure(figsize=(10, 6))

plt.hist(
    relacoes_por_ocupacao,
    bins=20
)

plt.title(
    "Figura 4 – Distribuição de Relações ESCO por Ocupação"
)

plt.xlabel(
    "Quantidade de relações por ocupação"
)

plt.ylabel(
    "Quantidade de ocupações"
)

plt.grid(
    axis="y",
    alpha=0.3
)

salvar_grafico(
    "04_esco_relacoes_por_ocupacao.png"
)


print("\n")
print("=" * 70)
print("GRÁFICO 5 - ESCO: RELAÇÕES POR CLASSIFICAÇÃO")
print("=" * 70)


relacoes_tipo = (
    esco_relations["relationType"]
    .value_counts()
)


# Garantir a ordem desejada
ordem_relacoes = [
    "essencial",
    "opcional"
]

relacoes_tipo = (
    relacoes_tipo
    .reindex(ordem_relacoes)
    .fillna(0)
)


plt.figure(figsize=(9, 6))

barras = plt.bar(
    relacoes_tipo.index,
    relacoes_tipo.values
)

plt.title(
    "Figura 5 – Relações ESCO por classificação"
)

plt.xlabel(
    "Classificação da relação"
)

plt.ylabel(
    "Quantidade de relações (registros)"
)

plt.grid(
    axis="y",
    alpha=0.3
)


# Mostrar o valor exato sobre cada barra
for barra in barras:

    altura = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f"{int(altura):,}".replace(",", "."),
        ha="center",
        va="bottom"
    )


salvar_grafico(
    "05_esco_essential_optional.png"
)



print("\n")
print("=" * 70)
print("GRÁFICO 6 - ESCO: TIPO DE COMPETÊNCIA/CONHECIMENTO")
print("=" * 70)


skill_type = (
    esco_relations["skillType"]
    .fillna("Sem classificação")
    .value_counts()
)


# Ordem desejada
ordem_skill_type = [
    "competência",
    "conhecimento",
    "Sem classificação"
]

skill_type = (
    skill_type
    .reindex(ordem_skill_type)
    .fillna(0)
)


plt.figure(figsize=(10, 6))

barras = plt.bar(
    skill_type.index,
    skill_type.values
)

plt.title(
    "Figura 6 – Relações ESCO por tipo de competência/conhecimento"
)

plt.xlabel(
    "Tipo"
)

plt.ylabel(
    "Quantidade de relações (registros)"
)

plt.grid(
    axis="y",
    alpha=0.3
)


for barra in barras:

    altura = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f"{int(altura):,}".replace(",", "."),
        ha="center",
        va="bottom"
    )


salvar_grafico(
    "06_esco_skill_type.png"
)



print("\n")
print("=" * 70)
print("GRÁFICO 7 - ESCO: PRINCIPAIS COMPETÊNCIAS/CONHECIMENTOS")
print("=" * 70)


top_skills = (
    esco_relations["skillLabel"]
    .value_counts()
    .head(10)
    .sort_values()
)


plt.figure(figsize=(11, 7))

plt.barh(
    top_skills.index,
    top_skills.values
)

plt.title(
    "Figura 7 – Principais competências e conhecimentos relacionados às ocupações"
)

plt.xlabel(
    "Quantidade de relações"
)

plt.ylabel(
    "Competência ou conhecimento"
)

plt.grid(
    axis="x",
    alpha=0.3
)


salvar_grafico(
    "07_esco_top_skills.png"
)



print("\n")
print("=" * 70)
print("GERAÇÃO DOS GRÁFICOS CONCLUÍDA")
print("=" * 70)

print("\nOs 7 gráficos foram salvos em:")

print(
    PASTA_GRAFICOS
)