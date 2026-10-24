import csv, re, unicodedata
from pathlib import Path
from app.config import CBO_DATA_DIR

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()

def _ler_csv(caminho: Path):
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            with caminho.open("r", encoding=encoding, newline="") as f:
                sample = f.read(4096); f.seek(0)
                try: dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
                except csv.Error: dialect = csv.excel
                yield from csv.DictReader(f, dialect=dialect)
            return
        except UnicodeDecodeError:
            continue
        except OSError:
            return

def buscar_referencias(cargo: str, limite: int = 5) -> list[dict]:
    """Busca lexical simples nos CSVs processados, sem embeddings ou serviços pagos."""
    cargo_norm = normalizar(cargo)
    termos = [t for t in cargo_norm.split() if len(t) > 2]
    if not termos or not CBO_DATA_DIR.exists(): return []
    resultados = []
    arquivos = [CBO_DATA_DIR / "CBO_ocupacao_processed.csv", CBO_DATA_DIR / "CBO_sinonimo_processed.csv", CBO_DATA_DIR / "ESCO_occupations_processed.csv", CBO_DATA_DIR / "ESCO_skills_processed.csv"]
    vistos = set()
    for arquivo in arquivos:
        if not arquivo.exists(): continue
        for row in _ler_csv(arquivo):
            valores = [str(v) for v in row.values() if v]
            texto = " | ".join(valores)
            norm = normalizar(texto)
            cobertura = sum(1 for t in termos if t in norm) / len(termos)
            if cobertura < 0.5: continue
            chave = normalizar(texto[:300])
            if chave in vistos: continue
            vistos.add(chave)
            resultados.append({"fonte": arquivo.name, "texto": texto[:900], "score": cobertura})
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:limite]
