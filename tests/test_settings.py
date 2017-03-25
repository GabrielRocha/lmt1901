#! -*- Coding: UTF-8 -*-
import settings


class TestCaseSettings():

    def test_mCod_key_in_LOGIN(self):
        assert "mCod" in settings.LOGIN.keys()

    def test_mSenha_key_in_LOGIN(self):
        assert "mSenha" in settings.LOGIN.keys()

    def test_mGerModulo_key_in_LOGIN(self):
        assert "mGerModulo" in settings.LOGIN.keys()

    def test_btnProcesso_key_in_LOGIN(self):
        assert "btnProcesso" in settings.LOGIN.keys()

    def test_mUsuario_key_in_LOGIN(self):
        assert "mUsuario" in settings.LOGIN.keys()

    def test_LOGIN_is_dict(self):
        assert type(settings.LOGIN) is dict

    def test_total_LOGIN_keys(self):
        assert len(settings.LOGIN) == 5

    def test__DOMINIO_settings(self):
        assert settings._DOMINIO == "http://www.inmet.gov.br/projetos/rede/pesquisa/"

    def test_FILTER(self):
        assert settings._FILTER == "&mRelEstacao={estacao}&btnProcesso=serie&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"

    def test_URL_INDEX(self):
        assert settings.URL_INDEX == "http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php"

    def test__URL_BASE_DIARIOS_HORARIOS(self):
        assert settings._URL_BASE_DIARIOS_HORARIOS == "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php" \
                                                      "?&mRelEstacao={estacao}&btnProcesso=serie" \
                                                      "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"

    def test_URL_DADOS_DIARIOS(self):
        assert settings.URL_DADOS_DIARIOS == "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php" \
                                             "?&mRelEstacao={estacao}&btnProcesso=serie" \
                                             "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
                                             "&mAtributos=,,1,1,,,,,,1,1,,1,1,1,1,"

    def URL_DADOS_HORARIOS(self):
        assert settings.URL_DADOS_HORARIOS == "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php" \
                                             "?&mRelEstacao={estacao}&btnProcesso=serie" \
                                             "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
                                             "&mAtributos=1,1,,,1,1,,1,1,,,1,,,,,"

    def URL_DADOS_MENSAIS(self):
        assert settings.URL_DADOS_DIARIOS == "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt_mensal.php?" \
                                             "?&mRelEstacao={estacao}&btnProcesso=serie" \
                                             "&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}" \
                                             "&mAtributos=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"

    def test_ancora(self):
        assert settings.ANCORA == "\nEstacao"

    def test_SECRET_KEY(self):
        assert settings.SECRET_KEY == "\nA\xe3\xf5\x94\xe3\xb9\xae\xdf\xeb\xf3\x80\xf0i\xc7[\xb49D\x88\x1d\xfa\x8aR"
