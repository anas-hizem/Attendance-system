import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://attendance-system-real-time-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')



data = {
    "518468" :
        {
            "name" : "Leo Messi" ,
            "major" : "Football" ,
            "starting_year" : "2006" ,
            "total-attendance" : 6 ,
            "standing" : "G" ,
            "year" : 4 ,
            "last_attendance_time" : "2023-08-15 00:54:34"

        },
    "645151":
        {
            "name": "Anas Hizem",
            "major": "Software Engineering Student",
            "starting_year": "2022",
            "total-attendance": 2,
            "standing": "G",
            "year": 1,
            "last_attendance_time" : "2023-08-15 00:54:34"
        },
    "848754":
        {
            "name": "Mark Zuckerberg",
            "major": "Computer Science",
            "starting_year": "2004",
            "total-attendance": 10,
            "standing": "G",
            "year": 10,
            "last_attendance_time" : "2023-08-15 00:54:34"
        },
    "864215" :
        {
            "name": "Elon Musk",
            "major": "physics and economics",
            "starting_year": "2008",
            "total-attendance": 0,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2023-08-15 00:54:34"
        }
}


for key , value in data.items():
    ref.child(key).set(value)