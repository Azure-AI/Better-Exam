import simplejson as json
import app.schema as sc
import os
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

    speak = ET.Element('speak')
    voice = ET.SubElement(speak, 'voice')
    speak.set('version','1.0')
    speak.set('xmlns','https://www.w3.org/2001/10/synthesis')
    speak.set('xml:lang','en-US')
    voice.set('name',"en-GB-George-Apollo")
    voice.text = 'When you\'re on the motorway, it\'s a good idea to use a sat-nav.'
    question_string = ET.tostring(speak,encoding='unicode', method='xml')
    print(type(question_string))
    speech_config = SpeechConfig(endpoint="https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken")
    speech_config.authorization_token = "2a32fa5f2c504b34bd6ba61d496fed6f"
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    
    result = synthesizer.speak_ssml_async(question_string).get()
    
    stream = AudioDataStream(result)
    stream.save_to_wav_file("./app/static/audio/test.wav")


@bp.route('answer', methods=["POST"])
def answer():
    f = request.files['file']
    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    speech_config = speechsdk.SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f", region="westeurope")
    speech_config.speech_recognition_language = "en-US"
    audio_input = speechsdk.AudioConfig(filename="app/uploads/test1.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return result.text
