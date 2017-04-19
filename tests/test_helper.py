#! -*- coding: UTF-8 -*-
from .xls import compare_xls
from core import helper
import xlrd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def test_remover_acentos():
    assert helper.remover_acentos("ÁBÇÃO") == "ABCAO"

def test_normalize_string():
    string = "Teste\r  \n\r\nTeste **\n"
    assert helper.normalize_string(string) == "TesteTeste "

def test_build_xls_list():
    dados = [[1,2,3,4],[5,6,7,8]]
    xls = helper.build_xls(dados)
    compare_xls(xls.filename, BASE_DIR+"/dados/build.xls")

def _create_sheet():
    dados = ["1;2;3;4","5;6;7;8"]
    xls = helper.build_xls(dados)
    return xlrd.open_workbook(xls.filename).sheet_by_index(0)

def test_size_build_xls_csv_with_semicolon():
    sheet = _create_sheet()
    assert sheet.nrows == 2

def test_first_row_build_xls_csv_with_semicolon():
    sheet = _create_sheet()
    assert sheet.row_values(0) == ['1','2','3','4']

def test_second_row_build_xls_csv_with_semicolon():
    sheet = _create_sheet()
    assert sheet.row_values(1) == ['5','6','7','8']
