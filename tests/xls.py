from itertools import izip_longest
import xlrd


def compare_xls(xls, xls_base):
    sheet1 = xlrd.open_workbook(xls).sheet_by_index(0)
    sheet2 = xlrd.open_workbook(xls_base).sheet_by_index(0)
    assert sheet2.nrows == sheet1.nrows
    for rownum in range(max(sheet1.nrows, sheet2.nrows)):
        row_rb1 = sheet1.row_values(rownum)
        row_rb2 = sheet2.row_values(rownum)
        for _, (c1, c2) in enumerate(izip_longest(row_rb1, row_rb2)):
            assert c1 == c2