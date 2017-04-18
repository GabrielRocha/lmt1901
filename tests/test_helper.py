#! -*- coding: UTF-8 -*-
from unittest import TestCase, main
from .xls import compare_xls
from core import helper
import xlrd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCaseHelper(TestCase):

    def test_remover_acentos(self):
        assert helper.remover_acentos("ÁBÇÃO") == "ABCAO"

    def test_normalize_string(self):
        string = "Teste\r  \n\r\nTeste **\n"
        assert helper.normalize_string(string) == "TesteTeste "

    def test_build_xls_list(self):
        dados = [[1,2,3,4],[5,6,7,8]]
        xls = helper.build_xls(dados)
        compare_xls(xls.filename, BASE_DIR+"/dados/build.xls")

    def test_build_xls_csv_with_semicolon(self):
        dados = ["1;2;3;4","5;6;7;8"]
        xls = helper.build_xls(dados)
        sheet1 = xlrd.open_workbook(xls.filename).sheet_by_index(0)
        assert sheet1.nrows == 2
        assert sheet1.row_values(0) == ['1','2','3','4']
        assert sheet1.row_values(1) == ['5','6','7','8']

if __name__ == '__main__':
    main()