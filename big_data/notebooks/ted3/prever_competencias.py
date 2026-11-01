from pathlib import Path
import joblib
import numpy as np



PASTA_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_MODELO = (
    PASTA_PROJETO
    / "data"
    / "modeling"
    / "modelo_competencias_esco.joblib"
)


# Carrega o modelo treinado
pacote = joblib.load(CAMINHO_MODELO)

vetorizador = pacote["vetorizador"]
modelo = pacote["modelo"]
nomes_competencias = pacote["nomes_competencias"]


def prever_competencias(titulo, descricao, quantidade=10):
    texto = f"{titulo} {descricao}".strip()

    # Transforma o texto no formato utilizado pelo modelo
    texto_vetorizado = vetorizador.transform([texto])

    # Calcula as probabilidades estimadas para cada competência
    probabilidades = modelo.predict_proba(texto_vetorizado)[0]

    # Obtém os índices das competências com maiores pontuações
    melhores_indices = np.argsort(probabilidades)[::-1][:quantidade]

    print("\nCompetências previstas:\n")

    for indice in melhores_indices:
        competencia_uri = pacote["rotulos"][indice]

        nome = nomes_competencias.get(
            competencia_uri,
            competencia_uri
        )

        pontuacao = probabilidades[indice] * 100

        print(f"- {nome}: {pontuacao:.2f}%")


if __name__ == "__main__":
    print("=== Previsão de competências profissionais ===")

    titulo = input("\nDigite o nome da profissão: ")
    descricao = input("Digite a descrição da profissão: ")

    prever_competencias(titulo, descricao)
