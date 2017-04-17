from bdmep import BDMEP
from core.estacoes import ESTACOES
from core.validates import login_required
from functools import partial
import json
import flask
import xlrd
import settings


@login_required
def download_dados_query(query, period ,form):
    bdmep = BDMEP(flask.session['username'], flask.session['password'])
    temp = bdmep.get_xls(form['estacao'],
                         form['data_inicio'],
                         form['data_fim'],
                         query)
    estacao = ESTACOES.get(form['estacao'], "").replace(" ", "_")
    data_inicio = form['data_inicio'].replace("/", "")
    data_fim = form['data_fim'].replace("/", "")
    file_name = "{}_{}_{}_{}.xls".format(estacao,
                                         data_inicio,
                                         data_fim,
                                         period)
    return flask.send_file(temp.filename, as_attachment=True,
                           attachment_filename=file_name)


dados_mensais = partial(download_dados_query, settings.URL_DADOS_MENSAIS, "MENSAIS")
dados_diarios = partial(download_dados_query, settings.URL_DADOS_DIARIOS, "DIARIOS")
dados_horarios = partial(download_dados_query, settings.URL_DADOS_HORARIOS, "HORARIOS")


def xls_to_json(xls_file):
    xls = xlrd.open_workbook(xls_file).sheet_by_index(0)
    normais = list()
    for number_row in range(1, xls.nrows):
        value_xls = [number_row]
        value_xls += xls.row_values(number_row)
        normais.append(value_xls)
    return json.dumps(dict(data=normais))
