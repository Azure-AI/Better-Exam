import time
from azure.cognitiveservices.speech.speech_py_impl import CancellationDetails
import simplejson as json
from werkzeug.datastructures import FileStorage
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
import secrets
import shutil
from datetime import date
import qrcode
from email.message import EmailMessage
import mimetypes
import smtplib

from flask_expects_json import expects_json


exam_json = {
    "exam": {
        "questions": [{
            "number": "1",
            "type": "MC",
            "text": "What is 2+2",
            "choices": [{
                "letter": "A",
                "text": "1"
            }, {
                "letter": "B",
                "text": "4"
            }],
            "answer": None,
            "audio_link": "/static/users/kRsyQs4d3myR3A/audio/1-MC.wav"
        }, {
            "number": "2",
            "type": "ES",
            "text": "What is Cloud Computing?",
            "answer": None,
            "audio_link": "/static/users/kRsyQs4d3myR3A/audio/2-ES.wav"
        }]
    }
}

bp = Blueprint('exam', __name__, url_prefix='/exam')

@bp.route('create', methods=["POST"])
def create_exam():
    exam_json = request.json
    exam_id = secrets.token_urlsafe(5)
    os.makedirs("app/static/exams/"+exam_id,exist_ok =True)
    os.makedirs("app/static/exams/"+exam_id+"/audio",exist_ok =True)
    f = open('app/static/exams/' + exam_id + '/' + 'exam_json.json', "w")
    json.dump(exam_json, f)
    f.close()
    text_to_speech(exam_json, exam_id)
    url = 'http://localhost:5000/exam/start?id={}'.format(exam_id)
    img = qrcode.make(url)
    img.save('app/static/exams/' + exam_id + '/' + 'qr.png')
    send_mail(exam_id, url, exam_json["exam"]["email"])
    return "success", 200

def send_mail(exam_id, url, email):
    message = EmailMessage()
    sender = "better.exam.info@gmail.com"
    recipient = email
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = "Better Exam - Exam Info"
    body = "Hey there!\nThanks for using Better Exam.\nExam Link: {}".format(url)
    message.set_content(body)
    attachment_path = 'app/static/exams/' + exam_id + '/' + 'qr.png'
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(),maintype = mime_type,subtype = mime_subtype,filename = os.path.basename(attachment_path))
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.login(sender, 'B3tt3rExam')
    mail_server.send_message(message)
    mail_server.quit()
    return ""

@bp.route('/start', methods=['Get'])
def start_exam():
    exam_id = request.args["id"]
    token = get_token()
    os.makedirs("app/static/users/" + token, exist_ok=True)
    os.makedirs("app/static/users/" + token + "/audio", exist_ok=True)
    f = open('app/static/exams/' + exam_id + '/' + 'exam_json.json', "r+")
    exam_json = json.load(f)
    f.close()
    with open('app/static/users/' + token + '/exam_json.json', 'w') as f:
        json.dump(exam_json, f)
    exam_json_processed = generate_question_list(exam_json, exam_id)
    print("Token:{}\nExam:{}\n{}".format(token, exam_id, exam_json_processed))
    return render_template("index.html", token=token, exam_id=exam_id, exam_json=exam_json_processed)

# Initializing exam:
# 1. Get the JSON from client or Processed results of Form Recognizer (schema is available in app/schema.py)
# 2. Create folder for user with the value in the token-id header
# 3. Save request.json (json of the exam) in the folder as exam_json.json
# 4. Categorize question into: Essay(ES), Multiple Choice(MC)
# 5. Get audio for all questions and save it in app/static/users/<TOKEN>/audio
# 6. Name audio files based on question number in the exam
@bp.route('/init', methods=['POST'])
def init_exam(exam_json=exam_json):
    # token = request.headers['token-id']
    # os.makedirs("app/static/users/" + token, exist_ok =True)
    # os.makedirs("app/static/users/" + token + "/audio", exist_ok =True)
    # with open('app/static/users/' + token + '/exam_json.json', 'w') as f:
    #     json.dump(exam_json, f)
    print("start operation")
    #text_to_speech(exam_json, token)
    return "success"


