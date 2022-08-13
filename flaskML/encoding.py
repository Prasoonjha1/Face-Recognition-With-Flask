import cv2 as cv
import numpy as np
import face_recognition as fc
import os
import time

path = 'Faces/train'
images = []
classNames = []
nameList = []
myList = os.listdir(path)
for cl in myList:
    print(cl)
    curImg = cv.imread(f'{path}/{cl}/{cl}.jpg')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    nameList.append('A')
def findencodings(imgs):
    encdli = []
    for img in imgs:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = fc.face_encodings(img)[0]
        encdli.append(encode)
    return encdli



encodeListForKnown = findencodings(images)
data = np.asarray(encodeListForKnown)
data1  = np.asarray(classNames)
data2 = np.asarray(nameList)
np.save('data.npy',data)
np.save('data1.npy', data1)
np.save('data2.npy',data2)
print('Encoding Complete')