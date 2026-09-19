# Sistema de Inteligência Artificial para Currículos e Entrevistas

## TED 01 – Definição do Problema de Dados e Seleção do Conjunto de Dados

### 👥 Integrantes da equipe

* Jardel Oliveira
* Gustavo Noleto
* Miqueias do Nascimento
* Wallaci Araujo

---

## 📌 Sobre o projeto

O projeto propõe o desenvolvimento de um **Sistema de Inteligência Artificial para Currículos e Entrevistas**, voltado para pessoas que estão em busca de emprego ou de novas oportunidades profissionais.

A proposta é utilizar Inteligência Artificial para auxiliar o candidato a transformar informações fornecidas de maneira informal sobre sua experiência, conhecimentos e habilidades em informações mais organizadas e adequadas para um currículo profissional.

Além da elaboração do currículo, o sistema também pretende auxiliar na criação de uma carta de apresentação e na preparação para entrevistas de emprego por meio de uma simulação de entrevista, na qual o candidato responde perguntas e recebe orientações sobre suas respostas.

O sistema tem como objetivo **auxiliar o candidato**, não substituir processos de recrutamento e seleção ou tomar decisões automatizadas de contratação.

---

## ❗ Problema

Muitas pessoas possuem experiências profissionais, conhecimentos e habilidades relevantes, mas encontram dificuldades para apresentar essas informações de maneira clara, organizada e profissional em um currículo.

Essa dificuldade pode ser ainda maior para pessoas que possuem pouca familiaridade com ferramentas digitais, modelos de currículo ou linguagem profissional.

Além da elaboração do currículo, candidatos também podem apresentar dificuldades na preparação para entrevistas, principalmente para organizar suas experiências e responder de maneira objetiva às perguntas relacionadas à vaga desejada.

Dessa forma, o projeto busca investigar como uma solução baseada em Inteligência Artificial pode auxiliar o candidato na **organização de suas experiências profissionais, elaboração de documentos e preparação para entrevistas**.

---

## 🎯 Objetivo do MVP

O MVP (Produto Mínimo Viável) consiste em um sistema capaz de:

* receber informações profissionais fornecidas pelo candidato;
* identificar e organizar experiências, conhecimentos e habilidades;
* considerar a ocupação desejada pelo candidato;
* auxiliar na elaboração de um currículo;
* auxiliar na elaboração de uma carta de apresentação;
* realizar uma simulação de entrevista;
* apresentar perguntas relacionadas à ocupação desejada;
* analisar as respostas fornecidas pelo candidato;
* fornecer feedback para auxiliar na preparação para a entrevista.

---

# 📊 Conjuntos de dados utilizados

Para atender às necessidades de dados do projeto, foram selecionadas duas fontes complementares:

1. **CBO – Classificação Brasileira de Ocupações**
2. **ESCO – European Skills, Competences, Qualifications and Occupations**

A utilização conjunta das duas fontes permite trabalhar com diferentes aspectos das informações profissionais.

A **CBO** será utilizada como principal referência para a identificação e organização das ocupações do mercado de trabalho brasileiro.

O **ESCO** será utilizado como fonte complementar, principalmente para informações relacionadas a **ocupações, conhecimentos, habilidades e competências profissionais**, além das relações existentes entre ocupações e habilidades.

---

# 🇧🇷 CBO – Classificação Brasileira de Ocupações

## Identificação da base

* **Nome:** Classificação Brasileira de Ocupações – CBO
* **Classificação:** CBO 2002
* **Órgão responsável:** Ministério do Trabalho e Emprego – MTE
* **País:** Brasil
* **Idioma:** Português
* **Formato utilizado:** CSV

A CBO é a classificação oficial utilizada para identificar e codificar as ocupações do mercado de trabalho brasileiro.

Para este projeto foram analisados os seguintes arquivos:

