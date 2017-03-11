#! -*- coding: UTF-8 -*-

LOGIN = {"mCod": "",
         "mSenha": "",
         "mGerModulo": "PES",
         "btnProcesso": "+Acessar+",
         "mUsuario": ""}

_DOMINIO = "http://www.inmet.gov.br/projetos/rede/pesquisa/"

_FILTER = "&mRelEstacao={estacao}&btnProcesso=serie&mRelDtInicio={data_inicio}&mRelDtFim={data_fim}"

URL_INDEX = _DOMINIO + "inicio.php"

_URL_BASE_DIARIOS_HORARIOS = _DOMINIO + "gera_serie_txt.php?" + _FILTER

URL_DADOS_DIARIOS = _URL_BASE_DIARIOS_HORARIOS + "&mAtributos=,,1,1,,,,,,1,1,,1,1,1,1,"

URL_DADOS_HORARIOS = _URL_BASE_DIARIOS_HORARIOS + "&mAtributos=1,1,,,1,1,,1,1,,,1,,,,,"

URL_DADOS_MENSAIS = _DOMINIO + "gera_serie_txt_mensal.php?" + _FILTER + "&mAtributos=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"

ANCORA = "\nEstacao"

SECRET_KEY = '\nA\xe3\xf5\x94\xe3\xb9\xae\xdf\xeb\xf3\x80\xf0i\xc7[\xb49D\x88\x1d\xfa\x8aR'
