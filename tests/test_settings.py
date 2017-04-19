#! -*- Coding: UTF-8 -*-
import settings


def test_mcod_key_in_login():
    assert "mCod" in settings.LOGIN.keys()

def test_msenha_key_in_login():
    assert "mSenha" in settings.LOGIN.keys()

def test_mgermodulo_key_in_login():
    assert "mGerModulo" in settings.LOGIN.keys()

def test_btnprocesso_key_in_login():
    assert "btnProcesso" in settings.LOGIN.keys()

def test_musuario_key_in_login():
    assert "mUsuario" in settings.LOGIN.keys()

def test_login_is_dict():
    assert type(settings.LOGIN) is dict

def test_total_login_keys():
    assert len(settings.LOGIN) == 5

def test__dominio_settings():
    assert settings._DOMINIO == \
           "http://www.inmet.gov.br/projetos/rede/pesquisa/"

def test_filter():
    filter = "&mRelEstacao={estacao}&btnProcesso=serie" \
             "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"
    assert settings._FILTER == filter

def test_url_index():
    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php"
    assert settings.URL_INDEX == url

def test__url_base_diarios_horarios():
    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
          "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
          "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"
    assert settings._URL_BASE_DIARIOS_HORARIOS == url

def test_url_dados_diarios():
    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
          "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
          "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
          "&mAtributos=,,1,1,,,,,,1,1,,1,1,1,1,"
    assert settings.URL_DADOS_DIARIOS == url

def url_dados_horarios():
    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
          "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
          "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
          "&mAtributos=1,1,,,1,1,,1,1,,,1,,,,,"
    assert settings.URL_DADOS_HORARIOS == url

def url_dados_mensais():
    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
          "gera_serie_txt_mensal.php?&mRelEstacao={estacao}" \
          "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
          "&btnProcesso=serie&mAtributos=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
    assert settings.URL_DADOS_DIARIOS == url

def test_ancora():
    assert settings.ANCORA == "\nEstacao"

def test_secret_key():
    key = "\nA\xe3\xf5\x94\xe3\xb9\xae\xdf\xeb\xf3" \
          "\x80\xf0i\xc7[\xb49D\x88\x1d\xfa\x8aR"
    assert settings.SECRET_KEY == key
