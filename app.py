#! -*- coding: UTF-8 -*-
from core.validates import login_required, already_loged_redirect_bdmeptoxls
from core.app_helper import dados_mensais, dados_diarios, dados_horarios
from core.helper import remover_acentos
from core.estacoes import ESTACOES
from cptec import CPTECCrawler
from datetime import date
import json
import os
import flask
import xlrd
import settings

app = flask.Flask(__name__, static_url_path="")
app.secret_key = settings.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
@already_loged_redirect_bdmeptoxls
def index():
    context = dict()
    if flask.request.method == "POST":
        user = flask.request.form['username']
        password = flask.request.form['password']
        if not(user and password):
            error = "Usuário e Senha são obrigatórios".decode('utf-8')
            context['error'] = error
        else:
            flask.session['username'] = flask.request.form['username']
            flask.session['password'] = flask.request.form['password']
            return flask.redirect("/bdmeptoxls")
    return flask.render_template("index.html", **context)


@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect("/")


@app.route("/bdmeptoxls")
@login_required
def bdmeptoxls():
    context = dict(estacoes=sorted(ESTACOES.items()))
    return flask.render_template("bdmeptoxls.html", **context)


@app.route("/download/horarios", methods=['POST'])
def download_horarios():
    return dados_horarios(flask.request)


@app.route("/download/diarios", methods=['POST'])
def download_diarios():
    return dados_diarios(flask.request)


@app.route("/download/mensal", methods=['POST'])
def download_mensal():
    return dados_mensais(flask.request)


@app.route("/recomendacao", methods=['GET'])
def recomendacao():
    return flask.render_template("recomendacao.html")


@app.route("/celsius_to_fahrenheit")
def celsius_to_fahrenheit():
    return flask.render_template("celsius_to_fahrenheit.html")


@app.route("/cptec", methods=['GET', 'POST'])
def cptec():
    if flask.request.method == "POST":
        cidade = remover_acentos(flask.request.form['cidade'].encode("utf-8"))
        if flask.request.form.get('url', None):
            cptec = CPTECCrawler(url=flask.request.form.get('url'))
        else:
            cptec = CPTECCrawler(cidade)
        try:
            tmp = cptec.get_xls()
            cidade = cidade.upper().replace(" ", "_")
            data = date.today().strftime("%d_%m_%Y")
            file_name = "CPTEC_{}_{}.xls".format(cidade, data)
            return flask.send_file(tmp.filename, as_attachment=True,
                                   attachment_filename=file_name)
        except:
            context = cptec.show_cidades_validas()
            return flask.render_template("cptec.html", **context)
    return flask.render_template("cptec.html")


@app.route("/normais/json")
def normais_json():
    xls_file = "dados/Precipitacao-Acumulada_NCB_1961-1990.xls"
    xls = xlrd.open_workbook(xls_file).sheet_by_index(0)
    normais = list()
    for number_row in range(1, xls.nrows):
        value_xls = xls.row_values(number_row)
        normais.append(value_xls)
    return json.dumps(dict(data=normais))


@app.route("/normais")
def normais():
    xls_file = "dados/Precipitacao-Acumulada_NCB_1961-1990.xls"
    xls = xlrd.open_workbook(xls_file).sheet_by_index(0)
    keys = [key for key in xls.row_values(0)]
    context = dict(columns=keys)
    return flask.render_template("normais.html", **context)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return flask.render_template('status_code/404.html'), 404


@app.errorhandler(500)
def page_error(e):
    return flask.render_template('status_code/500.html'), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
