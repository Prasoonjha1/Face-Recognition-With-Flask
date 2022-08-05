import cv2 as cv
import numpy as np
import face_recognition as fc
import os
import time
from files import db,bcrypt,login_manager
from flask_login import UserMixin

encodeListForKnown = np.load('data.npy')
classNames = np.load('data1.npy')

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.encodeListForKnown = encodeListForKnown
        self.classNames = classNames
    
    def __del__(self):
        self.video.release()

    
    def Face_Rec(self):
        
        success, img = self.video.read()
        
        imgS = cv.resize(img,(0,0),None, 0.25, 0.25)
        imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)
        facecrfr = fc.face_locations(imgS)
        encodecurframe = fc.face_encodings(imgS,facecrfr)
        for encodeFace, faceloc in zip(encodecurframe, facecrfr):
            matches = fc.compare_faces(self.encodeListForKnown, encodeFace)
            faceDis = fc.face_distance(self.encodeListForKnown, encodeFace)
            '''print(faceDis)'''
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = self.classNames[matchIndex].upper()
                print(name)
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv.rectangle(img,(x1,y1) , (x2,y2), (0,255,0),2)
                cv.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0),cv.FILLED)
                cv.putText(img, name, (x1+6,y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
                break
        ret,buffer = cv.imencode('.jpg', img)
        return buffer.tobytes()

@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))
        
class Person(db.Model,UserMixin):
    id = db.Column(db.Integer,nullable=False,unique=True,primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False,unique=True)
    faces = db.relationship("Faces",backref='owned_user', lazy=True)
    

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Faces(db.Model):
    id = db.Column(db.String(length=30), nullable=False, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    encodings = db.Column(db.JSON, unique=True,nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('person.id'))
    attendance = db.relationship("Attendance",backref='owned_user',lazy=True)
    
    def __repr__(self):
        return f'Faces {self.name}'

class Attendance(db.Model):
    id = db.Column(db.Integer(),nullable=False,unique=True,primary_key=True)
    date = db.Column(db.JSON)
    att = db.Column(db.JSON)
    owner = db.Column(db.Integer(),db.ForeignKey('faces.id'))
