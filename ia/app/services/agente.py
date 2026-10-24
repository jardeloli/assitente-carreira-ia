from functools import lru_cache
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.services.base_conhecimento import buscar_referencias

@lru_cache(maxsize=1)

def _modelo():

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY não configurada no arquivo .env")
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY, temperature=0.4)

def gerar_texto(prompt: str) -> str:
    resposta = _modelo().invoke(prompt)
    return str(resposta.content).strip()

def gerar_curriculo(informacoes: str, cargo: str) -> str:
    refs = buscar_referencias(cargo)
    contexto = "\n".join(f"- {r['texto']}" for r in refs) or "Nenhuma referência específica foi encontrada."

    return gerar_texto(f"""Você é um assistente de carreira. Escreva um currículo em português brasileiro, claro e profissional, para o cargo: {cargo}.
    Use somente fatos fornecidos pelo candidato. Nunca invente experiência, formação, datas, cursos, resultados ou competências. Os dados pessoais obrigatórios já foram coletados antes da geração.
    Utilize o nome completo, telefone e cidade/UF fornecidos.
    O e-mail é opcional: se não foi informado, omita completamente
    essa informação. Nunca escreva marcadores como [Nome completo],
    [Telefone: informação a preencher] ou [E-mail: informação a preencher].
    Nunca invente dados pessoais.. Não invente nome, telefone, endereço ou e-mail.
    Informações do candidato:
    {informacoes}
    Referências ocupacionais opcionais (use apenas para compreender o cargo, nunca como experiência do candidato):
    {contexto}
    Entregue um currículo bem formatado em texto simples, com seções adequadas ao perfil. Para primeiro emprego, destaque formação, projetos, cursos e competências reais quando fornecidos.""")

def gerar_carta(informacoes: str, cargo: str, empresa: str = "") -> str:
    refs = buscar_referencias(cargo)
    contexto = "\n".join(f"- {r['texto']}" for r in refs) or "Sem referências adicionais."
    
    return gerar_texto(f"""Redija uma carta de apresentação profissional em português brasileiro para candidatura ao cargo de {cargo}. Empresa: {empresa or 'não informada'}.
Não invente experiências, qualificações ou resultados. Use apenas os fatos informados e mantenha tom natural, objetivo e respeitoso. Se faltarem dados pessoais, não os invente.
Informações fornecidas:
{informacoes}
Contexto ocupacional de referência:
{contexto}
Entregue somente a carta, com saudação e encerramento apropriados.""")

def gerar_pergunta(cargo: str, numero: int, informacoes: str = "", historico: str = "") -> str:
    return gerar_texto(f"Crie UMA pergunta de entrevista de emprego em português brasileiro para o cargo '{cargo}'. Esta é a pergunta {numero} de 8. Varie entre experiência, situações práticas, resolução de problemas, trabalho em equipe e motivação. Contexto do candidato: {informacoes or 'não informado'}. Perguntas/respostas anteriores: {historico or 'nenhuma'}. Não inclua feedback nem mais de uma pergunta; devolva somente a pergunta.")

def avaliar_resposta(cargo: str, pergunta: str, resposta: str) -> str:
    return gerar_texto(f"Avalie de forma construtiva uma resposta de entrevista para o cargo '{cargo}'. Pergunta: {pergunta}. Resposta: {resposta}. Em português brasileiro, forneça: Pontos positivos; O que melhorar; Exemplo de resposta mais clara (sem inventar fatos pessoais). Não dê nota eliminatória nem afirme prever contratação.")

def resumo_entrevista(cargo: str, respostas: str) -> str:
    return gerar_texto(f"Faça um resumo construtivo da entrevista simulada para o cargo '{cargo}', com pontos fortes, aspectos a praticar e três dicas concretas. Não classifique o candidato nem prometa contratação. Respostas e feedbacks: {respostas}")
