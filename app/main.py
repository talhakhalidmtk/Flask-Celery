import json
import urllib
import requests


import mysql.connector    
cnx = mysql.connector.connect(user='root', password='Physics-94',
                              host='127.0.0.1',
                              database='car_model_schema')
cursor = cnx.cursor()

def insert(data):
    query = """INSERT INTO car_model (objectId, Year, Make, Model, Category, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s) AS new 
            ON DUPLICATE KEY UPDATE Year=new.Year, Make=new.Make, Category=new.Category, createdAt=new.createdAt, updatedAt=new.updatedAt
            ;""",data
    cursor.execute(*query)

def commit():
  cnx.commit()
  print("Data inserted successfully.")



from flask import Flask, jsonify
from celery import Celery
app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"

celery = Celery(app.name)
celery.conf.update(app.config)

where = urllib.parse.quote_plus("""
{
    "Year": {
        "$gte": 2012
    }
}
""")
url = 'https://parseapi.back4app.com/classes/Car_Model_List?count=1&limit=0&order=Year&where=%s' % where
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z', 
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW' 
}

@celery.task
def car_model():
    with app.app_context():
        print("Process Started")
        total_count = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) 
        count = total_count["count"]
        data_url = url.replace('limit=0','limit='+str(count))
        data = json.loads(requests.get(data_url, headers=headers).content.decode('utf-8')) 
        for i in data["results"]:
            insert(tuple(i.values()))
        commit()
        print("Process Stopped")

@app.route('/')
def add_task():
    car_model.apply_async(countdown=60)
    return jsonify({'status': 'ok'})


