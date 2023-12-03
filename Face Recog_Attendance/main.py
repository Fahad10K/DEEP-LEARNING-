import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import shutil

# import pandas as pd
# from simple_facerec import SimpleFacerec


path = 'ImageAttendance'
images = []
classNames = []
mylist = os.listdir(path)
print(mylist)

# creating a list of names from the images in dataset
for cls in mylist:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)


# converting image into RGB and encoding it
def findencoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print(encodeList)
    return encodeList


# marking attendance on an excel sheet
def markAttendance(name):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            date = datetime.today()
            dString = date.strftime('%d:%b:%Y')
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{"PRESENT"},{dString}')

encodeListKnown = findencoding(images)
print('Facial Landmark estimation  Complete....\nDeep CNN used for measuring faces... \n Using SVM classifiers...')

# capturing image using webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # HOG
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(img, facesCurFrame)

    # encoding captured frame to match the faces with dataset
    # Finding face landmarks in captured frame adn comparing it to the known faces landmark of data set
    for encodeFace, faceLocation in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        # Labelling faces
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1, x2, y2, x1

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)

            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name)
            # cv2.imshow(name, img)
        else:
            name = "Unknown"

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)

            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # markAttendance(name)
            # cv2.imshow(name, img)

    # On screen date and time
    if success:
        # save it inside a variable
        dt = str(datetime.now())
        # put the dt variable over the
        # video frame
        img = cv2.putText(img, dt,(10, 100),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv2.LINE_8)

    cv2.imshow('Facial Recognition Attendance System', img)

    # EXITING THE CODE AND MODIFYING THE CSV FILES

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        cap.release()
        cv2.destroyAllWindows()

        Current_Date = datetime.today().strftime('%d-%b-%Y')
        # Renaming the file
        shutil.copyfile(r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton_modificationary\Attendance.csv',
                        r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton_modificationary\Attendance_' + str(Current_Date) + '.csv')

        file = 'Attendance.csv'
        lines = open(file).readlines()
        open(file, 'w').writelines(lines[:2])
