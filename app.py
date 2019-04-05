from flask import Flask, render_template, request
import requests


application = Flask('glo2005_projet')


@application.route('/')
def index():
    return render_template('index.html')

application.run('0.0.0.0',8080)