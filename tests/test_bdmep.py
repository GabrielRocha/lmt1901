#! -*- coding: UTF-8 -*-
from bdmep import BDMEP, LOGIN
from .xls import compare_xls
import settings
import pytest
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def dados():
    return BDMEP("user", "pass")


def test_init_bdmep_instance():
    BDMEP("user1", "pass1")
    assert LOGIN['mUsuario'] and LOGIN['mCod'] == "user1"
    assert LOGIN['mSenha'] == "pass1"


def test_get_dados_horario_inexistente(dados):
    with pytest.raises(ValueError) as error:
        dados.get_dados("83695", "01/01/2017", "01/01/2016",
                        settings.URL_DADOS_HORARIOS)
    assert "Dados Não encontrados" in str(error.value)


def test_get_dados_horario(dados):
    assert dados.get_dados("83695", "01/01/2016", "01/01/2016",
                            settings.URL_DADOS_HORARIOS) == \
           open(BASE_DIR+"/dados/horarios.txt").read().split("\n")


def test_get_dados_diarios_inexistente(dados):
    with pytest.raises(ValueError) as error:
        dados.get_dados("83695", "01/01/2017", "01/01/2016",
                        settings.URL_DADOS_DIARIOS)
    assert "Dados Não encontrados" in str(error.value)


def test_get_dados_diarios(dados):
    assert dados.get_dados("83695", "01/01/2016", "01/01/2016",
                           settings.URL_DADOS_DIARIOS) == \
           open(BASE_DIR+"/dados/diarios.txt").read().split("\n")


def test_get_dados_mensais_inexistente(dados):
    with pytest.raises(ValueError) as error:
        dados.get_dados("83695", "01/01/2016", "01/01/2016",
                        settings.URL_DADOS_MENSAIS)
    assert "Dados Não encontrados" in str(error.value)


def test_get_dados_mensais(dados):
    assert dados.get_dados("83695", "01/01/2016", "01/02/2016",
                           settings.URL_DADOS_MENSAIS) == \
           open(BASE_DIR+"/dados/mensais.txt").read().split("\n")


def test_generate_xls_horarios(dados):
    xls = dados.get_xls("83695", "01/01/2016", "01/01/2016",
                        settings.URL_DADOS_HORARIOS)
    compare_xls(xls.filename, BASE_DIR+"/dados/horarios.xls")


def test_generate_xls_diarios(dados):
    xls = dados.get_xls("83695", "01/01/2016", "01/01/2016",
                        settings.URL_DADOS_DIARIOS)
    compare_xls(xls.filename, BASE_DIR+"/dados/diarios.xls")


def test_generate_xls_mensais(dados):
    xls = dados.get_xls("83695", "01/01/2016", "01/02/2016",
                        settings.URL_DADOS_MENSAIS)
    compare_xls(xls.filename, BASE_DIR+"/dados/mensais.xls")