# Parses the questions. Creates an audio file for each of them
def text_to_speech(questions_json,exam_id):
    es_list,mc_list = question_parser(questions_json)
    print(mc_list)
    es_question_audio_creation(es_list,exam_id)
    mc_question_audio_creation(mc_list,exam_id)



# Gets the long answer questions in the form of a dict. Creates an audio file for each of them
def es_question_audio_creation(long_questions,exam_id):
    for question in long_questions:
        es_question_xml(question,exam_id)

# Gets the multiple choice questions in the form of a dict. Creates an audio file for each of them
def mc_question_audio_creation(multiple_choice_questions,exam_id):
    for question in multiple_choice_questions:
        mc_question_xml(question,exam_id)


# Gets the whole questions' JSON as input. Seperates the questions based on their type into dicts
def question_parser(questions_json):
    questions = questions_json['exam']['questions']
    es_questions = []
    mc_questions = []
    for question in questions:
        if question['type'] == 'ES':
            es_questions.append(question)
        elif question['type'] == 'MC':
            mc_questions.append(question)
    return es_questions, mc_questions


def es_question_xml(question,exam_id):
    # Themp solution - might change
    ssml_string_speak = "<speak version=\"1.0\" xmlns=\"https://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">"
    ssml_string_voice = "<voice name=\"en-US-AriaNeural\">"
    ssml_string_prosody = "<prosody rate=\"0.85\">"
    ssml_string_break = "<break time=\"500ms\"/>"
    ssml_string_question_info = "Question" + question["number"]
    ssml_string_question_text =  question["text"]
    ssml_string_prosody_end = "</prosody>"
    ssml_string_voice_end = "</voice>"
    ssml_string_speak_end = "</speak>"
    ssml_message = ssml_string_speak + ssml_string_voice +ssml_string_prosody+ ssml_string_question_info + ssml_string_break + \
            ssml_string_question_text+ssml_string_prosody_end + ssml_string_voice_end + ssml_string_speak_end


    print(ssml_message)
    speech_config = SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f",region="westeurope")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(ssml_message).get()
    stream = AudioDataStream(result)
    stream.save_to_wav_file_async("./app/static/exams/"+exam_id+"/audio/"+question["number"]+"-"+question["type"]+".wav")
    print("File saved")


def mc_question_xml(question,exam_id):

    speech_config = SpeechConfig(subscription="2a32fa5f2c504b34bd6ba61d496fed6f",region="westeurope")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Temp solution - might change
    ssml_string_speak = "<speak version=\"1.0\" xmlns=\"https://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">"
    ssml_string_voice = "<voice name=\"en-US-AriaNeural\">"
    ssml_string_prosody = "<prosody rate=\"0.85\">"
    ssml_string_break = "<break time=\"500ms\"/>"
    ssml_string_question_info = "Question" + question["number"]
    ssml_string_question_text =  question["text"]
    choices = question["choices"]
    ssml_string_choices = ''
    for choice in choices:
       ssml_string_choices+= "choice" + choice["letter"] + "<break time=\"300ms\"/>" + choice["text"] + "<break time=\"300ms\"/>"
    ssml_string_prosody_end = "</prosody>"
    ssml_string_voice_end = "</voice>"
    ssml_string_speak_end = "</speak>"

    ssml_message = ssml_string_speak + ssml_string_voice + ssml_string_prosody + ssml_string_question_info + ssml_string_break + \
            ssml_string_question_text +ssml_string_break + ssml_string_choices+ ssml_string_prosody_end +ssml_string_voice_end + ssml_string_speak_end


    print(ssml_message)


    result = synthesizer.speak_ssml_async(ssml_message).get()

    stream = AudioDataStream(result)
    stream.save_to_wav_file("./app/static/exams/"+exam_id+"/audio/"+question["number"]+"-"+question["type"]+".wav")
    print("File saved")

