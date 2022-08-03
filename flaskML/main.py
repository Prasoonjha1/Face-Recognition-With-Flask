from flask import Flask, render_template,Response
from Face import VideoCamera
import numpy as np
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service.db'
db = SQLAlchemy(app)

class Person(db.Model):
    username = db.Column(db.String(30), nullable=False, unique=True,primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    encodings = db.Column(db.JSON)
    classnames = db.Column(db.JSON)

    def __repr__(self):
        return f'Person {self.username}'

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    person = Person.query.all()
    return render_template('market.html',persons=person)
def gen(Face):
    while True:
        frame = Face.Face_Rec()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')  

if __name__=="__main__":
    app.run(debug=True)