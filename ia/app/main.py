from fastapi import FastAPI
from app.config import GEMINI_API_KEY, TELEGRAM_BOT_TOKEN
app = FastAPI(title='Agente de Carreira API', version='0.1.0', description='API de apoio ao bot do Telegram do Agente de Carreira.')
@app.get('/health')
def health():
    return {'status':'ok', 'gemini_configurada':bool(GEMINI_API_KEY), 'telegram_configurado':bool(TELEGRAM_BOT_TOKEN)}
