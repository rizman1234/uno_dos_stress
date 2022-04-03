import requests
import os
import json
import pyodbc
import schedule_algo

from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for, jsonify

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
    return render_template('login.html')


@app.route('/_user_info', methods=['POST'])
def user_info():    
    data = request.get_json()
    print(data)
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("insert into [dbo].[User](first_name, last_name, email, password) values ('{}', '{}', '{}', '{}')".format(data["first_name"], data["last_name"], data["email"], data["password"]))
            conn.commit()

            cursor.execute("select user_id from [dbo].[User] where email='{}' and password='{}'".format(data["email"], data["password"]))
            user_id = cursor.fetchall()[0][0]

            cursor.execute("insert into [dbo].[Activities](user_id, activities) values ('{}', '{}')".format(user_id, data["activity"]))
            conn.commit()

            print("user_id: ")
            print(user_id)

            availablility = data["availability"]
            for i, hour in enumerate(availablility):
                for j, day in enumerate(availablility[i]):
                    if availablility[i][j]==1:
                        print(j, 8+i)
                        cursor.execute("insert into [dbo].[Schedule](user_id, day_of_week, block_time) values ('{}', '{}', '{}')".format(user_id, j, 8+i))
                        conn.commit()
    run_algo()

    return ('', 204)

def run_algo():
    return schedule_algo.main()

@app.route('/_login_info', methods=['POST'])
def login_info():    
    data = request.get_json()
    print(data)
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select count(*) from [dbo].[User] where email='{}' and password='{}'".format(data["email"], data["password"]))
            
            count = cursor.fetchall()[0][0]
        
            if count==0:
                return 'false'
            else:
                print("send")
                return jsonify({"redirect": "/edit_preferences"})

@app.route('/edit_preferences', methods=['GET','POST'])
def edit_preferences():
    return render_template('edit_preferences.html')

@app.route('/create_account', methods=['GET','POST'])
def create_account():
    return render_template('create_account.html')

if __name__ == "__main__":
    app.run(debug=True, host="localhost")