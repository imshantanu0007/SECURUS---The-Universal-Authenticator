import urllib.request
import urllib.parse
from pages.views import Register_form
import random 
import os
import cv2
import numpy as np
from PIL import Image
import pickle
import win32api
import ctypes 
import dlib
from math import hypot

def get_image(path):
    image_path=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    ids=[]
    for img_path in image_path:
        faceImg=Image.open(img_path).convert("L")
        size=(350,350)
        final_img=faceImg.resize(size,Image.ANTIALIAS)
        facenp=np.array(final_img,"uint8")
        ID=int(os.path.split(img_path)[-1].split(".")[1])
        faces.append(facenp)
        ids.append(ID)
        cv2.waitKey(5)
    return np.array(ids),faces

def dataset_generator(id):
    cam=cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier(r"C:\Users\Shantanu Shukla\djangoProject\pages\haarcascade_frontalface_default.xml")
    sample_Num=0
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        for(x,y,w,h) in faces:
            if w*h>=33120:
                sample_Num=sample_Num+1
                cv2.imwrite(r"media/user."+str(id)+"."+str(sample_Num)+".jpg",gray[y:y+h,x:x+w])
                cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow("img",im)
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''') # To make window active
        cv2.waitKey(5)
        if sample_Num>500:
            cam.release()
            cv2.destroyAllWindows()
            break
    recog= cv2.face.LBPHFaceRecognizer_create()
    ids,faces= get_image(r"media")
    recog.train(faces,ids)
    recog.save("pages/trainingdata.yml")
    cv2.destroyAllWindows()
    win32api.MessageBox(0, "Successfully Registered!!!", "SUCCESS!", 0x00001000)
    #if(z):
        #return render(request,"home.html",{})

def midpt(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def gets_blinking_ratio(eye_points, facial_landmarks):
    
    left_points = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_points = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpt(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpt(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
 
    hor_lines_length = hypot((left_points[0] - right_points[0]), (left_points[1] - right_points[1]))
    ver_lines_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
 
    ratio = hor_lines_length / ver_lines_length
    return ratio

def face_detector():
    l=blinking()
    if(l=="0"):
        return "0"
    recogniser= cv2.face.LBPHFaceRecognizer_create()
    recogniser.read("pages/trainingdata.yml")
    facesCascade= cv2.CascadeClassifier(r"C:\Users\Shantanu Shukla\djangoProject\pages\haarcascade_frontalface_default.xml")
    cam= cv2.VideoCapture(0)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        #ids=np.empty(1,dtype= int)
        ret,im =cam.read()
        if ret!=0:
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        
        faces=facesCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(int(minW),int(minH)), flags = cv2.CASCADE_SCALE_IMAGE)
        co1=0
        co2=0
        i=0
        
        for(x,y,w,h) in faces:
            i+=1
            if i<=500:
                #if w*h>=33120:
                idc, conf= recogniser.predict(gray[y:y+h,x:x+w])
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                if conf<50: #and conf<=85:
                    co1+=1
                        #np.append(ids,idc)
                else:
                    co2+=1
            else:
                break 
        cv2.imshow("img",im)
        cv2.waitKey(5000)
        if(co1>co2):
            cam.release()
            cv2.destroyAllWindows()
            
            win32api.MessageBox(0, 'Face matched!!', 'SUCCESS!!', 0x00001000) 
            return "1"
        else:
            cam.release()
            cv2.destroyAllWindows()
            return "0"
            

def blinking():
    be1=0
    font = cv2.FONT_HERSHEY_PLAIN
    detects = dlib.get_frontal_face_detector()
    predicts = dlib.shape_predictor(r"C:\Users\Shantanu Shukla\djangoProject\pages\shape_predictor_68_face_landmarks.dat")
    capt= cv2.VideoCapture(0)
    for ii in range(1,100):
        ret,frame = capt.read()
        if ret is True:
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        else:
            continue
        faces1 = detects(gray)
        for face in faces1:
            landmarks = predicts(gray, face)
            left_eyes_ratio = gets_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eyes_ratio = gets_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eyes_ratio + right_eyes_ratio) / 2
            if blinking_ratio > 4:
                be1+=1
            #    cv2.putText(im, "BLINKING", (50, 150), font, 7, (255, 0, 0))
        cv2.imshow("Frame",frame)
    if(be1<1):
        return "0"   
    else:
        return "1"




def send_SMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def otp(apikey, numbers, sender, message):   
	resp =  send_SMS(apikey, numbers, sender, message)



	