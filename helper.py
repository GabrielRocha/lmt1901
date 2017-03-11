from flask import session, request, redirect, url_for
from bdmep import BDMEP
from estacoes import ESTACOES
import settings


def download(query):
    if 'username' and 'password' not in session.keys():
        return redirect(url_for('login'))
    bdmep = BDMEP(session['username'], session['password'])
    temp = bdmep.generate_xls(request.form['estacao'],
                              request.form['data_inicio'],
                              request.form['data_fim'],
                              settings.__getattribute__(query))
    file_name = "{}_{}_{}_{}.xls".format(ESTACOES.get(request.form['estacao'], "").replace(" ","_"),
                                         request.form['data_inicio'].replace("/", ""),
                                         request.form['data_fim'].replace("/", ""),
                                         query.replace("URL_DADOS_", ""))
    return temp, file_name
