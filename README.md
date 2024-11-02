# Real-Time Face Attendance System

This project is a Real-Time Face Attendance System that uses computer vision and face recognition technology to automate attendance tracking. The system captures video from a webcam, detects faces, and marks attendance based on recognized individuals. It utilizes Firebase for storing user data and attendance records.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Firebase Configuration](#firebase-configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time face detection and recognition.
- Attendance tracking with automatic updates in Firebase.
- Displays student information such as name, major, and total attendance.
- Supports adding new students to the Firebase database.

## Technologies Used

- Python
- OpenCV
- Face Recognition
- Firebase Admin SDK
- NumPy
- CVZone
- Pickle

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install the required packages:**
Ensure you have Python installed. You can create a virtual environment and install the required libraries:
   
   ```bash
    pip install opencv-python face_recognition firebase-admin numpy
   ```

3. **Firebase Configuration:**
- Create a Firebase project.
- Download the service account key (JSON file) and place it in the project directory. Rename it to serviceAccountKey.json.
- Set up a Realtime Database and Storage bucket in your Firebase project.

4. **Prepare Images:**

Place student images in a folder named images in the project directory. Ensure the images are named with the corresponding student IDs (e.g., 518468.png).

5. **Add Student Data:**

- Modify the addDataToDatabase.py file to include student details.
- Run addDataToDatabase.py to upload student information to Firebase.

## Usage :
1. **Generate Face Encodings:**
Run EncodeGenerator.py to encode the student images and create the encoding file (encodeFile.p).

   ```bash
    python EncodeGenerator.py

   ```
2. **Run the Main Application:**

   ```bash
    python main.py
   ```
The application will open a window displaying the webcam feed and attendance interface.

3. **Attendance Process:**

- As students enter the frame, their faces will be detected and matched against the database.
- When a match is found, the system will update the attendance record in Firebase and display the corresponding student information on the screen.


## Code Structure :


```bash
  .
  ├── images                   # Directory for student images
  ├── resources                # Directory for background and mode images
  │   ├── background.png
  │   └── Modes               # Directory for mode images
  ├── EncodeGenerator.py       # Script to encode student images
  ├── main.py                  # Main attendance system script
  ├── addDataToDatabase.py     # Script to add student data to Firebase
  └── serviceAccountKey.json    # Firebase service account key

```

## Firebase Configuration :

Make sure to set the following rules in your Firebase Realtime Database for testing purposes:

```bash
      {
        "rules": {
          ".read": "auth != null",
          ".write": "auth != null"
        }
      }
```


