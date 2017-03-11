#! -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from settings import LOGIN, URL_INDEX, ANCORA
import requests
import xlsxwriter
import tempfile


class BDMEP():
    def __init__(self, user, password):
        self.session = requests.Session()
        LOGIN['mUsuario'] = user
        LOGIN['mCod'] = user
        LOGIN['mSenha'] = password
        self.login()

    def set_cookie(self, name_cookie, value_cookie):
        self.session.cookies.clear()
        self.session.cookies.set(name_cookie, value_cookie)

    def login(self):
        self.session.cookies.clear()
        self.session.get(url=URL_INDEX)
        self.session.post(url=URL_INDEX, data=LOGIN, cookies=self.session.cookies.get_dict())

    def get_dados(self, estacao, data_inicio, data_fim, query):
        query = query.format(estacao=estacao, data_inicio=data_inicio, data_fim=data_fim)
        html = BeautifulSoup(self.session.get(url=query).text, "html.parser")
        tag_pre_html = html.find("pre").text
        index_ancora = tag_pre_html.find(ANCORA)
        if index_ancora:
            return tag_pre_html[index_ancora:].replace(".", ",").split("\n")
        raise ValueError("Dados Não encontrados")

    def generate_xls(self, estacao, data_inicio, data_fim, query):
        dados = self.get_dados(estacao, data_inicio, data_fim, query)
        handle, filepath = tempfile.mkstemp()
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        for row_number, row_value in enumerate(dados):
            columns = row_value.split(";")
            for column_number, column_value in enumerate(columns):
                worksheet.write(row_number, column_number, column_value)
        workbook.close()
        return workbook
