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
class Rooms(db.Model):
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
@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        name = request.form.get("name")
        capacity = request.form.get("capacity")
        room = Rooms(name = name, capacity = capacity)
        db.session.add(room)
        db.session.commit()
        
    room = Rooms.query.all()
    return render_template("create.html",room = room)

@app.route('/read')
def read():
    all_rooms = Rooms.query.all()
    return render_template("read.html", all_rooms = all_rooms, title = "Read")

def update(room_id):
    #all_rooms = rooms.query.all()
    update_room = Rooms.query.get(room_id)
    
    if request.form:
            
            update_room.name = request.form.get("name")
            update_room.capacity = request.form.get("capacity")
            
         
            
            
            
          
            
            
            
#     
            db.session.commit()
            return redirect("/read")
    return render_template("update.html",update_room = update_room)
    
#@app.route('/update/<room_id>', methods = ['GET', 'POST'])
#def update(room_id):
#    all_rooms = Rooms.query.all()
#    update_room = Rooms.query.get(room_id)
#    if request.form:
#            
#            update_room.name = request.form.get("name")
#            update_room.capacity = request.form.get("capacity")
     
#            db.session.commit()
 #   return render_template("update.html",update_room = update_room, all_rooms = all_rooms)

@app.route('/delete/<room_id>') # add id
def delete(room_id):
    room = Rooms.query.get(room_id)
    db.session.delete(room)
    db.session.commit()
    return redirect("/read")
    
if __name__ == '__main__':
    app.run(debug=True)
