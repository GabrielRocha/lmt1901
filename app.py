#! -*- coding: UTF-8 -*-
import flask
from datetime import date
from estacoes import ESTACOES
from bdmep import BDMEP
from cptec import CPTECCrawler
from helper import remover_acentos
import settings
import os


app = flask.Flask(__name__, static_url_path="")
app.secret_key = settings.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
def index():
    pass_user_in_session = 'username' and 'password' in flask.session
    get_validate = flask.request.method == "GET" and pass_user_in_session
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
            return flask.redirect(flask.url_for("bdmeptoxls"))
    if get_validate:
        return flask.redirect("bdmeptoxls")
    flask.session.clear()
    return flask.render_template("index.html", **context)


@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))


@app.route("/bdmeptoxls")
def bdmeptoxls():
    pass_user_in_session = 'username' and 'password' in flask.session
    get_validate = flask.request.method == "GET" and pass_user_in_session
    if get_validate:
        return flask.redirect(flask.url_for('index'))
    context = dict(estacoes=sorted(ESTACOES.items()))
    return flask.render_template("bdmeptoxls.html", **context)


@app.route("/download/horarios", methods=['POST'])
def download_horarios():
    return download_dados_query("URL_DADOS_HORARIOS")


@app.route("/download/diarios", methods=['POST'])
def download_diarios():
    return download_dados_query("URL_DADOS_DIARIOS")


@app.route("/download/mensal", methods=['POST'])
def download_mensal():
    return download_dados_query("URL_DADOS_MENSAIS")


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


@app.route("/normais")
def normais():
    return flask.render_template("normais.html")


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return flask.render_template('status_code/404.html'), 404


@app.errorhandler(500)
def page_error(e):
    return flask.render_template('status_code/500.html'), 500


def download_dados_query(query):
    if 'username' and 'password' not in flask.session.keys():
        return flask.redirect(flask.url_for('index'))
    bdmep = BDMEP(flask.session['username'], flask.session['password'])
    temp = bdmep.get_xls(flask.request.form['estacao'],
                         flask.request.form['data_inicio'],
                         flask.request.form['data_fim'],
                         settings.__getattribute__(query))
    estacao = ESTACOES.get(flask.request.form['estacao'], "").replace(" ", "_")
    data_inicio = flask.request.form['data_inicio'].replace("/", "")
    data_fim = flask.request.form['data_fim'].replace("/", "")
    file_name = "{}_{}_{}_{}.xls".format(estacao,
                                         data_inicio,
                                         data_fim,
                                         query.replace("URL_DADOS_", ""))
    return flask.send_file(temp.filename, as_attachment=True,
                           attachment_filename=file_name)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
