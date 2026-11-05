# Agente de Carreira IA — MVP

O **Agente de Carreira IA** é um assistente virtual desenvolvido para apoiar pessoas em sua jornada profissional, desde a busca pelo primeiro emprego até a recolocação no mercado de trabalho.

O projeto utiliza inteligência artificial para auxiliar na elaboração de currículos, criação de cartas de apresentação e preparação para entrevistas de emprego. A proposta é simplificar essas atividades por meio de uma conversa natural, permitindo que o usuário informe seus dados e receba orientações personalizadas sem precisar utilizar ferramentas complexas.

Nesta versão do MVP (*Minimum Viable Product*), a interação acontece pelo **Telegram**, utilizado como canal de validação da experiência conversacional. Ainda não foram desenvolvidas telas próprias para web ou dispositivos móveis.

## Funcionalidades

- **Chat pelo Telegram:** interação por comandos, botões e mensagens de texto em linguagem natural.
- **Geração de currículos:** organização de experiências profissionais, escolaridade, cursos e competências com auxílio do Gemini.
- **Carta de apresentação:** criação de textos de apresentação profissional conforme as informações fornecidas pelo usuário.
- **Entrevista simulada:** simulação com oito perguntas, feedback após cada resposta e resumo de desempenho ao final.
- **Recuperação de informações profissionais:** consulta lexical às bases CBO e ESCO disponíveis no repositório para auxiliar na identificação de ocupações e competências.
- **Gerenciamento de conversas:** utilização do SQLite para armazenar o estado das tarefas e manter a continuidade dos fluxos.
- **API com FastAPI:** disponibilização de uma rota `/health` para verificar o funcionamento do serviço.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal do projeto. |
| Telegram Bot API | Interface de comunicação com o usuário. |
| FastAPI | Estruturação da API do projeto. |
| LangChain | Organização da integração com modelos de linguagem e fluxos de IA. |
| Google Gemini | Processamento de linguagem natural e geração de conteúdo. |
| SQLite | Persistência do estado das conversas e tarefas. |
| CBO e ESCO | Bases de referência para ocupações e competências profissionais. |
| Pytest | Execução dos testes automatizados. |

## Estrutura do projeto

A aplicação está organizada dentro da pasta `ia`, separando os módulos responsáveis pelo bot, API, serviços e testes.

```text
assitente-carreira-ia/
│
├── ia/
│   ├── app/
│   │   ├── bot/
│   │   │   └── telegram_bot.py
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── tests/
|   ├──.env
│   ├── .env.example
│   ├── requirements.txt
│   └── ...
│
├── big_data/
│   └── data/
│       └── processed/
│           └── bases CBO/ESCO
│
└── README.md
```

> **Observação:** a estrutura acima representa os principais diretórios e arquivos. Outros módulos e arquivos auxiliares podem existir no projeto.

## Requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.11 instalado.
- Git instalado (caso ainda não tenha clonado o repositório).
- Uma conta no Telegram.
- Um token de bot criado pelo BotFather.
- Uma chave de API do Google Gemini.
- Conexão com a internet.

As bases CBO/ESCO utilizadas pela recuperação lexical devem estar disponíveis em:

```text
big_data/data/processed/
```

O caminho é considerado em relação à raiz do repositório.

## Configuração do ambiente

### 1. Clonar o repositório

Abra o terminal e execute:

```powershell
git clone https://github.com/jardeloli/assitente-carreira-ia.git
```

Entre na pasta do projeto:

```powershell
cd assitente-carreira-ia
```

Acesse a pasta da aplicação:

```powershell
cd ia
```

### 2. Criar o ambiente virtual

Recomenda-se utilizar o Python 3.11 para executar o projeto.

```powershell
py -3.11 -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação do ambiente virtual, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, tente ativá-lo novamente:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

Com o ambiente virtual ativado, atualize o instalador de pacotes:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências do projeto:

```powershell
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie o arquivo `.env` a partir do arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e preencha as configurações necessárias:

```env
GEMINI_API_KEY=sua_chave_api_gemini
TELEGRAM_BOT_TOKEN=seu_token_telegram
```

**Como obter as credenciais:**

