#! -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from core.helper import build_xls, remover_acentos, normalize_string
import requests
import re


class CPTECCrawler:

    def __init__(self, cidade=None, url=None):
        session = requests.Session()
        if not url:
            self.html_cptec = session.post("http://www.cptec.inpe.br/cidades/previsao.do",
                                           data=dict(parameter="listar2", name=cidade)).text
        else:
            self.html_cptec = session.get("http://www.cptec.inpe.br/{}".format(url)).text
        self.parsed_html = BeautifulSoup(self.html_cptec, "html.parser")
        self.root_content = self.parsed_html.find("div", {"class": "meio_esquerda"})

    def _get_elements(self, content, elements_number):
        divs = "c"+" c".join(map(str,range(elements_number[0], elements_number[1])))
        group = list()
        for div in divs.split():
            text_div = content.find("div", {"class": div})
            if text_div and text_div.find("b"):
                value = normalize_string(" ".join(text_div.find("b").strings))
                key = remover_acentos(normalize_string(text_div.text.replace(text_div.find("b").text,""))
                                      .encode('utf-8'))
            else:
                key = "None"
                value = text_div.text
            group += [(key.strip(), value)]
        return group

    def _get_uv_max(self, content):
        src_img = content.find("img").attrs['src']
        return re.split("uv_", src_img)[-1].replace(".gif", "")

    @property
    def condicoes_atuais(self):
        try:
            condicao_atual = self.root_content.find("div", {"class":"cond"})
            if not condicao_atual:
                iuv_max = self.root_content.find("div", {"class": "dados"})
                dados = [('IUV MAXIMO', "%s - %s" %(self._get_uv_max(iuv_max), " ".join(iuv_max.strings)))]
            else:
                dados = self._get_elements(condicao_atual, (2,7))
                dados += [('CONDICAO', self._get_elements(condicao_atual, (7,8))[0][-1])]
                iuv_max = self.root_content.find("div", {"class": "induv"})
                dados += [('IUV MAXIMO', "%s - %s" %(self._get_uv_max(iuv_max), " ".join(iuv_max.strings)))]
            return [dados]
        except:
            raise ValueError("Dados Não encontrados")

    @property
    def previsoes(self):
        try:
            dados = list()
            previsoes = self.root_content.find_all("div", {"class":"previsao"})
            for previsao in previsoes:
                dados.append([("DATA", previsao.find("div", {"class": "tit"}).text.strip())])
                dados[-1] += self._get_elements(previsao, (2,7))
                dados[-1] += [('CONDICAO', self._get_elements(previsao, (8,9))[0][-1])]
                dados[-1] += [('IUV MAXIMO', self._get_uv_max(previsao.find("div", {"class": "c7"})))]
            return dados
        except:
            raise ValueError("Dados Não encontrados")

    def show_cidades_validas(self):
        try:
            cidades = self.parsed_html.find("div", {"class": "cont_inferior"}).find_all("li")
            dict_cidades = list()
            for cidade in cidades:
                sugestao = cidade.find("a")
                dict_cidades.append([normalize_string(sugestao.text), normalize_string(sugestao.attrs['href'])])
            return dict(cidades=dict_cidades)
        except:
            return dict(error="Nenhuma cidade foi encontrada. Tente novamente!")

    def _to_list(self, group):
        header = [key for key, _ in group[0]]
        content = [[value for _, value in items] for items in group]
        return [header] + content

    def condicoes_atuais_list(self):
        return self._to_list(self.condicoes_atuais)

    def previsoes_list(self):
        return self._to_list(self.previsoes)

    def get_xls(self):
        return build_xls(self.condicoes_atuais_list()+[[]]+self.previsoes_list())
