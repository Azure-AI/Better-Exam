from flask import Flask, render_template
from flask.helpers import url_for
import requests
import json

def send_post():
    url = "https://artronics.herokuapp.com/towermania/serveraddress"
    r = requests.get(url)
    print(r.text)
    return json.loads(r.text)['result']['ip']

names = ['Ali', 'Faezeh', 'an', 'goh']
app = Flask(__name__)
app.jinja_env.globals.update(send_post=send_post, names =names)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/hammer')
def hammer():
    return render_template('hi.html')