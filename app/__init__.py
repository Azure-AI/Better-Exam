from flask import Flask
import os
import secrets
import shutil
from datetime import date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='hi',
        S2T_KEY='',
    )
    app.config.from_pyfile("config.py")
    # try:
    #     os.makedirs(app.instance_path)
    # except Exception as e:
    #     print("ERR: instance path does not exist \n {}".format(e))

    @app.route('/', methods=['GET'])
    def hello():
        return app.send_static_file('index.html')

    # This api is used for generating unique tokens for user to support multiple users at a time
    # Client must send this token in every request header named "token-id"
    @app.route('/gettoken', methods=['GET'])
    def settoken():
        token = secrets.token_urlsafe(10)
        session[str(token)] = date.today()
        return token

    # This api is used for deleting a user session. It deletes the in static/users and the token
    @app.route('/poptoken', methods=['GET'])
    def poptoken():
        shutil.rmtree("app/static/users/"+request.headers["token-id"])
        session.pop(request.headers["token-id"], None)
        print(session)
        return "Session Deleted"

    from . import exam
    app.register_blueprint(exam.bp)

    return app
