from app.services.base_conhecimento import normalizar

def test_normalizar_remove_acentos():
    assert normalizar('Auxiliar Administrativo') == 'auxiliar administrativo'
