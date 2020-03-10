# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask_cors import CORS
import urllib.request 
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    print("hello")
    return "hello weather!"

@app.route("/searchWeather", methods=['POST'])
def getData():
    value = request.json['value']
    api_key="44b62273d60a1ddee49f4c5344866cb8"
    sWeek = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'.format(value, api_key)
    sDay = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(value, api_key)
    try:
     sourceWeek = urllib.request.urlopen(sWeek)
     sourceDay = urllib.request.urlopen(sDay)
    except:
        print("wrong")
        return "this is wrong"
    weather_data_week= json.loads(sourceWeek.read())
    weather_data_today=json.loads(sourceDay.read())
    date=datetime.now().strftime("%H:%M")
    weather_data_week=weather_data_week["list"]
    def week_data_templete(num):
        return {
          "icon":"http://openweathermap.org/img/wn/"+weather_data_week[num]["weather"][0]["icon"]+"@2x.png",
            "temperature":int(weather_data_week[num]["main"]["temp"]-273.15),
            "description":weather_data_week[num]["weather"][0]["description"],
            "humidity":weather_data_week[num]["main"]["humidity"],
            "pressure":weather_data_week[num]["main"]["pressure"],
            "date":weather_data_week[num]["dt_txt"]
        }
    just_to_test=week_data_templete(1)
    week_result=[]
    for i in range(5):
        week_result.append({"day":week_data_templete(i*8+2),"night":week_data_templete(i*8+6)})
    
    return {
        # "description":weather_data_today["weather"][0]["description"],
        # "icon": "http://openweathermap.org/img/wn/"+weather_data_today["weather"][0]["icon"]+"@2x.png",
        # "temperature":int(weather_data_today["main"]["temp"]-273.15),
        "date":date,
        "today":{
            "icon":"http://openweathermap.org/img/wn/"+weather_data_today["weather"][0]["icon"]+"@2x.png",
            "temperature":int(weather_data_today["main"]["temp"]-273.15),
            "description":weather_data_today["weather"][0]["description"],
            "humidity":weather_data_today["main"]["humidity"],
            "pressure":weather_data_today["main"]["pressure"],
        },
        "week":week_result  
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')