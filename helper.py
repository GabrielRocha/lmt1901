#! -*- coding: UTF-8 -*-
import tempfile
import xlsxwriter
from unicodedata import normalize


def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')


def build_xls(dados):
    handle, filepath = tempfile.mkstemp()
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    for row_number, row_value in enumerate(dados):
        try:
            columns = row_value.split(";")
        except:
            columns = [column for column in row_value]
        for column_number, column_value in enumerate(columns):
            worksheet.write(row_number, column_number, column_value)
    workbook.close()
    return workbook


