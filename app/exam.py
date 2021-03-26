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

# Parses the questions. Creates an audio file for each of them
def text_to_speech(questions_json):
    question_parser(questions_json)
    long_answer_question_xml()
    pass

# Gets the long answer questions in the form of a dict. Creates an audio file for each of them
def long_answer_question_xml(long_questions):
    questions = json.loads(long_questions)
    pass

# Gets the whole questions' JSON as input. Seperates the questions based on their type into dicts
def question_parser(questions_json):
    questions = json.loads(questions_json)['exam']['questions']
    es_questions = []
    ma_questions = []
    for question in questions:
        if question['type']=='ES':
            es_questions.append(question)
        elif question['type']=='MA':
            ma_questions.append(question)
    return es_questions,ma_questions