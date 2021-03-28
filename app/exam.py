import time
import simplejson as json
import app.schema as sc
import os
import time
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.platypus import SimpleDocTemplate

from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flask_expects_json import expects_json

bp = Blueprint('exam', __name__, url_prefix='/exam')


# Initializing exam:
# 1. Get the JSON from client or Processed results of Form Recognizer (schema is available in app/schema.py)
# 2. Create folder for user with the value in the token-id header
# 3. Save request.json (json of the exam) in the folder as exam_json.json
# 4. Categorize question into: Essay(ES), Multiple Choice(MC)
# 5. Get audio for all questions and save it in app/static/users/<TOKEN>/audio
# 6. Name audio files based on question number in the exam
@bp.route('init', methods=["POST"])
@expects_json(sc.EXAM_SCHEMA)
def init_exam():
    os.makedirs("app/static/users/"+request.headers["token-id"])
    with open('app/static/users/'+request.headers["token-id"]+'/'+'exam_json.json', 'w') as f:
        json.dump(request.json, f)
    #es_question_xml()
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
    speak = ET.Element('speak')
    voice = ET.SubElement(speak, 'voice')
    speak.set('version', '1.0')
    speak.set('xmlns', 'https://www.w3.org/2001/10/synthesis')
    speak.set('xml:lang', 'en-US')
    voice.set('name', "en-GB-George-Apollo")
    voice.text = 'When you\'re on the motorway, it\'s a good idea to use a sat-nav.'
    question_string = ET.tostring(speak, encoding='unicode', method='xml')
    print(type(question_string))
    speech_config = SpeechConfig(endpoint="https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken")
    speech_config.authorization_token = "2a32fa5f2c504b34bd6ba61d496fed6f"
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.speak_ssml_async(question_string).get()

    stream = AudioDataStream(result)
    stream.save_to_wav_file("./app/static/audio/test.wav")


# Process answer of a question:
# 1. Get the audio file and save it in app/uploads
# 2. Call speech_recognize_continuous_from_file() for Speech to Text
# 3. Remove the audio file from uploads folder
# 4. Save answer in the JSON dedicated to this user
#todo get answer audio and question number from client and add the answer to the exam json
@bp.route('answer', methods=["POST"])
def answer():
    f = request.files['file']
    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    time.sleep(0.5)
    answer_text = speech_recognize_continuous_from_file(
        os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return answer_text


def speech_recognize_continuous_from_file(filename):
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f", region="westeurope")
    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    all_results = ""

    def handle_final_result(evt):
        nonlocal all_results
        all_results += evt.result.text

    speech_recognizer.recognized.connect(handle_final_result)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    return all_results
    # </SpeechContinuousRecognitionWithFile>


# Get audio file for a specific question (User's state like current question is handled on client side):
# 1. Receive question number as parameter in the url --> qnumber
# 2. Return the corresponding audio file from app/static/audio
@bp.route('question', methods=["GET"])
def question():
    args = request.args
    try:
        return current_app.send_static_file('./users/' + request.headers["token-id"] + '/audio/' + args["qnumber"] + '.wav')
    except Exception as e:
        return "file not found", 404

@bp.route('terminate', methods=["GET"])
def terminate():
    token = request.headers["token-id"]
    f = open('app/static/users/'+token+'/'+'exam_json.json')
    exam_json = json.load(f)
    json_to_pdf(exam_json, token)
    return current_app.send_static_file('./users/' + token + '/' + 'report.pdf')


def json_to_pdf(exam_json, token):
    report = SimpleDocTemplate("app/static/users/"+token+"/"+"report.pdf")
    styles = getSampleStyleSheet()
    doc_paragraphs = []
    for question in exam_json["exam"]["questions"]:
        doc_paragraphs.append(Paragraph(question["number"]+". "+question["text"], styles["Normal"]))
    report.build(doc_paragraphs)
    return ""


