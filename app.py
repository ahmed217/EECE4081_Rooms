# Imports
from flask import Flask                 # general web development
from flask import render_template       # render html5 templates
from flask import request               #
from flask import redirect              #
from flask_sqlalchemy import SQLAlchemy # create sqlite databases using python3
from flask.json import jsonify

# create the flask application object
app = Flask(__name__)

# create a database and link it to the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rooms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# create a table of rooms
class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(16), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    
    def serialize(self):
        return {
            'id'        :   self.id,
            'name'      :   self.name,
            'number'    :   self.number,
            'capacity'  :   self.capacity
        }
#################################################################
# Create basic CRUD API                                         #
#                                                               #
# Create - will add new broken laptop to inventory              #
# Read - will list all the existing broken laptops in inventory #
# Update - will modify the attributes of a broken laptop        #
# Delete - will delete a single entry of a broken laptop        #
#################################################################

@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all()
    return 'DB initialized'

@app.route('/json_dump')
def json_dump():
    all_rooms = Rooms.query.all()
    json_data = jsonify( json_list = [i.serialize() for i in all_rooms] )
    return json_data 

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        name = request.form.get("name")
        number = request.form.get("number")
        capacity = request.form.get("capacity")
        new_room = Rooms(name = name,number = number ,capacity = capacity)
        db.session.add(new_room)
        db.session.commit()
        
    all_rooms = Rooms.query.all()
    return render_template("create.html", all_rooms = all_rooms, title = "Create a Room")

@app.route('/')
def read():
    all_rooms = Rooms.query.all()
    return render_template("read.html", all_rooms = all_rooms, title = "Rooms Listing")
    
@app.route('/update/<room_id>', methods = ['GET', 'POST'])
def update(room_id):
    update_room = Rooms.query.get(room_id)
    if request.form:
        update_room.name = request.form.get("name")
        update_room.number = request.form.get("number")
        update_room.capacity = request.form.get("capacity")
        db.session.commit()
    all_rooms = Rooms.query.all()
    return render_template("update.html", update_room = update_room, all_rooms = all_rooms, title = "Update a room")

@app.route('/delete/<room_id>') # add id
def delete(room_id):
    delete_room = Rooms.query.get(room_id)
    db.session.delete(delete_room)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
