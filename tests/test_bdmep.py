#! -*- coding: UTF-8 -*-
from itertools import izip_longest
from bdmep import BDMEP, LOGIN
from unittest import TestCase
import settings
import pytest
import os
import xlrd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCaseBDMEP(TestCase):

    def setUp(self):
        self.dados = BDMEP("user", "pass")

    def test_init_BDMEP_instance(self):
        BDMEP("user1", "pass1")
        assert LOGIN['mUsuario'] and LOGIN['mCod'] == "user1"
        assert LOGIN['mSenha'] == "pass1"

    def test_get_dados_horario_inexistente(self):
        with pytest.raises(ValueError) as error:
            self.dados.get_dados("83695", "01/01/2017", "01/01/2016",
                                 settings.URL_DADOS_HORARIOS)
        assert "Dados Não encontrados" in str(error.value)

    def test_get_dados_horario(self):
        assert self.dados.get_dados("83695", "01/01/2016", "01/01/2016",
                                    settings.URL_DADOS_HORARIOS) == \
               open(BASE_DIR+"/dados/horarios.txt").read().split("\n")

    def test_get_dados_diarios_inexistente(self):
        with pytest.raises(ValueError) as error:
            self.dados.get_dados("83695", "01/01/2017", "01/01/2016",
                                 settings.URL_DADOS_DIARIOS)
        assert "Dados Não encontrados" in str(error.value)

    def test_get_dados_diarios(self):
        assert self.dados.get_dados("83695", "01/01/2016", "01/01/2016",
                                    settings.URL_DADOS_DIARIOS) == \
               open(BASE_DIR+"/dados/diarios.txt").read().split("\n")

    def test_get_dados_mensais_inexistente(self):
        with pytest.raises(ValueError) as error:
            self.dados.get_dados("83695", "01/01/2016", "01/01/2016",
                                 settings.URL_DADOS_MENSAIS)
        assert "Dados Não encontrados" in str(error.value)

    def test_get_dados_mensais(self):
        assert self.dados.get_dados("83695", "01/01/2016", "01/02/2016",
                                    settings.URL_DADOS_MENSAIS) == \
               open(BASE_DIR+"/dados/mensais.txt").read().split("\n")

    def test_generate_xls_horarios(self):
        xls = self.dados.get_xls("83695", "01/01/2016", "01/01/2016",
                                 settings.URL_DADOS_HORARIOS)
        self._compare_xls(xls.filename, BASE_DIR+"/dados/horarios.xls")

    def test_generate_xls_diarios(self):
        xls = self.dados.get_xls("83695", "01/01/2016", "01/01/2016",
                                 settings.URL_DADOS_DIARIOS)
        self._compare_xls(xls.filename, BASE_DIR+"/dados/diarios.xls")

    def test_generate_xls_mensais(self):
        xls = self.dados.get_xls("83695", "01/01/2016", "01/02/2016",
                                 settings.URL_DADOS_MENSAIS)
        self._compare_xls(xls.filename, BASE_DIR+"/dados/mensais.xls")

    def _compare_xls(self, xls, xls_base):
        sheet1 = xlrd.open_workbook(xls).sheet_by_index(0)
        sheet2 = xlrd.open_workbook(xls_base).sheet_by_index(0)
        assert sheet2.nrows == sheet1.nrows
        for rownum in range(max(sheet1.nrows, sheet2.nrows)):
            row_rb1 = sheet1.row_values(rownum)
            row_rb2 = sheet2.row_values(rownum)
            for colnum, (c1, c2) in enumerate(izip_longest(row_rb1, row_rb2)):
                assert c1 == c2
