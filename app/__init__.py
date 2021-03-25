from flask import Flask
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config.from_pyfile("config.py")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print("ERR: instance path does not exist \n {}".format(OSError))

    @app.route('/', methods=['GET'])
    def hello():
        return app.send_static_file('index.html')

    from . import exam
    app.register_blueprint(exam.bp)

    return app
