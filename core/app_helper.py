import json

import flask
import xlrd

import settings
from bdmep import BDMEP
from core.estacoes import ESTACOES
from core.validates import login_required


@login_required
def download_dados_query(query, request):
    bdmep = BDMEP(flask.session['username'], flask.session['password'])
    temp = bdmep.get_xls(request.form['estacao'],
                         request.form['data_inicio'],
                         request.form['data_fim'],
                         settings.__getattribute__(query))
    estacao = ESTACOES.get(request.form['estacao'], "").replace(" ", "_")
    data_inicio = request.form['data_inicio'].replace("/", "")
    data_fim = request.form['data_fim'].replace("/", "")
    file_name = "{}_{}_{}_{}.xls".format(estacao,
                                         data_inicio,
                                         data_fim,
                                         query.replace("URL_DADOS_", ""))
    return flask.send_file(temp.filename, as_attachment=True,
                           attachment_filename=file_name)


def partial(funcao, query):
    def aux_func(request):
        return funcao(query, request)
    return aux_func

dados_mensais = partial(download_dados_query, "URL_DADOS_MENSAIS")
dados_diarios = partial(download_dados_query, "URL_DADOS_DIARIOS")
dados_horarios = partial(download_dados_query, "URL_DADOS_HORARIOS")


def xls_to_json(xls_file):
    xls = xlrd.open_workbook(xls_file).sheet_by_index(0)
    normais = list()
    for number_row in range(1, xls.nrows):
        value_xls = xls.row_values(number_row)
        normais.append(value_xls)
    return json.dumps(dict(data=normais))
