#! -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for, send_file
from estacoes import ESTACOES
from bdmep import BDMEP
import settings
import os


app = Flask(__name__, static_url_path="")
app.secret_key = settings.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
def index():
    get_validate = request.method == "GET" and 'username' and 'password' in session
    context = dict()
    if request.method == "POST":
        if not(request.form['username'] and request.form['password']):
            context['error'] = "Usuário e Senha são obrigatórios".decode('utf-8')
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for("bdmeptoxls"))
    if get_validate:
        return redirect("bdmeptoxls")
    session.clear()
    return render_template("index.html", **context)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/bdmeptoxls")
def bdmeptoxls():
    get_validate = request.method == "GET" and 'username' and 'password' not in session.keys()
    if get_validate:
        return redirect(url_for('index'))
    context = dict(estacoes=sorted(ESTACOES.items()))
    return render_template("bdmeptoxls.html", **context)


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
    return render_template("recomendacao.html")


@app.route("/celsius_to_fahrenheit")
def celsius_to_fahrenheit():
    return render_template("celsius_to_fahrenheit.html")


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template('status_code/404.html'), 404


@app.errorhandler(500)
def page_error(e):
    return render_template('status_code/500.html'), 500


def download_dados_query(query):
    if 'username' and 'password' not in session.keys():
        return redirect(url_for('index'))
    bdmep = BDMEP(session['username'], session['password'])
    temp = bdmep.get_xls(request.form['estacao'],
                              request.form['data_inicio'],
                              request.form['data_fim'],
                              settings.__getattribute__(query))
    file_name = "{}_{}_{}_{}.xls".format(ESTACOES.get(request.form['estacao'], "").replace(" ","_"),
                                         request.form['data_inicio'].replace("/", ""),
                                         request.form['data_fim'].replace("/", ""),
                                         query.replace("URL_DADOS_", ""))
    return send_file(temp.filename, as_attachment=True,
                     attachment_filename=file_name)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
