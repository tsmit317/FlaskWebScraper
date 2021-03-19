from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import appWS, cataWS, beechWS, sugarWS, wolfridgeWS
import sys
import time
from pytz import timezone


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resortDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()


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

def delete_everthing(modelToDelete):
    print("db delete")
    sys.stdout.flush()

    db.session.query(modelToDelete).delete()
    db.session.commit()

def update_db():
    print("update db")
    sys.stdout.flush()
    populate_db_conditions(appWS.get_conditions_dict(), "App", "cond")
    populate_db_conditions(appWS.get_slope_dict(), "App", "slope")
    populate_db_conditions(appWS.get_lift_dict(), "App", "lift")
    print("app udb: done")
    sys.stdout.flush()

    populate_db_conditions(cataWS.get_slope_dict(), "Cata", "slope")
    populate_db_conditions(cataWS.get_conditions_dict(), "Cata", "cond")
    populate_db_conditions(cataWS.get_lift_dict(), "Cata", "lift")
    print("cata udb: done")
    sys.stdout.flush()

    populate_db_conditions(beechWS.get_conditions_dict(), "Ski Beech", "cond")
    populate_db_conditions(beechWS.get_lift_dict(), "Ski Beech", "lift")
    populate_db_conditions(beechWS.get_slope_dict(), "Ski Beech", "slope")
    print("beech udb: done")
    sys.stdout.flush()

    populate_db_conditions(sugarWS.get_conditions_dict(), "Ski Sugar", "cond")
    populate_db_conditions(sugarWS.get_lift_dict(), "Ski Sugar", "lift")
    populate_db_conditions(sugarWS.get_slope_dict(), "Ski Sugar", "slope")
    print("sugar udb: done")
    sys.stdout.flush()

    populate_db_conditions(wolfridgeWS.get_conditions_dict(), "Wolf", "cond")
    populate_db_conditions(wolfridgeWS.get_lift_dict(), "Wolf", "lift")
    populate_db_conditions(wolfridgeWS.get_slope_dict(), "Wolf", "slope")
    print("wolf udb: done")
    sys.stdout.flush()

@scheduler.scheduled_job('interval', id='sched_job', minutes=30 ,max_instances=1, misfire_grace_time=900, start_date='2021-03-19 15:00:00')
def sched_job():
    print("sched_job")
    sys.stdout.flush()

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
    app.run(debug=True)    