from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from appWS import App
from cataWS import Cata
from beechWS import Beech 
from sugarWS import Sugar
from wolfridgeWS import Wolf
import sys
import time
from pytz import timezone


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
    print("populate db")
    sys.stdout.flush()

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
    print("update_ws_objects: start")
    sys.stdout.flush()

    app_obj.update()
    beech_obj.update()
    cata_obj.update()
    sugar_obj.update()
    wolf_obj.update()

    print("update_ws_objects: end")
    sys.stdout.flush()


def delete_everthing(modelToDelete):
    print("db delete")
    sys.stdout.flush()

    db.session.query(modelToDelete).delete()
    db.session.commit()


def update_db():
    print("update db")
    sys.stdout.flush()

    populate_db_conditions(app_obj.get_conditions(), "App", "cond")
    populate_db_conditions(app_obj.get_slope(), "App", "slope")
    populate_db_conditions(app_obj.get_lift(), "App", "lift")
    print("app udb: done")
    sys.stdout.flush()

    populate_db_conditions(cata_obj.get_conditions(), "Cata", "cond")
    populate_db_conditions(cata_obj.get_slope(), "Cata", "slope")
    populate_db_conditions(cata_obj.get_lift(), "Cata", "lift")
    print("cata udb: done")
    sys.stdout.flush()

    populate_db_conditions(beech_obj.get_conditions(), "Ski Beech", "cond")
    populate_db_conditions(beech_obj.get_lift(), "Ski Beech", "lift")
    populate_db_conditions(beech_obj.get_slope(), "Ski Beech", "slope")
    print("beech udb: done")
    sys.stdout.flush()

    populate_db_conditions(sugar_obj.get_conditions(), "Ski Sugar", "cond")
    populate_db_conditions(sugar_obj.get_lift(), "Ski Sugar", "lift")
    populate_db_conditions(sugar_obj.get_slope(), "Ski Sugar", "slope")
    print("sugar udb: done")
    sys.stdout.flush()

    populate_db_conditions(wolf_obj.get_conditions(), "Wolf", "cond")
    populate_db_conditions(wolf_obj.get_lift(), "Wolf", "lift")
    populate_db_conditions(wolf_obj.get_slope(), "Wolf", "slope")
    print("wolf udb: done")
    sys.stdout.flush()


@scheduler.scheduled_job('interval', id='sched_job', hours=1 ,max_instances=1, misfire_grace_time=900, next_run_time=datetime.now())
def sched_job():
    print("sched_job")
    sys.stdout.flush()

    update_ws_objects()
    delete_everthing(ResortDB)
    update_db()
    time.sleep(20)

scheduler.start()     


@app.route('/')
def home():
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
                            appCond = appCond, appLift = appLift, appSlope = appSlope,
                            cataCond = cataCond, cataLift = cataLift, cataSlope = cataSlope,
                            beechCond = beechCond, beechLift = beechLift, beechSlope= beechSlope,
                            sugarCond = sugarCond, sugarLift = sugarLift, sugarSlope = suagrSlope, 
                            wrCond = wrCond, wrLift = wrLift, wrSlope = wrSlope)


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    db.create_all()
    # delete_everthing(ResortDB)
    # update_db()
    app.run(debug=False)    