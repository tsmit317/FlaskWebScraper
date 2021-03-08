from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from WebScraper import appWS, cataWS, beechWS, sugarWS, wolfridgeWS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resortDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ResortDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    resort = db.Column(db.String(50))
    slc = db.Column(db.String(10))
    name = db.Column(db.String(100))
    status = db.Column(db.String(200))

 
def populate_db_conditions(dictToUse, rname, slc):
 for k, v in dictToUse.items():
        newCond = ResortDB(resort = rname, slc = slc, name = k, status = v)
        try:
            db.session.add(newCond)
            db.session.commit()
        except:
            print("Problem with adding conditions") 

def delete_everthing(modelToDelete):
    db.session.query(modelToDelete).delete()
    db.session.commit()

@app.route('/')
def index():
    cataCond = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="cond").all()
    cataSlope = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="slope").all()
    cataLift  = ResortDB.query.filter(ResortDB.resort == "Cata").filter(ResortDB.slc=="lift").all()
    beechCond = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="cond").all()
    beechSlope = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="slope").all()
    beechLift = ResortDB.query.filter(ResortDB.resort == "Ski Beech").filter(ResortDB.slc=="lift").all()
  
   
    
    return render_template('index.html', 
                            cataCond = cataCond, cataLift = cataLift, cataSlope = cataSlope,
                            beechCond = beechCond, beechLift = beechLift, beechSlope= beechSlope)



if __name__ == '__main__':
    db.create_all()
    delete_everthing(ResortDB)
    populate_db_conditions(cataWS.get_slope_dict(), "Cata", "slope")
    populate_db_conditions(cataWS.get_conditions_dict(), "Cata", "cond")
    populate_db_conditions(cataWS.get_lift_dict(), "Cata", "lift")
    populate_db_conditions(beechWS.get_conditions_dict(), "Ski Beech", "cond")
    populate_db_conditions(beechWS.get_lift_dict(), "Ski Beech", "lift")
    populate_db_conditions(beechWS.get_slope_dict(), "Ski Beech", "slope")

    
    app.run(debug=True)    