from flask import Flask
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='',
        S2T_KEY='',
    )
    app.config.from_pyfile("config.py")
    try:
        os.makedirs(app.instance_path)
    except Exception as e:
        print("ERR: instance path does not exist \n {}".format(e))

    @app.route('/', methods=['GET'])
    def hello():
        return app.send_static_file('index.html')

    from . import exam
    app.register_blueprint(exam.bp)

    return app