def generate_question_list(exam_json, exam_id):
    # result = []
    for question in exam_json['exam']['questions']:
        question['audio_link'] = '/static/exams/{}/audio/{}.wav'.format(exam_id, f"{question['number']}-{question['type']}")
    
    # with open('app/static/users/' + token + '/exam_json.json', 'w') as f:
    #     json.dump(exam_json, f)
    # for file in os.listdir("app/static/users/"+token+"/audio"):
    #     question_dict = {"qnumber": "", "type": "", "audio_link": ""}
    #     question_dict["audio_link"] = "static/users/"+token+"/audio/"+file
    #     question_dict["qnumber"] = str(file).split("-")[0]
    #     question_dict["type"] = str(file).split("-")[1][:2]
    #     result.append(question_dict)
    return exam_json

# Process answer of a question:
# 1. Get the audio file and save it in app/uploads
# 2. Call speech_recognize_continuous_from_file() for Speech to Text
# 3. Remove the audio file from uploads folder
# 4. Save answer in the JSON dedicated to this user

# @app.route('/recorder', methods=["POST"])
#     def save_file():
        
#         return "File Recieved"


@bp.route('answer', methods=["POST"])
def answer_question():
    token = request.headers["token-id"]
    qnumber = int(request.form["qnumber"])
    file_name = request.form.get('fname')
    f: FileStorage = request.files.get('data')
    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file_name)))
    time.sleep(0.5)
    answer_text = speech_recognize_continuous_from_file(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
    #answer_text = "test text"
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
    f = open('app/static/users/' + token + '/' + 'exam_json.json', "r+")
    exam_json = json.load(f)
    f.close()
    if exam_json["exam"]["questions"][qnumber-1]["type"] == "MC":
        answer_text = find_choice(exam_json,answer_text,qnumber)
    exam_json["exam"]["questions"][qnumber-1]["answer"] = answer_text
    f = open('app/static/users/' + token + '/' + 'exam_json.json', "w")
    json.dump(exam_json, f)
    f.close()
    return "Success", 200
def find_choice(exam_json,answer_text,qnumber):
    pass

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
# @bp.route('question', methods=["GET"])
# def question():
#     args = request.args
#     try:
#         return current_app.send_static_file('./users/' + request.headers["token-id"] + '/audio/' + args["qnumber"] + '.wav')
#     except Exception as e:
#         return "file not found", 404

# Terminate the exam and generate the pdf
# return the pdf
@bp.route('terminate', methods=["POST"])
def terminate_exam():
    token = request.headers["token-id"]
    f = open('app/static/users/'+token+'/'+'exam_json.json')
    exam_json = json.load(f)
    json_to_pdf(exam_json, token)
    email_answers(token, exam_json)
    return "Answers were sent to the teacher"


def json_to_pdf(exam_json, token):
    report = SimpleDocTemplate("app/static/users/"+token+"/"+"report.pdf")
    styles = getSampleStyleSheet()
    doc_paragraphs = []
    for question in exam_json["exam"]["questions"]:
        doc_paragraphs.append(Paragraph(question["number"]+". "+question["text"], styles["Normal"]))
        doc_paragraphs.append(Spacer(1, 1))
        doc_paragraphs.append(Paragraph("ANSWER: "+question["answer"], styles["Normal"]))
        doc_paragraphs.append(Spacer(1, 8))
    report.build(doc_paragraphs)
    return ""
def email_answers(token, exam_json):
    message = EmailMessage()
    sender = "better.exam.info@gmail.com"
    recipient = exam_json["exam"]["email"]
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = "Better Exam - {} Answers".format(exam_json["exam"]["title"])
    body = "Hey there!\nThanks for using Better Exam.\nExam title: {}\nStudent Name: {}".format(exam_json["exam"]["title"], "NAME")
    message.set_content(body)
    attachment_path = 'app/static/users/' + token + '/' + 'report.pdf'
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype,
                               filename=os.path.basename(attachment_path))
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.login(sender, 'B3tt3rExam')
    mail_server.send_message(message)
    mail_server.quit()
    return ""

def questions():
    print('Parsing Questions')
    # get questions from exam JSON:
    return exam_json["exam"]["questions"]

def get_token():
    token = secrets.token_urlsafe(10)
    session[str(token)] = date.today()
    return token

def pop_token(token):
    shutil.rmtree("app/static/users/" + token)
    session.pop(token, None)
    print(session)
    return "Session Deleted"

jinja_globals = [questions, get_token, pop_token, init_exam, terminate_exam]