- **Token do Telegram:** converse com o [@BotFather](https://t.me/BotFather), crie um bot com o comando `/newbot` e copie o token fornecido.
- **Chave Gemini:** acesse o [Google AI Studio](https://aistudio.google.com/), gere uma chave de API e copie o valor para o arquivo `.env`.

> **Importante:** nunca compartilhe suas credenciais e nunca envie o arquivo `.env` para o GitHub. O arquivo deve permanecer protegido pelo `.gitignore`. O `.env.example` deve conter apenas valores ilustrativos.

## Executando o chat pelo Telegram

Esta é a principal forma de interação com o MVP.

### 1. Iniciar o bot

Certifique-se de estar dentro da pasta `ia` e com o ambiente virtual ativado.

Execute:

```powershell
python -m app.bot.telegram_bot
```

Se estiver tudo configurado corretamente, o terminal deverá indicar que o bot foi iniciado.

Mantenha esse terminal aberto enquanto estiver utilizando o chat. O bot utiliza o mecanismo de *polling* para receber as mensagens enviadas pelo Telegram.

### 2. Abrir o bot no Telegram

1. Abra o Telegram no computador ou celular.
2. Pesquise pelo nome de usuário do bot criado no BotFather.
3. Abra a conversa com o bot.
4. Clique em **Iniciar** ou envie o comando:

```text
/start
```

### 3. Interagir com o assistente

Após iniciar a conversa, o bot apresentará as opções e orientações disponíveis.

O usuário poderá solicitar funcionalidades por meio dos comandos, botões ou mensagens de texto, conforme os fluxos implementados.

**Exemplo de solicitação para criação de currículo:**

```text
Quero criar um currículo para procurar emprego.
```

O assistente poderá conduzir a conversa para coletar as informações necessárias, como:

- Nome completo;
- Telefone;
- Cidade e estado;
- Experiências profissionais;
- Escolaridade;
- Cursos e qualificações;
- Competências profissionais.

As informações obrigatórias devem ser coletadas antes da elaboração do currículo. O e-mail é opcional.

**Exemplo de solicitação para entrevista simulada:**

```text
Quero fazer uma entrevista simulada para uma vaga de auxiliar administrativo.
```

O agente iniciará o fluxo de entrevista, apresentando as perguntas e fornecendo feedback sobre as respostas.

### 4. Encerrar a execução

Para encerrar o bot, volte ao terminal em que ele está sendo executado e pressione:

```text
Ctrl + C
```

## Executando a API

Além do bot do Telegram, o projeto possui uma API desenvolvida com FastAPI.

Para executá-la, abra **outro terminal**, acesse a pasta `ia` e ative o ambiente virtual, caso necessário.

Execute:

```powershell
uvicorn app.main:app --reload
```

A API será disponibilizada localmente no endereço:

```text
http://127.0.0.1:8000
```

**Documentação interativa:**

http://127.0.0.1:8000/docs

**Verificação de saúde da aplicação:**

http://127.0.0.1:8000/health

A rota `/health` permite verificar se o serviço está respondendo corretamente.

## Executando os testes

Com o ambiente virtual ativado e as dependências instaladas, execute:

```powershell
pytest -q
```

O Pytest executará os testes automatizados disponíveis no diretório `tests`.

## Observações e limitações do MVP

- **Sem cadastro de usuários:** não existe criação de conta ou perfil profissional permanente. O ID do chat do Telegram é utilizado para separar os estados das conversas.
- **Interface:** nesta etapa, o Telegram é utilizado para validar a experiência conversacional. Não foram desenvolvidas telas próprias para web ou mobile.
- **Comunicação textual:** o MVP trabalha com mensagens de texto. A funcionalidade de envio e processamento de áudio ainda não foi implementada.
- **Documentos:** nesta versão, os currículos e as cartas são entregues em formato `.txt`. A geração em PDF ou DOCX poderá ser incorporada em etapas futuras.
- **Recuperação CBO/ESCO:** a recuperação é lexical e inicial, não sendo um sistema vetorial completo.
- **Integrações externas:** o funcionamento real do Gemini e do Telegram depende de credenciais válidas e conexão com a internet.
- **Validação das informações:** o usuário deve revisar todo conteúdo gerado antes de utilizá-lo profissionalmente. A inteligência artificial não deve inventar experiências, qualificações ou dados pessoais.


**Agente de Carreira IA — MVP**

Projeto desenvolvido para demonstrar a aplicação de inteligência artificial no apoio à carreira profissional, utilizando uma abordagem incremental de desenvolvimento e validação de um Produto Mínimo Viável.