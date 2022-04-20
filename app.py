from datetime import datetime
import sys
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
import requests
from appWS import App
from cataWS import Cata
from beechWS import Beech 
from sugarWS import Sugar
from wolfridgeWS import Wolf




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resortDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()


app_obj = App()
beech_obj = Beech()
cata_obj = Cata()
sugar_obj = Sugar()
wolf_obj = Wolf()


class ResortDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    resort = db.Column(db.String(50))
    slc = db.Column(db.String(10))
    name = db.Column(db.String(100))
    status = db.Column(db.String(200))
    updated_on = db.Column(db.String(50))


def populate_db_conditions(dictToUse, rname, slc):
    for k, v in dictToUse.items():
        now = datetime.now(timezone('America/New_York'))
        update_time = now.strftime("%m/%d/%Y, %I:%M:%S %p")
        newCond = ResortDB(resort = rname, slc = slc, name = k, status = v, updated_on = update_time)
        try:
            db.session.add(newCond)
            db.session.commit()
        except:
            print("Problem with adding conditions") 


def update_ws_objects():
    app_obj.update()
    beech_obj.update()
    cata_obj.update()
    sugar_obj.update()
    wolf_obj.update()


def delete_everthing(modelToDelete):
    db.session.query(modelToDelete).delete()
    db.session.commit()


def update_db():
    populate_db_conditions(app_obj.get_conditions(), "App", "cond")
    populate_db_conditions(app_obj.get_slope(), "App", "slope")
    populate_db_conditions(app_obj.get_lift(), "App", "lift")

    populate_db_conditions(cata_obj.get_conditions(), "Cata", "cond")
    populate_db_conditions(cata_obj.get_slope(), "Cata", "slope")
    populate_db_conditions(cata_obj.get_lift(), "Cata", "lift")

    populate_db_conditions(beech_obj.get_conditions(), "Ski Beech", "cond")
    populate_db_conditions(beech_obj.get_lift(), "Ski Beech", "lift")
    populate_db_conditions(beech_obj.get_slope(), "Ski Beech", "slope")

    populate_db_conditions(sugar_obj.get_conditions(), "Ski Sugar", "cond")
    populate_db_conditions(sugar_obj.get_lift(), "Ski Sugar", "lift")
    populate_db_conditions(sugar_obj.get_slope(), "Ski Sugar", "slope")

    populate_db_conditions(wolf_obj.get_conditions(), "Wolf", "cond")
    populate_db_conditions(wolf_obj.get_lift(), "Wolf", "lift")
    populate_db_conditions(wolf_obj.get_slope(), "Wolf", "slope")


@scheduler.scheduled_job('interval', id='sched_job', hours=1 ,max_instances=1, misfire_grace_time=900, next_run_time=datetime.now())
def sched_job():
    update_ws_objects()
    delete_everthing(ResortDB)
    update_db()
    time.sleep(20)

scheduler.start()     

def get_weather(lat, lon):
    api_key = os.environ.get('OPEN_WEATHER_API_KEY')
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial")
    
    req=r.json()
    descr = req['weather'][0]['description'].title()
    icon = req['weather'][0]['icon']
    return {'desc': descr, 'icon': f"https://openweathermap.org/img/wn/{icon}.png", 'temp': str("{:.1f}".format(req['main']['temp'])) + '°F'}

@app.route('/')
def home():
    appCond = ResortDB.query.filter(ResortDB.resort == "App").filter(ResortDB.slc=="cond").all()
    
    if (datetime.now() - datetime.strptime(appCond[0].updated_on,'%m/%d/%Y, %I:%M:%S %p')).seconds/3600 > 6:
        scheduler.shutdown()
        scheduler.start()
    
    appCond = ResortDB.query.filter(ResortDB.resort == "App").filter(ResortDB.slc=="cond").all()
    appSlope = ResortDB.query.filter(ResortDB.resort == "App").filter(ResortDB.slc=="slope").all()
    appLift = ResortDB.query.filter(ResortDB.resort == "App").filter(ResortDB.slc=="lift").all()
    

    cataCond = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="cond").all()
    cataSlope = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="slope").all()
    cataLift  = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="lift").all()
    
    
    beechCond = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="cond").all()
    beechSlope = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="slope").all()
    beechLift = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="lift").all()
    
    sugarCond = ResortDB.query.filter(ResortDB.resort == "Ski Sugar").filter(ResortDB.slc=="cond").all()
    suagrSlope = ResortDB.query.filter(ResortDB.resort == "Ski Sugar").filter(ResortDB.slc=="slope").all()
    sugarLift = ResortDB.query.filter(ResortDB.resort == "Ski Sugar").filter(ResortDB.slc=="lift").all()
    
    wrCond = ResortDB.query.filter(ResortDB.resort == "Wolf").filter(ResortDB.slc=="cond").all()
    wrSlope = ResortDB.query.filter(ResortDB.resort == "Wolf").filter(ResortDB.slc=="slope").all()
    wrLift = ResortDB.query.filter(ResortDB.resort == "Wolf").filter(ResortDB.slc=="lift").all()
    
    return render_template('home.html', 
                            appCond = appCond, appLift = appLift, appSlope = appSlope, appWeather = get_weather(36.173957698179045, -81.66265630243835),
                            cataCond = cataCond, cataLift = cataLift, cataSlope =cataSlope, cataWeather = get_weather(35.56216406965617, -83.09036834582928),
                            beechCond = beechCond, beechLift = beechLift, beechSlope= beechSlope, beechWeather = get_weather(36.192907117543285, -81.87807586201936),
                            sugarCond = sugarCond, sugarLift = sugarLift, sugarSlope = suagrSlope, sugarWeather = get_weather(36.128552597736494, -81.86381420634011),
                            wrCond = wrCond, wrLift = wrLift, wrSlope = wrSlope, wrWeather = get_weather(35.952354672507575, -82.50723837684295))


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db.create_all()
    # delete_everthing(ResortDB)
    # update_db()
    app.run(debug=False)    