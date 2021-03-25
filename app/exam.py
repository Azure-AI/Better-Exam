import simplejson as json
import app.schema as sc
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_expects_json import expects_json

bp = Blueprint('exam', __name__, url_prefix='/exam')


@bp.route('init', methods=["POST"])
@expects_json(sc.EXAM_SCHEMA)
def init_exam():
    print(request.json)
    return json.dumps({"number": "1", "audio": "/PATH/TO/AUDIO/IN/STATIC/DIRECTORY"})

def text_to_speech(question_type):
    pass

def long_answer_question_xml(question_list):
    return xml_list