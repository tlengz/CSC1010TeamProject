try:
    import os
    import cv2               # sudo pip3 install opencv_contrib_python; dependencies include numpy and dlib - DO NOT INSTALL opencv-python
    import numpy as np
    #import face_recognition  # sudo pip3 install face_recognition
    from PIL import Image
    import threading
    import queue
    import paho.mqtt.publish as publish
    import paho.mqtt.client as mqtt
    from   gpiozero import LED
except Exception as e:
    print(e)
#---------------------------------------------------------------------------------------------------------------------  
def TrainModel():
    BASEDIR = '/home/pi/Documents/CSC1010/images'
    names = []
    paths = []
    for users in os.listdir(BASEDIR):
        names.append(users)
        #print(users)
    for name in names:
        for image in os.listdir(BASEDIR + "/" + name ):
            path_string = os.path.join(BASEDIR + "/" + name, image)
            paths.append(path_string)
            #print(path_string)
    faces = []
    ids = []
    for image_path in paths:
        image = Image.open(image_path).convert("L")
        imageNp = np.array(image,"uint8")
        faces.append(imageNp)
        id = int(image_path.split("/")[7].split("_")[0])
        #print(id)
        ids.append(id)
    ids = np.array(ids)
    trainer = cv2.face.LBPHFaceRecognizer_create()  # pip3 install opencv-contrib-python
    trainer.train(faces,ids)
    trainer.write("training.yml")
    print("Model trained")
