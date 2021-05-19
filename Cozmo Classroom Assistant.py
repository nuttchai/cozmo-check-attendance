#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Display Cozmo's camera feed back on his face (like a mirror)
'''
from PIL import Image
import sys
import time
import imageio
try:
    import numpy as np
except ImportError:
    sys.exit("Cannot import numpy: Do `pip3 install --user numpy` to install")

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo
import cv2


line_token = 'X4Yb6QA4cIFDBtq00kx9lOMwEclbQFhlrlSaKwVDAK8' #EDIT Line address HERE
Pic_Path = "C:/Users/AIlucky/Desktop/FaceDetect-master/unknown_faces/000000.png" #EDIT Picture address HERE
all_student_id = ['61011278', '61011312', '61011318', '61011334', '61011338', '61011353', '61011356', '61011358', '61011359', '61011441'] #EDIT ID Student HERE
Total_Student = 10 #EDIT Number of student in classroom
path = Pic_Path

###################################################################################################################3

#TIME DATE

def day():
    from datetime import date
    import calendar
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]
def date():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%m-%d-%Y")

######################################################################################################################################

#LINE NOTIFICATION"

def _lineNotify(file, payload):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = line_token
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload)
    #return requests.post(url, headers=headers , files=file, data = payload)

def notifyPicture(url,robot: cozmo.robot.Robot):
    
    import os.path
    
    if url and os.path.isfile(url):
        files = {"imageFile": open(url, "rb")}
        
    S = Total_Student
    Present = len(student_id())
    Absent = S - Present

    if Present == 1:
        if Absent == 1:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and 1 student who's absent.").wait_for_completed()
        elif Absent > 1:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and " + str(Absent) + " students who's absent.").wait_for_completed()
        else:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and no student who's absent.").wait_for_completed()

    elif Present == 0:
        payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
        robot.say_text("On " + day() +  " there is no student in the classroom.").wait_for_completed()
        
    else:
        if Absent == 1:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and 1 student who's absent.").wait_for_completed()
        elif Absent > 1:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and " + str(Absent) + " students who's absent.").wait_for_completed()
        else:
            payload = {'message': "[ " + str(date()) + " ]   Present: " + str(Present) + "     Absent: " + str(Absent)}
            robot.say_text("On " + day() + " there are " + str(Present) + " student in the classroom and no student who's absent.").wait_for_completed()
            
    return _lineNotify(files, payload)


#######################################################################################################################################

#DETECT STUDENT WHO's PRESENT

#cozmo.run_program(cozmo_face_camera)
#EXECUTING COMMAND FOR LINE NOTIFICATION"
#print(_lineNotify(None, {'message':"123"}))
#to add additional message replace the string "123" with the message you want to put in
def student_id():

    import face_recognition
    from os import listdir
    from os.path import isfile, join

    known_faces = []
    known_face_name= []
    # Load the jpg files into numpy arrays
    known_faces_images_files = [f for f in listdir("faces") if isfile(join("faces", f))]
    for i in known_faces_images_files:
        image = face_recognition.load_image_file("faces/"+i)
        image_encoded = face_recognition.face_encodings(image)[0]
        known_faces.append(image_encoded)
        j = i.split(".")
        known_face_name.append(j[0])

    # lucky_image = face_recognition.load_image_file("faces/lucky.jpg")
    # boss_image = face_recognition.load_image_file("faces/boss.jpg")
    unknown_image = face_recognition.load_image_file("unknown_faces/000000.png")


    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.


    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    unknown_faces_encoded = face_recognition.face_encodings(unknown_image)
    results = []
    for unknown_face_encoded in unknown_faces_encoded:
        matches = face_recognition.compare_faces(known_faces, unknown_face_encoded, tolerance=0.6)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_name[first_match_index]

            results.append(name)
    
    return results
import csv

########################################################################################

#ATTENDANCE SCORE

def score_attendace(a, result):
    all_student = all_student_id
    attendance = []
    for i in all_student:
        if i in result: attendance.append('1')
        else: attendance.append('0')

    bottle_list = []

    # Read all data from the csv file.
    with open('List_of_student.csv', newline='') as b:
        bottles = csv.reader(b, delimiter=',', quotechar='|')
        # for i in bottles:
        #     print(i)
        bottle_list.extend(bottles)

    # data to override in the format {line_num_to_override:data_to_write}. 
    column = ['week'+a]
    column.extend(attendance)
    line_to_override = {int(a)+1: column}

    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open('List_of_student.csv','w', newline='') as b:
        writer = csv.writer(b, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line, row in enumerate(bottle_list):
            data = line_to_override.get(line, row)
            writer.writerow(data)

#################################################################################################################################

#TAKING PICTURE

cap = cv2.VideoCapture(0)
def capture_pic(robot: cozmo.robot.Robot):
    while True:
        k = cv2.waitKey(30)
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        if k == -1: # Esc key to stop
            continue
        elif int(chr(k)) >= 1 and int(chr(k)) <= 9: # normally -1 returned,so don't print it
            cv2.imwrite(path,frame)
            score_attendace(chr(k), student_id())
            break
    notifyPicture(path,robot)

##########################################################################################################################33

#EXCUTE CODE

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(capture_pic)

print(student_id())