| Arquivo/estrutura  |   Registros |
| ------------------ | ----------: |
| Grande Grupo       |          10 |
| Subgrupo Principal |          49 |
| Subgrupo           |         195 |
| Família            |         626 |
| Ocupação           |       2.694 |
| Sinônimo           |       7.778 |
| Perfil Ocupacional |     174.296 |
| **Total**          | **185.648** |

O total corresponde à soma dos registros dos arquivos analisados e não representa a quantidade de ocupações distintas.

## Fonte original

**Ministério do Trabalho e Emprego – Governo Federal**

Página oficial para obtenção dos arquivos:

https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/servicos/downloads/downloads

## Como obter os dados da CBO

1. Acessar a página oficial de downloads da CBO.
2. Localizar a seção referente à **Estrutura CBO (CSV)**.
3. Baixar os arquivos disponibilizados pelo Ministério do Trabalho e Emprego.
4. Para reproduzir a análise deste projeto, utilizar os arquivos referentes a:

   * Grande Grupo;
   * Subgrupo Principal;
   * Subgrupo;
   * Família;
   * Ocupação;
   * Sinônimo;
   * Perfil Ocupacional.
5. Manter os arquivos em formato CSV para reprodução das etapas de tratamento e análise.

Os arquivos originais da CBO **não estão armazenados neste repositório**. O link oficial acima permite obter os dados diretamente da fonte responsável pela disponibilização da classificação.

---

# 🇪🇺 ESCO – European Skills, Competences, Qualifications and Occupations

## Identificação da base

* **Nome:** European Skills, Competences, Qualifications and Occupations – ESCO
* **Versão utilizada:** ESCO v1.2.1
* **Idioma utilizado:** Português (pt)
* **Formato:** CSV
* **Fonte:** Comissão Europeia – European Commission
* **Finalidade no projeto:** fonte complementar à CBO para informações sobre ocupações, conhecimentos, habilidades e competências.

O ESCO organiza informações relacionadas a ocupações, conhecimentos, habilidades e competências profissionais e permite estabelecer relações entre ocupações e habilidades.

## Arquivos utilizados

O pacote de dados do ESCO contém diversos arquivos. Para este projeto foram selecionados especificamente:

| Arquivo                           |   Registros |
| --------------------------------- | ----------: |
| `occupations_pt.csv`              |       3.043 |
| `skills_pt.csv`                   |      13.960 |
| `occupationSkillRelations_pt.csv` |     126.051 |
| **Total**                         | **143.054** |

O total corresponde à soma dos registros dos três arquivos analisados.

O arquivo `occupationSkillRelations_pt.csv` possui grande quantidade de registros porque uma mesma ocupação pode estar relacionada a diversas habilidades, conhecimentos e competências. Portanto, os **143.054 registros não correspondem a 143.054 ocupações distintas**.

## Fonte original

**European Commission – ESCO**

Página oficial para download:

https://esco.ec.europa.eu/en/use-esco/download

## Como obter os dados do ESCO

Os arquivos utilizados no projeto não serão armazenados diretamente neste repositório.

Para obter os dados:

1. Acessar a página oficial de download do ESCO:

   https://esco.ec.europa.eu/en/use-esco/download

2. Selecionar a versão **ESCO v1.2.1** utilizada neste projeto.

3. Selecionar o conjunto de dados de classificação (**Classification**).

4. Selecionar o idioma **Português (pt)**.

5. Solicitar o download dos dados.

6. Informar um **endereço de e-mail válido** no formulário disponibilizado pelo ESCO.

7. O ESCO enviará para o endereço informado um **link para download do arquivo ZIP**.

8. Baixar o arquivo ZIP recebido por e-mail.

9. Extrair o conteúdo do arquivo.

10. Dentro do pacote, localizar os arquivos utilizados neste projeto:

    * `occupations_pt.csv`
    * `skills_pt.csv`
    * `occupationSkillRelations_pt.csv`

Os demais arquivos presentes no pacote não foram utilizados diretamente nesta etapa do projeto.



