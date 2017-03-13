#! -*- coding: UTF-8 -*-
from flask import Flask, send_file, render_template, request, session, redirect, url_for
from estacoes import ESTACOES
from helper import download
import settings
import os


app = Flask(__name__, static_url_path="")
app.secret_key = settings.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
def login():
    get_validate = request.method == "GET" and 'username' and 'password' in session.keys()
    context = dict()
    if request.method == "POST":
        if not(request.form['username'] and request.form['password']):
            context['error'] = "Usuário e Senha são obrigatórios"
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for("dashboard"))
    if get_validate:
        return redirect("dashboard")
    session.clear()
    return render_template("login.html", **context)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/dashboard")
def dashboard():
    get_validate = request.method == "GET" and 'username' and 'password' not in session.keys()
    if get_validate:
        return redirect(url_for('login'))
    context = dict(estacoes=sorted(ESTACOES.items()))
    return render_template("index.html", **context)


@app.route("/download/horarios", methods=['POST'])
def download_horarios():
    _file, file_name = download("URL_DADOS_HORARIOS")
    return send_file(_file.filename, as_attachment=True,
                     attachment_filename=file_name)


@app.route("/download/diarios", methods=['POST'])
def download_diarios():
    _file, file_name = download("URL_DADOS_DIARIOS")
    return send_file(_file.filename, as_attachment=True,
                     attachment_filename=file_name)


@app.route("/download/mensal", methods=['POST'])
def download_mensal():
    _file, file_name = download("URL_DADOS_MENSAIS")
    return send_file(_file.filename, as_attachment=True,
                     attachment_filename=file_name)


@app.route("/recomendacao", methods=['GET'])
def recomendacao():
    get_validate = request.method == "GET" and 'username' and 'password' not in session.keys()
    if get_validate:
        return redirect(url_for('login'))
    return render_template("recomendacao.html")


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template('status_code/404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('status_code/500.html'), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
