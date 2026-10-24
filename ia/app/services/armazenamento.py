import json, sqlite3
from pathlib import Path
from app.config import DATABASE_PATH

def conectar():
    path = Path(DATABASE_PATH); path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path); con.row_factory = sqlite3.Row
    con.execute('''CREATE TABLE IF NOT EXISTS conversas (chat_id TEXT PRIMARY KEY, estado TEXT NOT NULL, dados TEXT NOT NULL, atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP)''')
    con.commit(); return con

def obter(chat_id: str):
    with conectar() as con:
        row = con.execute('SELECT estado,dados FROM conversas WHERE chat_id=?', (str(chat_id),)).fetchone()
    return {"estado": row["estado"], "dados": json.loads(row["dados"])} if row else {"estado":"menu", "dados":{}}

def salvar(chat_id: str, estado: str, dados: dict):
    with conectar() as con:
        con.execute('INSERT INTO conversas(chat_id,estado,dados,atualizado_em) VALUES(?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(chat_id) DO UPDATE SET estado=excluded.estado,dados=excluded.dados,atualizado_em=CURRENT_TIMESTAMP', (str(chat_id), estado, json.dumps(dados, ensure_ascii=False)))
        con.commit()

def limpar(chat_id: str):
    with conectar() as con:
        con.execute('DELETE FROM conversas WHERE chat_id=?', (str(chat_id),)); con.commit()
