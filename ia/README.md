# Agente de Carreira — MVP

MVP conversacional para Telegram com Python, FastAPI, LangChain, Gemini e recuperação lexical das bases CBO/ESCO já presentes no repositório.

## Funcionalidades
- Telegram com comandos, botões e mensagens de texto em linguagem natural.
- Geração de currículo e carta de apresentação via Gemini.
- Entrevista simulada com oito perguntas, feedback por resposta e resumo final.
- SQLite para estado de tarefa; não existe cadastro ou perfil profissional permanente.
- FastAPI com `/health` para diagnóstico.

## Requisitos
Python 3.11 recomendado. As bases CBO/ESCO ficam na pasta `../big_data/data/processed` em relação a `ia`.

## Configuração no Windows (PowerShell)
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edite `.env` e informe `GEMINI_API_KEY` e `TELEGRAM_BOT_TOKEN`. Crie o bot com `@BotFather`; obtenha a chave Gemini no Google AI Studio. Nunca envie ou comite os tokens.

## Executar bot
Na pasta `ia`:
```powershell
python -m app.bot.telegram_bot
```
No Telegram, abra o bot e envie `/start`. O bot usa polling para facilitar testes locais.

## Executar API
Em outro terminal, na pasta `ia`:
```powershell
uvicorn app.main:app --reload
```
Abra `http://127.0.0.1:8000/docs` e verifique `http://127.0.0.1:8000/health`.

## Testes
```powershell
pytest -q
```

## Observações do MVP
- O usuário não cria conta nem preenche perfil. O ID do chat do Telegram é usado apenas para separar estados de conversa.
- Currículo e carta são entregues como `.txt` nesta primeira versão; PDF/DOCX e voz podem ser adicionados depois.
- A recuperação CBO/ESCO é lexical e inicial, não um sistema vetorial completo.
- A integração real com Gemini e Telegram exige chaves válidas e conexão com a internet.
- Revise todo documento gerado antes de utilizá-lo. A IA não deve inventar dados pessoais ou profissionais.
