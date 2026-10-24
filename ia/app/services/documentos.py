from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def arquivo_pdf(titulo: str, conteudo: str) -> str:
    pasta = Path(__file__).resolve().parents[2] / "outputs"
    pasta.mkdir(parents=True, exist_ok=True)

    seguro = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        titulo.lower()
    ).strip("_")[:50] or "documento"

    caminho = pasta / f"{seguro}.pdf"

    documento = SimpleDocTemplate(
        str(caminho),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=titulo.replace("_", " ").title(),
        author="Agente de Carreira",
    )

    estilos = getSampleStyleSheet()

    estilos.add(ParagraphStyle(
        name="TituloDocumento",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=23,
        textColor=colors.HexColor("#17365D"),
        alignment=TA_CENTER,
        spaceAfter=16,
    ))

    estilos.add(ParagraphStyle(
        name="Secao",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True,
    ))

    estilos.add(ParagraphStyle(
        name="CorpoDocumento",
        parent=estilos["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        alignment=TA_LEFT,
        spaceAfter=5,
        wordWrap="LTR",
    ))

    elementos = []
    titulo_formatado = titulo.replace("_", " ").title()
    elementos.append(Paragraph(
        escape(titulo_formatado),
        estilos["TituloDocumento"]
    ))
    elementos.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#17365D"),
        spaceAfter=14,
    ))

    for linha in conteudo.splitlines():
        texto = linha.strip()

        if not texto or texto == "---":
            elementos.append(Spacer(1, 5))
            continue

        # Converte títulos Markdown, como **EXPERIÊNCIA PROFISSIONAL**
        secao = re.fullmatch(r"\*\*(.+?)\*\*", texto)

        if secao:
            elementos.append(Paragraph(
                escape(secao.group(1)),
                estilos["Secao"]
            ))
            continue

        # Converte itens de listas
        if texto.startswith("* ") or texto.startswith("- "):
            texto = "• " + texto[2:]

        # Remove a marcação Markdown de negrito
        texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
        texto = re.sub(r"\*(.+?)\*", r"\1", texto)

        elementos.append(Paragraph(
            escape(texto),
            estilos["CorpoDocumento"]
        ))

    def numerar_paginas(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(
            A4[0] / 2,
            1 * cm,
            f"Página {doc.page}"
        )
        canvas.restoreState()

    documento.build(
        elementos,
        onFirstPage=numerar_paginas,
        onLaterPages=numerar_paginas,
    )

    return str(caminho)
