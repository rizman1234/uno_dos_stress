import requests
import os
import json
import pyodbc

from dotenv import load_dotenv
from flask import Flask, render_template, session, request

load_dotenv(dotenv_path="./config.py")
app = Flask(__name__, static_url_path='/static')

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_USERNAME = os.getenv("SERVER_USERNAME")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD")

server = SERVER_NAME + '.database.windows.net'
database = 'test'
username = SERVER_USERNAME
password = SERVER_PASSWORD
driver= '{ODBC Driver 17 for SQL Server}'


@app.route('/')
def landingPage():
    return render_template('create_account.html')


@app.route('/_user_info', methods=['POST'])
def user_info():    
    data = request.get_json()
    print(data)
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("insert into [dbo].[User](first_name, last_name, email, password) values ('{}', '{}', '{}', '{}')".format(data["first_name"], data["last_name"], data["email"], data["password"]))
            conn.commit()

    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True, host="localhost")