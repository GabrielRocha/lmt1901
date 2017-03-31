#! -*- Coding: UTF-8 -*-
import settings


class TestCaseSettings():

    def test_mcod_key_in_login(self):
        assert "mCod" in settings.LOGIN.keys()

    def test_msenha_key_in_login(self):
        assert "mSenha" in settings.LOGIN.keys()

    def test_mgermodulo_key_in_login(self):
        assert "mGerModulo" in settings.LOGIN.keys()

    def test_btnprocesso_key_in_login(self):
        assert "btnProcesso" in settings.LOGIN.keys()

    def test_musuario_key_in_login(self):
        assert "mUsuario" in settings.LOGIN.keys()

    def test_login_is_dict(self):
        assert type(settings.LOGIN) is dict

    def test_total_login_keys(self):
        assert len(settings.LOGIN) == 5

    def test__dominio_settings(self):
        assert settings._DOMINIO == \
               "http://www.inmet.gov.br/projetos/rede/pesquisa/"

    def test_filter(self):
        filter = "&mRelEstacao={estacao}&btnProcesso=serie" \
                 "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"
        assert settings._FILTER == filter

    def test_url_index(self):
        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php"
        assert settings.URL_INDEX == url

    def test__url_base_diarios_horarios(self):
        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
              "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
              "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"
        assert settings._URL_BASE_DIARIOS_HORARIOS == url

    def test_url_dados_diarios(self):
        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
              "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
              "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
              "&mAtributos=,,1,1,,,,,,1,1,,1,1,1,1,"
        assert settings.URL_DADOS_DIARIOS == url

    def url_dados_horarios(self):
        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
              "gera_serie_txt.php?&mRelEstacao={estacao}&btnProcesso=serie" \
              "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
              "&mAtributos=1,1,,,1,1,,1,1,,,1,,,,,"
        assert settings.URL_DADOS_HORARIOS == url

    def url_dados_mensais(self):
        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/" \
              "gera_serie_txt_mensal.php?&mRelEstacao={estacao}" \
              "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
              "&btnProcesso=serie&mAtributos=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
        assert settings.URL_DADOS_DIARIOS == url

    def test_ancora(self):
        assert settings.ANCORA == "\nEstacao"

    def test_secret_key(self):
        key = "\nA\xe3\xf5\x94\xe3\xb9\xae\xdf\xeb\xf3" \
              "\x80\xf0i\xc7[\xb49D\x88\x1d\xfa\x8aR"
        assert settings.SECRET_KEY == key
