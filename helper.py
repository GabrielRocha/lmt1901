#! -*- coding: UTF-8 -*-
from flask import session, request, redirect, url_for, send_file
from bdmep import BDMEP
from estacoes import ESTACOES
import settings


def download(query):
    if 'username' and 'password' not in session.keys():
        return redirect(url_for('index'))
    bdmep = BDMEP(session['username'], session['password'])
    temp = bdmep.generate_xls(request.form['estacao'],
                              request.form['data_inicio'],
                              request.form['data_fim'],
                              settings.__getattribute__(query))
    file_name = "{}_{}_{}_{}.xls".format(ESTACOES.get(request.form['estacao'], "").replace(" ","_"),
                                         request.form['data_inicio'].replace("/", ""),
                                         request.form['data_fim'].replace("/", ""),
                                         query.replace("URL_DADOS_", ""))
    return send_file(temp.filename, as_attachment=True,
                     attachment_filename=file_name)
