from os import name
import app

app = app.create_app()

if name == '__main__':
    app.run(host='0.0.0.0')