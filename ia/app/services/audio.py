"""Transcrição de mensagens de voz e áudio enviadas pelo Telegram.

Usa o próprio Gemini (que aceita áudio como entrada) para converter a fala em
texto. O texto transcrito segue depois pelo mesmo fluxo das mensagens escritas.
"""
import base64
from functools import lru_cache

from app.config import GEMINI_API_KEY, GEMINI_MODEL

# Formatos de áudio aceitos pelo Gemini, com os apelidos que o Telegram usa.
FORMATOS_SUPORTADOS = {
    "audio/ogg": "audio/ogg",
    "audio/opus": "audio/ogg",
    "audio/mpeg": "audio/mp3",
    "audio/mp3": "audio/mp3",
    "audio/wav": "audio/wav",
    "audio/x-wav": "audio/wav",
    "audio/wave": "audio/wav",
    "audio/aac": "audio/aac",
    "audio/flac": "audio/flac",
    "audio/x-flac": "audio/flac",
    "audio/aiff": "audio/aiff",
    "audio/x-aiff": "audio/aiff",
}

MARCADOR_INAUDIVEL = "[INAUDÍVEL]"

# Orientações extras conforme o dado que o bot está pedindo no momento.
DICAS_POR_ESTADO = {
    "coletar_nome": (
        "A pessoa está dizendo o próprio nome completo. "
        "Escreva o nome com iniciais maiúsculas."
    ),
    "coletar_telefone": (
        "A pessoa está ditando um número de telefone com DDD. "
        "Escreva apenas os algarismos, sem palavras."
    ),
    "coletar_email": (
        "A pessoa está ditando um endereço de e-mail. Escreva-o no formato "
        "usuario@dominio.com, sem espaços, convertendo 'arroba' em @ e "
        "'ponto' em '.'. Se a pessoa disser que não tem ou não quer informar "
        "e-mail, devolva exatamente: Não"
    ),
}

PROMPT_TRANSCRICAO = """Transcreva fielmente a fala deste áudio em português brasileiro.
Regras:
- Devolva somente a transcrição, sem comentários, títulos ou aspas.
- Não resuma, não corrija o conteúdo e não acrescente informações.
- Use pontuação natural e escreva números em algarismos.
- Se não houver fala compreensível, devolva exatamente: {inaudivel}
{dica}"""


class FormatoNaoSuportado(ValueError):
    """O arquivo de áudio enviado está em um formato que o Gemini não aceita."""


def normalizar_mime(mime_type: str | None) -> str:
    """Converte o tipo informado pelo Telegram para um formato aceito pelo Gemini."""
    base = (mime_type or "audio/ogg").split(";")[0].strip().lower()
    if base not in FORMATOS_SUPORTADOS:
        raise FormatoNaoSuportado(base)
    return FORMATOS_SUPORTADOS[base]


@lru_cache(maxsize=1)
def _modelo_transcricao():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY não configurada no arquivo .env")
    from langchain_google_genai import ChatGoogleGenerativeAI
    # Temperatura zero: a transcrição deve ser literal, não criativa.
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY, temperature=0
    )


def _extrair_texto(conteudo) -> str:
    """O LangChain pode devolver o conteúdo como texto ou como lista de blocos."""
    if isinstance(conteudo, str):
        return conteudo
    partes = []
    for bloco in conteudo or []:
        if isinstance(bloco, str):
            partes.append(bloco)
        elif isinstance(bloco, dict) and bloco.get("type") == "text":
            partes.append(bloco.get("text", ""))
    return "".join(partes)


def transcrever_audio(conteudo: bytes, mime_type: str | None, estado: str = "") -> str:
    """Transcreve o áudio e devolve o texto, ou "" se não houver fala compreensível."""
    from langchain_core.messages import HumanMessage

    formato = normalizar_mime(mime_type)
    prompt = PROMPT_TRANSCRICAO.format(
        inaudivel=MARCADOR_INAUDIVEL, dica=DICAS_POR_ESTADO.get(estado, "")
    ).strip()
    mensagem = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {
            "type": "media",
            "mime_type": formato,
            "data": base64.b64encode(bytes(conteudo)).decode("ascii"),
        },
    ])
    resposta = _modelo_transcricao().invoke([mensagem])
    texto = _extrair_texto(resposta.content).strip().strip('"“”«»').strip()
    if not texto or MARCADOR_INAUDIVEL in texto:
        return ""
    return texto
