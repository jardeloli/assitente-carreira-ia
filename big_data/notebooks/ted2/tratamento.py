import pandas as pd


#carregamento dos arquivos
cbo_grande_grupo = pd.read_csv(
    "../data/raw/cbo2002-grande-grupo.csv",
    sep=";",
    encoding="cp1252"
)

cbo_subgrupo_principal = pd.read_csv(
    "../data/raw/cbo2002-subgrupo-principal.csv",
    sep=";",
    encoding="cp1252"
)

cbo_subgrupo = pd.read_csv(
    "../data/raw/cbo2002-subgrupo.csv",
    sep=";",
    encoding="cp1252"
)

cbo_familia = pd.read_csv(
    "../data/raw/cbo2002-familia.csv",
    sep=";",
    encoding="cp1252"
)

cbo_ocupacao = pd.read_csv(
    "../data/raw/cbo2002-ocupacao.csv",
    sep=";",
    encoding="cp1252"
)

cbo_sinonimo = pd.read_csv(
    "../data/raw/cbo2002-sinonimo.csv",
    sep=";",
    encoding="cp1252"
)

cbo_perfil = pd.read_csv(
    "../data/raw/cbo2002-perfilocupacional.csv",
    sep=";",
    encoding="cp1252"
)



#organização das bases da cbo

bases_cbo = {
    "CBO Grande Grupo": cbo_grande_grupo,
    "CBO Subgrupo Principal": cbo_subgrupo_principal,
    "CBO Subgrupo": cbo_subgrupo,
    "CBO Família": cbo_familia,
    "CBO Ocupação": cbo_ocupacao,
    "CBO Sinônimo": cbo_sinonimo,
    "CBO Perfil Ocupacional": cbo_perfil
}

#limpeza e padronização 

for nome, df in bases_cbo.items():

    df.columns = df.columns.str.strip()

    colunas_texto = df.select_dtypes(
        include="object"
    ).columns

    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )



#inspeção das bases cbo

print("\n")
print("=" * 70)
print("INSPEÇÃO DAS BASES CBO")
print("=" * 70)

for nome, df in bases_cbo.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    print("Quantidade de registros:", len(df))
    print("Quantidade de colunas:", len(df.columns))

    print("\nColunas:")
    print(df.columns.tolist())

    print("\nTipos de dados:")
    print(df.dtypes)


#valores ausentes

print("\n")
print("=" * 70)
print("VALORES AUSENTES - CBO")
print("=" * 70)

for nome, df in bases_cbo.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    valores_ausentes = df.isnull().sum()

    print(
        valores_ausentes[
            valores_ausentes > 0
        ]
    )



#Duplicidade cbo

print("\n")
print("=" * 70)
print("DUPLICIDADES - CBO")
print("=" * 70)

for nome, df in bases_cbo.items():

    duplicados = df.duplicated().sum()

    print(
        nome,
        "->",
        duplicados,
        "registros duplicados"
    )



#estatísticas descritiva cbo

print("\n")
print("=" * 70)
print("ESTATÍSTICAS DESCRITIVAS - CBO")
print("=" * 70)

for nome, df in bases_cbo.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    print(
        df.describe(
            include="all"
        )
    )


#análise ocupações por grande grupo

print("\n")
print("=" * 70)
print("CBO - OCUPAÇÕES POR GRANDE GRUPO")
print("=" * 70)

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

print(ocupacoes_grande_grupo)


#análise cbo sinônimos por ocupações

print("\n")
print("=" * 70)
print("CBO - SINÔNIMOS POR OCUPAÇÃO")
print("=" * 70)

sinonimos_por_ocupacao = (
    cbo_sinonimo
    .groupby("CODIGO")
    .size()
)

print(
    sinonimos_por_ocupacao.describe()
)

print("\nMédia:")
print(
    sinonimos_por_ocupacao.mean()
)

print("\nMediana:")
print(
    sinonimos_por_ocupacao.median()
)

print("\nMínimo:")
print(
    sinonimos_por_ocupacao.min()
)

print("\nMáximo:")
print(
    sinonimos_por_ocupacao.max()
)


#análise cbo atividades por ocupações

print("\n")
print("=" * 70)
print("CBO - ATIVIDADES POR OCUPAÇÃO")
print("=" * 70)

atividades_por_ocupacao = (
    cbo_perfil
    .groupby("COD_OCUPACAO")
    .size()
)

print(
    atividades_por_ocupacao.describe()
)

print("\nMédia:")
print(
    atividades_por_ocupacao.mean()
)

print("\nMediana:")
print(
    atividades_por_ocupacao.median()
)

print("\nMínimo:")
print(
    atividades_por_ocupacao.min()
)

print("\nMáximo:")
print(
    atividades_por_ocupacao.max()
)


#carregamento arquivos esco 

esco_occupations = pd.read_csv(
    "../data/raw/occupations_pt.csv",
    sep=",",
    encoding="utf-8-sig"
)

esco_skills = pd.read_csv(
    "../data/raw/skills_pt.csv",
    sep=",",
    encoding="utf-8-sig"
)

esco_relacoes = pd.read_csv(
    "../data/raw/occupationSkillRelations_pt.csv",
    sep=",",
    encoding="utf-8-sig"
)



#organização das base esco

bases_esco = {
    "ESCO Ocupações": esco_occupations,
    "ESCO Competências": esco_skills,
    "ESCO Relações": esco_relacoes
}


#limpeza e padronização das bases esco

