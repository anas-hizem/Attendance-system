import os
import pickle
import cvzone
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://attendance-system-real-time-default-rtdb.firebaseio.com/",
    "storageBucket" : "attendance-system-real-time.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


imgBackground = cv2.imread('resources/background.png')


#importing the mode pictures into a list
folderModePath = 'resources/Modes'
modePathList = os.listdir((folderModePath))
imgModeList = []
for path in modePathList :
    imgModeList.append(cv2.imread(os.path.join(folderModePath , path)))




#load the encoding file
print("Loading Encode file")
file = open("encodeFile.p" , 'rb')
encodeListknownWithIds = pickle.load(file)
file.close()
encodeListknown , studentIds = encodeListknownWithIds
print(studentIds)
print("Encode file loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []



while True :
    sucess, img = cap.read()

    imgS = cv2.resize(img , (0 , 0) , None , 0.25 , 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS , faceCurFrame)

    imgBackground[187:187+480 , 60:60+640] = img
    imgBackground[50:50+620 , 785:785+435] = imgModeList[modeType]

    if faceCurFrame :

        for encodeFace , faceLoc in zip(encodeCurFrame , faceCurFrame) :
            matches = face_recognition.compare_faces(encodeListknown , encodeFace)
            faceDis = face_recognition.face_distance(encodeListknown , encodeFace)
            #print("matches" , matches)
            #print("faceDis" , faceDis)
            matchIndex = np.argmin(faceDis)
            #print("Match Index" , matchIndex)


            if matches[matchIndex] :
                #print("Known Face Detected")
                #print(studentIds[matchIndex])
                y1 , x2 , y2 , x1 = faceLoc
                #y1 , x2 , y2 , x1 = y1 * 4 , x2 * 4 , y2 * 4 , x1 * 4
                bbox = 60+x1 , 187+y1 , x2 - x1 , y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground , bbox ,rt=0)
                #cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)
                id = studentIds[matchIndex]
                if counter == 0 :
                    cvzone.putTextRect(imgBackground , "Loading ..." , (275 , 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 3


        if counter != 0 :

            if counter == 1 :
                #get the data from yhe storage
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                #get the image from yhe storage
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string() , np.uint8)
                imgStudent = cv2.imdecode(array , cv2.COLOR_BGR2RGB)



                #update the data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondeElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondeElapsed)
                if secondeElapsed > 30 :
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total-attendance'] +=1
                    ref.child('total-attendance').set(studentInfo['total-attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 1
                    counter = 0
                    imgBackground[50:50 + 620, 785:785 + 435] = imgModeList[modeType]

            if modeType != 1 :

                if 10 < counter < 20 :
                    modeType = 2

                imgBackground[50:50 + 620, 785:785 + 435] = imgModeList[modeType]

                if counter <= 10 :

                    cv2.putText(imgBackground , str(studentInfo['total-attendance']),(850, 110) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0 , 0) , 2)
                    cv2.putText(imgBackground , str(studentInfo['major']),(970, 570) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0 , 0 , 0) , 1)
                    cv2.putText(imgBackground , str(id),(970, 520) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0 , 0 , 0) , 1)
                    cv2.putText(imgBackground , str(studentInfo['standing']),(910, 625) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0 , 0 , 0) , 1)
                    cv2.putText(imgBackground , str(studentInfo['year']),(1025, 625) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0 , 0 , 0) , 1)
                    cv2.putText(imgBackground , str(studentInfo['starting_year']),(1150, 625) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0 , 0 , 0) , 1)

                    cv2.putText(imgBackground , str(studentInfo['name']),(940, 110) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0 , 0) , 2)


                    imgBackground[180:180+280 , 862:862+280] = imgStudent


            counter +=1
            if counter >= 20 :
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[50:50 + 620, 785:785 + 435] = imgModeList[modeType]
    else :
        modeType = 0
        counter = 0


    #print(img.shape)
    #cv2.imshow("WebCam" ,imgModeList[0])
    cv2.imshow("Face Attendance" , imgBackground)
    cv2.waitKey(1)