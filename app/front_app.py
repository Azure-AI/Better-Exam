from flask import Flask, render_template
from flask.helpers import url_for
import requests
import json

def send_post():
    url = "https://artronics.herokuapp.com/towermania/serveraddress"
    r = requests.get(url)
    print(r.text)
    return json.loads(r.text)['result']['ip']


def questions():

    # some JSON:
    

    x = {
        "exam":{
            "questions":[
            {
                "number":"1",
                "type":"MC",
                "text":"What is 2+2",
                "choices":[
                {
                    "letter":"A",
                    "text":"1"
                },
                {
                    "letter":"B",
                    "text":"4"
                }
                ],
                "answer":None
            },
            {
                "number":"2",
                "type":"ES",
                "text":"What is Cloud Computing?",
                "answer":None
            }
            ]
        }
        }

    # parse x:
    y = (x["exam"]["questions"])
    print(y)
    return y


app = Flask(__name__)
app.jinja_env.globals.update(send_post=send_post, questions =questions)

@app.route('/')
def root():
    return render_template('test.html')