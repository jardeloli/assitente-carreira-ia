# TED 03 — Primeira versão da modelagem preditiva

## 1. Problema de aprendizado de máquina

O experimento busca prever competências profissionais essenciais associadas a uma ocupação da ESCO, utilizando como entrada o título preferencial, os títulos alternativos e a descrição da ocupação.

Trata-se de um problema de **classificação multirrótulo**, pois uma mesma ocupação pode estar associada a várias competências.

Esta etapa utiliza apenas a ESCO. A CBO permanece como referência brasileira para identificação e organização das ocupações, conforme a definição anterior do projeto. A integração CBO–ESCO não é realizada neste experimento.

## 2. Dados utilizados

Arquivos de entrada:

- `data/processed/ESCO_occupations_processed.csv`
- `data/processed/ESCO_relations_processed.csv`

A tabela de ocupações possui 3.043 linhas e 3.039 URIs únicas. Quatro linhas repetidas por URI são removidas na preparação.

A tabela de relações possui 126.051 registros. Para o primeiro experimento, foram selecionadas somente as relações em que:

- `relationType = essencial`
- `skillType = competência`

Esse filtro resultou em 51.155 relações. Após relacionar as competências às ocupações e remover duplicidades de ocupação, o conjunto utilizado contém 3.037 ocupações. Duas ocupações não possuem competência essencial do tipo selecionado e, por isso, não entram neste primeiro treinamento.

## 3. Variáveis

### Entradas (X)

O texto de cada ocupação é formado pela concatenação de:

- `preferredLabel`: título preferencial;
- `altLabels`: títulos alternativos;
- `description`: descrição da ocupação.

Os campos textuais são preenchidos quando ausentes e passam por normalização de espaços em branco.

### Alvos (y)

Os alvos são os identificadores `skillUri` das competências associadas a cada ocupação pelas relações essenciais do tipo competência.

Foi adotada uma seleção experimental das 100 competências mais frequentes no conjunto de treinamento. Essa restrição é necessária para controlar a grande quantidade de competências raras da base ESCO. O modelo inicial não prevê todas as competências existentes na classificação.

## 4. Preparação e divisão

- Remoção de quatro linhas duplicadas por `conceptUri` na tabela de ocupações;
- seleção de relações essenciais do tipo competência;
- agrupamento das competências por URI da ocupação;
- concatenação do título, títulos alternativos e descrição;
- exclusão de ocupações sem competência alvo;
- divisão aleatória de 80% para treinamento e 20% para teste;
- `random_state = 42`, para permitir a reprodução da divisão.

A seleção dos rótulos mais frequentes é realizada exclusivamente no conjunto de treinamento, evitando utilizar o conjunto de teste para definir as classes aprendidas.

Resultado da divisão:

- Treinamento: 2.429 ocupações;
- Teste: 608 ocupações.

## 5. Modelo

O primeiro modelo utiliza:

1. **TF-IDF**, com unigramas e bigramas, para transformar os textos em representações numéricas;
2. **Regressão Logística**, como classificador binário para cada competência;
3. **One-vs-Rest**, para adaptar os classificadores binários ao problema multirrótulo;
4. `class_weight="balanced"`, para lidar parcialmente com o desequilíbrio entre as classes.

Foram comparadas três configurações, com 30, 50 e 100 competências selecionadas a partir do treinamento.

## 6. Resultados do primeiro experimento

| Competências consideradas | F1 Micro | F1 Macro | Precisão Micro | Revocação Micro |
|---:|---:|---:|---:|---:|
| 30 | 0,6396 | 0,6272 | 0,6208 | 0,6595 |
| 50 | 0,6674 | 0,6660 | 0,6576 | 0,6774 |
| 100 | 0,6863 | 0,6927 | 0,6816 | 0,6910 |

A configuração com 100 competências apresentou os melhores valores entre as três configurações avaliadas nesta execução. Por esse motivo, ela foi mantida como versão inicial do experimento.

Na configuração de 100 competências, o F1 por amostra (`F1 Samples`) foi 0,3807.

## 7. Interpretação e limitações

Os resultados são uma avaliação inicial, realizada com uma única divisão aleatória entre treinamento e teste. Eles não devem ser interpretados como garantia de desempenho em currículos reais.

Limitações atuais:

- o conjunto de dados descreve relações entre ocupações e competências, não experiências individuais de candidatos;
- o modelo prevê somente as 100 competências selecionadas, e não todas as competências ESCO;
- competências raras ficam fora do escopo desta primeira versão;
- a ESCO é uma classificação europeia traduzida para português e pode não representar integralmente o mercado de trabalho brasileiro;
- ainda é necessário comparar o modelo com uma linha de base simples, investigar falsos positivos e falsos negativos e avaliar outras divisões ou validação cruzada;
- as competências previstas devem ser tratadas como sugestões relacionadas à ocupação, nunca como comprovação de que o candidato possui essas competências.

## 8. Como executar

Na pasta `big_data`, instale as dependências:

```bash
pip install -r requirements-ml.txt
```

Execute:

```bash
python notebooks/modelagem.py
```

O script utiliza caminhos relativos à localização do próprio arquivo e salva os resultados em `data/modeling/`:

- `dataset_modelagem.csv`
- `comparacao_modelos.csv`
- `metricas_por_competencia.csv`
- `configuracao_experimento.json`
- `modelo_competencias_esco.joblib`

O arquivo `.joblib` contém o vetorizador, o classificador e o mapeamento das competências selecionadas.
