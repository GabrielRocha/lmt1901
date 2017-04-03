#! -*- coding: UTF-8 -*-
from unicodedata import normalize
import tempfile
import xlsxwriter
import re


def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')


def normalize_string(string):
    return re.sub("(\\r|\\n|  |\*)", "", string)


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
