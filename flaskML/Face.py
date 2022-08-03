import cv2 as cv
import numpy as np
import face_recognition as fc
import os
import time
import attendance


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
                attendance.markAttendance(name)
        ret,buffer = cv.imencode('.jpg', img)
        return buffer.tobytes()
        
        

