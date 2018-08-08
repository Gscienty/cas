from flask import Flask

APP_NAME = 'cas'

app = Flask(APP_NAME)
app.config.from_pyfile('config.cfg')