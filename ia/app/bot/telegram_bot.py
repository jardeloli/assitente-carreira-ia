import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from app.config import TELEGRAM_BOT_TOKEN
from app.services.armazenamento import obter, salvar, limpar
from app.services.agente import gerar_curriculo, gerar_carta, gerar_pergunta, avaliar_resposta, resumo_entrevista
from app.services.documentos import arquivo_pdf

MENU = InlineKeyboardMarkup([[InlineKeyboardButton('📄 Gerar currículo', callback_data='curriculo')], [InlineKeyboardButton('✉️ Carta de apresentação', callback_data='carta')], [InlineKeyboardButton('🎤 Simular entrevista', callback_data='entrevista')], [InlineKeyboardButton('❓ Ajuda', callback_data='ajuda')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpar(update.effective_chat.id)
    await update.message.reply_text('Olá! Sou seu Agente de Carreira. Você não precisa criar perfil nem fazer cadastro. Escolha uma opção ou escreva diretamente o que deseja fazer.', reply_markup=MENU)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('O que você gostaria de fazer?', reply_markup=MENU)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('Use os botões ou escreva em linguagem natural. Comandos: /start, /menu, /ajuda e /cancelar. No momento, o bot aceita texto; voz poderá ser adicionada depois.')

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpar(update.effective_chat.id)
    await update.effective_message.reply_text('Tarefa cancelada. O que deseja fazer agora?', reply_markup=MENU)

async def escolher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    escolha = q.data
    if escolha == 'ajuda':
        await q.message.reply_text('Você pode gerar currículo, carta ou praticar entrevista. Não precisa criar perfil. Envie suas informações em texto livre.'); return
    prompts = {'curriculo':'Vamos montar seu currículo. Informe o cargo desejado e conte, do seu jeito, sobre sua experiência, formação, cursos e habilidades. Se for seu primeiro emprego, diga isso e conte sobre estudos ou atividades relevantes.', 'carta':'Vamos preparar sua carta. Informe o cargo, a empresa (para qual irá encaminhar a carta) e conte um pouco sobre sua experiência, formação e interesse pela vaga.', 'entrevista':'Qual cargo você quer praticar para a entrevista? Se quiser, conte também um pouco sobre sua experiência.'}
    salvar(q.message.chat_id, escolha + ('_cargo' if escolha == 'entrevista' else '_dados'), {})
    await q.message.reply_text(prompts[escolha])

def inferir_intencao(texto: str):
    t = texto.lower()
    if any(x in t for x in ['currículo','curriculo','cv','montar meu currículo','gerar currículo']): return 'curriculo'
    if any(x in t for x in ['carta de apresentação','carta apresentação','carta para vaga']): return 'carta'
    if any(x in t for x in ['entrevista','simular entrevista','treinar entrevista','praticar entrevista']): return 'entrevista'
    return None


async def finalizar_documento(update: Update, chat_id: int, dados: dict):
    tipo = dados["tipo_documento"]
    pessoais = dados["pessoais"]

    informacoes = dados["informacoes"]

    informacoes += f"""
    DADOS PESSOAIS CONFIRMADOS:
    Nome completo: {pessoais["nome"]}
    Telefone: {pessoais["telefone"]}
    Cidade/UF: {pessoais["cidade"]}
    """

    if pessoais.get("email"):
        informacoes += f'E-mail: {pessoais["email"]}\n'
    else:
        informacoes += (
            "E-mail: não informado. "
            "Não incluir campo de e-mail no documento.\n"
        )

    try:
        await update.effective_message.reply_text(
            "Estou preparando seu documento. "
            "Isso pode levar alguns segundos…"
        )

        if tipo == "curriculo":
            cargo = dados.get("cargo") or "cargo compatível com a experiência informada"
            resultado = await asyncio.to_thread(
                gerar_curriculo, informacoes, cargo
            )
            titulo = "curriculo"
        else:
            cargo = dados.get("cargo") or "cargo desejado"
            empresa = dados.get("empresa") or ""
            resultado = await asyncio.to_thread(
                gerar_carta, informacoes, cargo, empresa
            )
            titulo = "carta_apresentacao"

        caminho = arquivo_pdf(titulo, resultado)
        
        with open(caminho, "rb") as arquivo:
            await update.effective_message.reply_document(
                document=arquivo,
                filename=f"{titulo}.pdf",
                caption="Revise as informações antes de utilizar o documento."
            )

        await update.effective_message.reply_text(
            "Documento gerado! O que deseja fazer agora?",
            reply_markup=MENU
        )

    except Exception as e:
        await update.effective_message.reply_text(
            f"Não consegui gerar o documento. Detalhe: {str(e)[:250]}",
            reply_markup=MENU
        )

    finally:
        limpar(chat_id)


async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id; texto = (update.message.text or '').strip()
    sessao = obter(chat_id); estado = sessao['estado']; dados = sessao['dados']
    if estado == 'menu':
        intencao = inferir_intencao(texto)
        if not intencao:
            await update.message.reply_text('Posso ajudar com currículo, carta de apresentação ou entrevista simulada. O que você prefere?', reply_markup=MENU); return
        salvar(chat_id, intencao + ('_cargo' if intencao == 'entrevista' else '_dados'), {})
        await update.message.reply_text({'curriculo':'Informe o cargo desejado e conte suas experiências, formação, cursos e habilidades. Pode escrever livremente.', 'carta':'Informe o cargo, a empresa se souber, e suas experiências, formação e interesse pela vaga.', 'entrevista':'Qual cargo você deseja praticar para a entrevista?'}[intencao]); return

    if estado in ('curriculo_dados', 'carta_dados'):
        tipo = 'curriculo' if estado == 'curriculo_dados' else 'carta'

        dados = {
            'tipo_documento': tipo,
            'informacoes': texto,
            'pessoais': {}
        }

        salvar(chat_id, 'coletar_nome', dados)

        await update.message.reply_text(
            'Vamos completar seus dados pessoais.\n\n'
            'Qual é o seu nome completo?'
        )
        return

    if estado == 'coletar_nome':
        if len(texto.split()) < 2:
            await update.message.reply_text(
                'Informe seu nome completo, incluindo pelo menos '
                'nome e sobrenome.'
            )
            return

        dados['pessoais']['nome'] = texto
        salvar(chat_id, 'coletar_telefone', dados)

        await update.message.reply_text(
            'Qual é o seu telefone com DDD?'
        )
        return

    if estado == 'coletar_telefone':
        telefone = ''.join(c for c in texto if c.isdigit())

        if len(telefone) < 10:
            await update.message.reply_text(
                'O telefone parece incompleto. Informe o número '
                'com DDD, por favor.'
            )
            return

        dados['pessoais']['telefone'] = texto
        salvar(chat_id, 'coletar_cidade', dados)

        await update.message.reply_text(
            'Em qual cidade e estado você mora? '
            'Exemplo: Balsas - MA.'
        )
        return

    if estado == 'coletar_cidade':
        dados['pessoais']['cidade'] = texto
        salvar(chat_id, 'coletar_email', dados)

        await update.message.reply_text(
            'Qual é o seu e-mail? Ele é opcional.\n\n'
            'Se não quiser informar, responda "Não".'
        )
        return

    if estado == 'coletar_email':
        resposta = texto.strip()
        opcional_nao_informado = {
            'não', 'nao', 'pular', 'não tenho', 'nao tenho',
            'prefiro não informar', 'prefiro nao informar',
            'sem email', 'sem e-mail'
        }

        if resposta.lower() not in opcional_nao_informado:
            if '@' not in resposta or '.' not in resposta.split('@')[-1]:
                await update.message.reply_text(
                    'O e-mail parece inválido. Informe um e-mail válido '
                    'ou responda "Não" para continuar sem ele.'
                )
                return

            dados['pessoais']['email'] = resposta

        salvar(chat_id, 'gerando_documento', dados)
        await finalizar_documento(update, chat_id, dados)
        return

    if estado == 'entrevista_cargo':
        dados = {'cargo': texto, 'numero': 1, 'historico': [], 'informacoes': ''}
        try:
            pergunta = await asyncio.to_thread(gerar_pergunta, texto, 1)
            dados['pergunta_atual'] = pergunta
            salvar(chat_id, 'entrevista_resposta', dados)
            await update.message.reply_text(f'Vamos começar sua entrevista para **{texto}**. Pergunta 1 de 8:\n\n{pergunta}', parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f'Erro ao iniciar entrevista: {str(e)[:200]}', reply_markup=MENU); limpar(chat_id)
        return
    if estado == 'entrevista_resposta':
        cargo = dados['cargo']; numero = int(dados['numero']); pergunta = dados['pergunta_atual']
        await update.message.reply_text('Analisando sua resposta…')
        try:
            feedback = await asyncio.to_thread(avaliar_resposta, cargo, pergunta, texto)
            dados['historico'].append({'pergunta': pergunta, 'resposta': texto, 'feedback': feedback})
            if numero >= 8:
                resumo = await asyncio.to_thread(resumo_entrevista, cargo, str(dados['historico']))
                await update.message.reply_text('Feedback da última resposta:\n' + feedback)
                await update.message.reply_text('Resumo final da entrevista:\n' + resumo, reply_markup=MENU)
                limpar(chat_id); return
            proximo = numero + 1
            historico_txt = '\n'.join(f"P: {x['pergunta']} R: {x['resposta']}" for x in dados['historico'])
            nova = await asyncio.to_thread(gerar_pergunta, cargo, proximo, dados.get('informacoes',''), historico_txt)
            dados['numero'] = proximo; dados['pergunta_atual'] = nova
            salvar(chat_id, 'entrevista_resposta', dados)
            await update.message.reply_text(f'Feedback da resposta {numero}:\n{feedback}\n\nPergunta {proximo} de 8:\n{nova}')
        except Exception as e:
            await update.message.reply_text(f'Não consegui processar a resposta. Tente novamente. Detalhe: {str(e)[:200]}')
        return
    await update.message.reply_text('Vamos voltar ao menu.', reply_markup=MENU); limpar(chat_id)

async def post_init(app: Application):
    print('Bot de carreira iniciado. Pressione Ctrl+C para encerrar.')

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            'Configure TELEGRAM_BOT_TOKEN no arquivo .env antes de iniciar o bot.'
        )

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('menu', menu))
    app.add_handler(CommandHandler('ajuda', ajuda))
    app.add_handler(CommandHandler('cancelar', cancelar))

    app.add_handler(CallbackQueryHandler(escolher))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem)
    )

    # Compatibilidade com versões recentes do Python
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()