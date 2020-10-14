# Imports
from flask import Flask                 # general web development
from flask import render_template       # render html5 templates
from flask import request               #
from flask import redirect              #
from flask_sqlalchemy import SQLAlchemy # create sqlite databases using python3

# create the flask application object
app = Flask(__name__)

# create a database and link it to the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rooms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# create a table of broken laptops
class rooms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(16), nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    
#################################################################
# Create basic CRUD API                                         #
#                                                               #
# Create - will add new broken laptop to inventory              #
# Read - will list all the existing broken laptops in inventory #
# Update - will modify the attributes of a broken laptop        #
# Delete - will delete a single entry of a broken laptop        #
#################################################################

@app.route('/')
def init_db():
    db.drop_all()
    db.create_all()
    
    # Test entries
    new_room1 = rooms(building = "ET",room_number = 236)
    new_room2 = rooms(building = 2.0 ,room_number = 220)
    db.session.add(new_room1)
    db.session.add(new_room2)
    db.session.commit()
    
    return redirect('/read')

# @app.route('/create')
# def create():

@app.route('/read')
def read():
    all_rooms = rooms.query.all()
    return render_template("read.html", all_rooms = all_rooms, title = "Read")
    
# @app.route('/update>')
# def update():
#     
# @app.route('/delete>')
# def delete():
    
if __name__ == '__main__':
    app.run(debug=True)
