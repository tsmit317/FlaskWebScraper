from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from WebScraper import appWS, cataWS, beechWS, sugarWS, wolfridgeWS
from datetime import datetime
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resortDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

scheduler = APScheduler()

class ResortDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    resort = db.Column(db.String(50))
    slc = db.Column(db.String(10))
    name = db.Column(db.String(100))
    status = db.Column(db.String(200))
    updated_on = db.Column(db.String(50))
        
 
def populate_db_conditions(dictToUse, rname, slc):
 for k, v in dictToUse.items():
        now = datetime.now()
        update_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        newCond = ResortDB(resort = rname, slc = slc, name = k, status = v, updated_on = update_time)
        try:
            db.session.add(newCond)
            db.session.commit()
        except:
            print("Problem with adding conditions") 

def delete_everthing(modelToDelete):
    db.session.query(modelToDelete).delete()
    db.session.commit()

def update_db():
    populate_db_conditions(appWS.get_conditions_dict(), "App", "cond")
    populate_db_conditions(appWS.get_slope_dict(), "App", "slope")
    populate_db_conditions(appWS.get_lift_dict(), "App", "lift")
    
    populate_db_conditions(cataWS.get_slope_dict(), "Cata", "slope")
    populate_db_conditions(cataWS.get_conditions_dict(), "Cata", "cond")
    populate_db_conditions(cataWS.get_lift_dict(), "Cata", "lift")

    populate_db_conditions(beechWS.get_conditions_dict(), "Ski Beech", "cond")
    populate_db_conditions(beechWS.get_lift_dict(), "Ski Beech", "lift")
    populate_db_conditions(beechWS.get_slope_dict(), "Ski Beech", "slope")

    populate_db_conditions(sugarWS.get_conditions_dict(), "Ski Sugar", "cond")
    populate_db_conditions(sugarWS.get_lift_dict(), "Ski Sugar", "lift")
    populate_db_conditions(sugarWS.get_slope_dict(), "Ski Sugar", "slope")

    populate_db_conditions(wolfridgeWS.get_conditions_dict(), "Wolf", "cond")
    populate_db_conditions(wolfridgeWS.get_lift_dict(), "Wolf", "lift")
    populate_db_conditions(wolfridgeWS.get_slope_dict(), "Wolf", "slope")

def scheduledTask():
     delete_everthing(ResortDB)
     update_db()
     print('Inside Scheduled Task')
     

@app.route('/')
def index():
    
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
    
    return render_template('index.html', 
                            appCond = appCond, appLift = appLift, appSlope = appSlope,
                            cataCond = cataCond, cataLift = cataLift, cataSlope = cataSlope,
                            beechCond = beechCond, beechLift = beechLift, beechSlope= beechSlope,
                            sugarCond = sugarCond, sugarLift = sugarLift, sugarSlope = suagrSlope, 
                            wrCond = wrCond, wrLift = wrLift, wrSlope = wrSlope)



if __name__ == '__main__':
    db.create_all()
    # delete_everthing(ResortDB)
    # update_db()
    # scheduler.add_job(id = 'Scheduled task', func=scheduledTask, trigger='interval', minutes=60)
    # scheduler.start()
    app.run(debug=True)    