#---------------------------------------------------------------------------------------------------------------------
quitVideo    = False
resizedQueue = queue.Queue()
colorQueue   = queue.Queue()
grayQueue    = queue.Queue()
profileQueue = queue.Queue()
outputQueue  = queue.Queue()
Recognized   = False
Who          = "No one is at the door"
led = LED(17)
ip_address = "192.168.156.141"
#---------------------------------------------------------------------------------------------------------------------
def resize(vid,width,height):
    global quitVideo
    global resizedQueue
    if vid.isOpened():
        while not quitVideo and vid.isOpened():
            try:
                success, original = vid.read()
                if success:
                    resized = cv2.resize(original, (width,height))
                    resizedQueue.put(resized)
            except Exception as e:
                print("resize() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------
def rgb(vid):
    global quitVideo
    global resizedQueue
    global grayQueue
    global colorQueue
    if vid.isOpened():
        while not quitVideo and vid.isOpened():
            try:
                if resizedQueue.qsize() > 0:
                    resized = resizedQueue.get()
                    resizedQueue.task_done()
                    grayframe  = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                    colorframe = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                    grayQueue.put(grayframe)
                    colorQueue.put(colorframe)
            except Exception as e:
                print("rgb() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------                
def saveface(vid,destination):
    global quitVideo
    global profileQueue
    if vid.isOpened() :
        BASEDIR = '/home/pi/Documents/CSC1010/images'
        #BASEDIR = os.path.dirname(os.path.abspath(__file__))
        SaveFolder = BASEDIR + "/" + destination + "/"
        counter = 128
        limit = counter + 50
        while not quitVideo and vid.isOpened() :
            if profileQueue.qsize() > 0 and counter < limit:
                profileframe = profileQueue.get()
                profileQueue.task_done()
                imgName = SaveFolder + "1_" + str(counter) + ".jpg"
                cv2.imwrite(imgName, profileframe)
                print(imgName + " saved.")
                counter += 1
#---------------------------------------------------------------------------------------------------------------------
def recognizeface(vid,face_cascade,face_recognizer):
    global quitVideo
    #global profileQueue
    global grayQueue
    global colorQueue
    global outputQueue
    global Recognized
    global Who
    if vid.isOpened() and face_cascade != None and face_recognizer != None:
        face_recognizer.read("./training.yml")
        person = ["","Kee Boon Hwee","Teo Leng"]
        
        while not quitVideo and vid.isOpened():
            try:
                if colorQueue.qsize() > 0 and grayQueue.qsize() > 0:
                    colorframe = colorQueue.get()
                    grayframe  = grayQueue.get()
                    colorQueue.task_done()
                    grayQueue.task_done()
                    try:
                        faces = face_cascade.detectMultiScale( grayframe, scaleFactor=1.1, minNeighbors=3 )
                        if len(faces) > 0 :
                            #print("There are " + str(len(faces)) +  " face(s)")
                            for (x,y,w,h) in faces:
                                color = (0,0,255)
                                personName = "Unknown"
                                croppedGrayImage = grayframe[y:y+h , x:x+w]
                                grayProfile = cv2.resize(croppedGrayImage, (400,368))
                                
                                #profileQueue.put(grayProfile)
                                _id, _confidence = face_recognizer.predict(grayProfile)
                                if _id and _confidence <= 39.0:
                                    color = (0,255,0)
                                    personName = person[_id]
                                    #print(str(_id) + " = " + str(_confidence))
                                    if Recognized == False:
                                        Recognized = True
                                        Who = personName + " is at the door"
                                        publish.single(topic="Doorbell", payload=Who, retain=True, hostname=ip_address,port=1883,keepalive=5)
                                        led.on()
                                        print(Who)
                                else:
                                    if Recognized == True:
                                        Recognized = False
                                        Who = "Unknown person(s) is at the door"
                                        publish.single(topic="Doorbell", payload=Who, retain=True, hostname=ip_address,port=1883,keepalive=5)
                                        led.off()
                                        print(Who)
                                    else:
                                        Who = "Unknown person(s) is at the door"
                                        publish.single(topic="Doorbell", payload=Who, retain=True, hostname=ip_address,port=1883,keepalive=5)
                                        led.off()
                                        
                                cv2.rectangle(colorframe,(x,y),(x+w,y+h),color,2)
                                cv2.putText(colorframe,personName,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
                        else:
                            if Who != "No one is at the door":
                                Recognized = False
                                Who = "No one is at the door"
                                publish.single(topic="Doorbell", payload=Who, retain=True, hostname=ip_address,port=1883,keepalive=5)
                                led.off()
                                print(Who)

                            #print("There are no faces")
                        
                    except Exception as f:
                        print("face_cascade : " + str(f))

                    outputQueue.put(colorframe)
            except Exception as e:
                print("recognizeface() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------
def output(vid):
    global quitVideo
    global outputQueue
    if vid.isOpened():
        while not quitVideo and vid.isOpened():
            try:
                if outputQueue.qsize() > 0:
                    output = outputQueue.get()
                    outputQueue.task_done()
                    cv2.imshow("Output", output)
            except Exception as e:
                print("output() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------
def userQuit(vid):
    global quitVideo
    if vid.isOpened():
        while not quitVideo and vid.isOpened():
            try:
                if  cv2.waitKey(1) & 0xFF == ord("q"):
                    quitVideo = True
                    break
            except Exception as e:
                print("userQuit() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------
def getCameraVideo():
    try:
        vid = cv2.VideoCapture(0)
        try:
            if vid != None and vid.isOpened():
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
                #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                if face_cascade != None and not face_cascade.empty():
                    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
                    if face_recognizer != None:
                        try:
                            #-------------------------------------------------------------------------------
                            resizeThread    = threading.Thread(target = resize            , args=[vid,400,368]                      )
                            rgbThread       = threading.Thread(target = rgb               , args=[vid]                              )
                            recognizefaceThread = threading.Thread(target = recognizeface , args=[vid,face_cascade,face_recognizer] )
                            #saveFaceThread  = threading.Thread(target = saveface         , args=[vid,"Kee Boon Hwee"]              )
                            outputThread    = threading.Thread(target = output            , args=[vid]                              )
                            userQuitThread  = threading.Thread(target = userQuit          , args=[vid]                              )
                            #-------------------------------------------------------------------------------
                            resizeThread.start()
                            rgbThread.start()
                            recognizefaceThread.start()
                            #saveFaceThread.start()
                            outputThread.start()
                            userQuitThread.start()
                            #-------------------------------------------------------------------------------
                            resizeThread.join()
                            rgbThread.join()
                            recognizefaceThread.join()
                            #saveFaceThread.join()
                            outputThread.join()
                            userQuitThread.join()
                            #-------------------------------------------------------------------------------
                        except Exception as e:
                            print("getCameraVideo() : " + str(e))
                    else:
                        print("cv2.face.LBPHFaceRecognizer_create is not ready!")
                else:
                    print("cv2.CascadeClassifier is not ready!")
        except Exception as f:
            print("" + str(f))
    except Exception as e:
        print("cv2.VideoCapture() exception" + str(e))
       
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
def main():
    #TrainModel()
    getCameraVideo()
#---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------