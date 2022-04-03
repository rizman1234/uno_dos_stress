import requests
import os
import json

from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def landingPage():
    return render_template('create_account.html')


if __name__ == "__main__":
    app.run(debug=True, host="localhost")