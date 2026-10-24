import json
from app.services import armazenamento

def test_salvar_obter_limpar(tmp_path, monkeypatch):
    monkeypatch.setattr(armazenamento, 'DATABASE_PATH', str(tmp_path / 'test.db'))
    armazenamento.salvar('123', 'entrevista_resposta', {'cargo':'motorista','numero':2})
    resultado = armazenamento.obter('123')
    assert resultado['estado'] == 'entrevista_resposta'
    assert resultado['dados']['cargo'] == 'motorista'
    armazenamento.limpar('123')
    assert armazenamento.obter('123')['estado'] == 'menu'
