import simplejson as json
import app.schema as sc
from xml.dom import minidom
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_expects_json import expects_json

bp = Blueprint('exam', __name__, url_prefix='/exam')


@bp.route('init', methods=["POST"])
@expects_json(sc.EXAM_SCHEMA)
def init_exam():
    # print(request.json)
    es_question_xml()
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
    questions = questions_json['exam']['questions']
    es_questions = []
    ma_questions = []
    for question in questions:
        if question['type'] == 'ES':
            es_questions.append(question)
        elif question['type'] == 'MA':
            ma_questions.append(question)
    return es_questions, ma_questions


def es_question_xml():
    speech_config = SpeechConfig(endpoint="https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken")
    speech_config.authorization_token = "2a32fa5f2c504b34bd6ba61d496fed6f"
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    ssml_string = "<speak version=\"1.0\" xmlns=\"https://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\"> <voice name=\"en-GB-George-Apollo\"> When you're on the motorway, it's a good idea to use a sat-nav.</voice> </speak>"
    result = synthesizer.speak_ssml_async(ssml_string).get()

    stream = AudioDataStream(result)
    stream.save_to_wav_file("./app/static/audio/test.wav")


@bp.route('answer', methods=["POST"])
def answer():
    pass
