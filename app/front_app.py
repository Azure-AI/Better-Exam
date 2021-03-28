from flask import Flask, render_template
from flask.helpers import url_for
import requests
import json

def send_post():
    url = "https://artronics.herokuapp.com/towermania/serveraddress"
    r = requests.get(url)
    print(r.text)
    return json.loads(r.text)['result']['ip']


def test():
    names = ['Ali', 'Faezeh', 'Arman', 'Afshin']
    return names


app = Flask(__name__)
app.jinja_env.globals.update(send_post=send_post, names =test)

@app.route('/')
def root():
    return render_template('test.html')


@app.route('/hammer')
def hammer():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')