for nome, df in bases_esco.items():

   
    df.columns = df.columns.str.strip()

    
    df.dropna(
        axis=1,
        how="all",
        inplace=True
    )

    
    colunas_texto = df.select_dtypes(
        include="object"
    ).columns

   
    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )



# inspeção das bases esco

print("\n")
print("=" * 70)
print("INSPEÇÃO DAS BASES ESCO")
print("=" * 70)

for nome, df in bases_esco.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    print("Quantidade de registros:", len(df))
    print("Quantidade de colunas:", len(df.columns))

    print("\nColunas:")
    print(df.columns.tolist())

    print("\nTipos de dados:")
    print(df.dtypes)


#valores ausentes esco

print("\n")
print("=" * 70)
print("VALORES AUSENTES - ESCO")
print("=" * 70)

for nome, df in bases_esco.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    valores_ausentes = df.isnull().sum()

    print(
        valores_ausentes[
            valores_ausentes > 0
        ]
    )



#duplicidades esco=========

print("\n")
print("=" * 70)
print("DUPLICIDADES - ESCO")
print("=" * 70)

for nome, df in bases_esco.items():

    duplicados = df.duplicated().sum()

    print(
        nome,
        "->",
        duplicados,
        "registros duplicados"
    )



# estatística descritiva esco

print("\n")
print("=" * 70)
print("ESTATÍSTICAS DESCRITIVAS - ESCO")
print("=" * 70)

for nome, df in bases_esco.items():

    print("\n" + "-" * 70)
    print(nome)
    print("-" * 70)

    print(
        df.describe(
            include="all"
        )
    )



#análise esco relações por ocupação

print("\n")
print("=" * 70)
print("ESCO - RELAÇÕES POR OCUPAÇÃO")
print("=" * 70)

relacoes_por_ocupacao = (
    esco_relacoes
    .groupby("occupationUri")
    .size()
)

print(
    relacoes_por_ocupacao.describe()
)

print("\nMédia:")
print(
    relacoes_por_ocupacao.mean()
)

print("\nMediana:")
print(
    relacoes_por_ocupacao.median()
)

print("\nMínimo:")
print(
    relacoes_por_ocupacao.min()
)

print("\nMáximo:")
print(
    relacoes_por_ocupacao.max()
)


#análise esco relações essencial e opcional

print("\n")
print("=" * 70)
print("ESCO - RELAÇÕES POR CLASSIFICAÇÃO")
print("=" * 70)

relacoes_tipo = (
    esco_relacoes["relationType"]
    .value_counts()
)

print(relacoes_tipo)

print("\nPercentual:")

percentual_tipo = (
    esco_relacoes["relationType"]
    .value_counts(
        normalize=True
    )
    * 100
)

print(percentual_tipo)


#análise esco tipo de competência/conhecimento

print("\n")
print("=" * 70)
print("ESCO - TIPO DE COMPETÊNCIA/CONHECIMENTO")
print("=" * 70)

esco_relacoes["skillType"] = (
    esco_relacoes["skillType"]
    .fillna("Sem classificação")
)

tipos_competencia = (
    esco_relacoes["skillType"]
    .value_counts()
)

print(tipos_competencia)

print("\nTotal de relações:")
print(
    tipos_competencia.sum()
)


#análise esco top 10 competências/conhecimentos 

print("\n")
print("=" * 70)
print("ESCO - TOP 10 COMPETÊNCIAS/CONHECIMENTOS")
print("=" * 70)

top10_competencias = (
    esco_relacoes["skillLabel"]
    .value_counts()
    .head(10)
)

print(top10_competencias)


# resumo de qualidade das 10 bases 

print("\n")
print("=" * 70)
print("RESUMO DE QUALIDADE DAS BASES")
print("=" * 70)

todas_as_bases = {
    "CBO Grande Grupo": cbo_grande_grupo,
    "CBO Subgrupo Principal": cbo_subgrupo_principal,
    "CBO Subgrupo": cbo_subgrupo,
    "CBO Família": cbo_familia,
    "CBO Ocupação": cbo_ocupacao,
    "CBO Sinônimo": cbo_sinonimo,
    "CBO Perfil Ocupacional": cbo_perfil,
    "ESCO Ocupações": esco_occupations,
    "ESCO Competências": esco_skills,
    "ESCO Relações": esco_relacoes
}

resumo = []

for nome, df in todas_as_bases.items():

    resumo.append({
        "Base": nome,
        "Registros": len(df),
        "Colunas": len(df.columns),
        "Duplicados": df.duplicated().sum(),
        "Valores ausentes": df.isnull().sum().sum()
    })

resumo = pd.DataFrame(resumo)

print(resumo)


#salvar bases tratadas

cbo_grande_grupo.to_csv(
    "../data/processed/CBO_grande_grupo_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_subgrupo_principal.to_csv(
    "../data/processed/CBO_subgrupo_principal_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_subgrupo.to_csv(
    "../data/processed/CBO_subgrupo_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_familia.to_csv(
    "../data/processed/CBO_familia_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_ocupacao.to_csv(
    "../data/processed/CBO_ocupacao_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_sinonimo.to_csv(
    "../data/processed/CBO_sinonimo_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

cbo_perfil.to_csv(
    "../data/processed/CBO_perfil_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

esco_occupations.to_csv(
    "../data/processed/ESCO_occupations_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

esco_skills.to_csv(
    "../data/processed/ESCO_skills_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

esco_relacoes.to_csv(
    "../data/processed/ESCO_relations_processed.csv",
    index=False,
    encoding="utf-8-sig"
)


print("TRATAMENTO E ANÁLISE CONCLUÍDOS")