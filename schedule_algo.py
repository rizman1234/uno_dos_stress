import enum
import os
import pyodbc
import time

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv


load_dotenv(dotenv_path="config.py")

SENDGRID_KEY = os.getenv("SENDGRID_KEY")
SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_USERNAME = os.getenv("SERVER_USERNAME")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD")

server = SERVER_NAME + '.database.windows.net'
database = 'test'
username = SERVER_USERNAME
password = SERVER_PASSWORD
driver= '{ODBC Driver 17 for SQL Server}'

days_arr = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT distinct([activities]) FROM [dbo].[Activities]")
            activites = cursor.fetchall()
            print(activites)

            for i in enumerate(activites):
                for j in range(13):
                    cursor.execute("SELECT s.*, email, activities from [dbo].[Schedule] s JOIN [dbo].[USER] u on s.user_id = u.user_id JOIN [dbo].[Activities] a on a.user_id=s.user_id WHERE activities = '{}' and block_time = {}".format(i[1][0],j+8))
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        print(data)
                        for k, val in enumerate(data):
                            message = Mail(
                                from_email='sghulamani@crimson.ua.edu',
                                to_emails = data[k][3],
                                subject = data[k][4] + ' Activity Found',
                                html_content='<strong>On ' + days_arr[data[k][1]] + ' from ' + str(data[k][2]) + ' to ' + str(data[k][2]+1) + ' </strong>')
                            try:
                                sg = SendGridAPIClient(SENDGRID_KEY)
                                response = sg.send(message)
                                print(response.status_code)
                                print(response.body)
                                print(response.headers)
                            except Exception as e:
                                print(e.message)