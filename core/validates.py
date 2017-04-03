from flask import session, redirect, request
from functools import wraps


def login_required(function):
    wraps(function)

    def validade_login_required(*args, **kwargs):
        if 'username' and 'password' not in session:
            return redirect("/")
        return function(*args, **kwargs)
    return validade_login_required


def already_loged_redirect_bdmeptoxls(function):
    wraps(function)

    def validade_already_loged(*args, **kwargs):
        pass_user_in_session = 'username' and 'password' in session
        if request.method == "GET" and pass_user_in_session:
            return redirect("/bdmeptoxls")
        return function(*args, **kwargs)
    return validade_already_loged
