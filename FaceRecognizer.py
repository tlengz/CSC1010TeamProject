try:
    import os
    import cv2               # sudo pip3 install opencv_contrib_python; dependencies include numpy and dlib - DO NOT INSTALL opencv-python
    import numpy as np
    #import face_recognition  # sudo pip3 install face_recognition
    from PIL import Image
    import threading
    import queue
except Exception as e:
    print(e)
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
def SaveFaces(key):
    try:
        vid          = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
        #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'lbpcascade_frontalface.xml')
        
        if face_cascade.empty():
            print("face is empty")

        if vid is not None and face_cascade is not None:
            BASEDIR = '/home/pi/Documents/CSC1010/images'
            #BASEDIR = os.path.dirname(os.path.abspath(__file__))
            SaveFolder = BASEDIR + "/" + key + "/"
            try:
                fps = vid.get(cv2.CV_CAP_PROP_FPS)
            except Exception as a:
                try:
                    fps = vid.get(cv2.CAP_PROP_FPS)
                except Exception as b:
                    fps = 1
            if fps > 1:
                spf = int(1000 / fps)
            else:
                spf = 1
            targetHeight = 360
            targetWidth  = 390
            if vid.isOpened:
                success, original = vid.read()
                if success:
                    try:
                        hT, wT, ct = original.shape
                        targetWidth = int(wT / hT * targetHeight)
                    except:
                        pass
            counter = 0
            while vid.isOpened():
                try:
                    success, original = vid.read()
                    if success:
                        grayframe = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
                        croppedImage = grayframe
                        faces = face_cascade.detectMultiScale(grayframe,scaleFactor=1.1,minNeighbors=4)
                        for (x,y,w,h) in faces:
                            try:
                                croppedImage = grayframe[y:y+h , x:x+w]
                            except Exception as ce:
                                pass
                        try:
                            hT, wT ,ct = croppedImage.shape
                            targetWidth = int(wT / hT * targetHeight)
                        except Exception as ed:
                            pass
                        try:
                            croppedImage  = cv2.resize(croppedImage, (targetWidth, targetHeight))
                            #pass
                        except Exception as er:
                            pass

                        if counter < 10:
                            imgName = SaveFolder + "img" + str(counter) + ".jpg"
                            cv2.imwrite(imgName, croppedImage)
                            print("Saving " + imgName)
                            counter += 1

                        cv2.imshow("frame", croppedImage)
                    if  cv2.waitKey(spf) & 0xFF == ord("q"):
                        break
                except Exception as exc:
                    print("vid.isOpened() : " + str(exc))
            vid.release()
            cv2.destroyAllWindows()
            print(SaveFolder)
    except Exception as e:
        print("SaveFaces() : " + str(e))
#---------------------------------------------------------------------------------------------------------------------
""" def TrainModel():
    BASEDIR = '/home/pi/Documents/CSC1010/images'
    names = []
    paths = []
    for users in os.listdir(BASEDIR):
        names.append(users)
    for name in names:
        for image in os.listdir(BASEDIR + "/" + name ):
            path_string = os.path.join(BASEDIR + "/" + name, image)
            paths.append(path_string)
    faces = []
    ids = []
    for image_path in paths:
        image = Image.open(image_path).convert("L")
        imageNp = np.array(image,"uint8")
        faces.append(imageNp)
        id = int(image_path.split("/")[7].split("_")[0])
        ids.append(id)
    ids = np.array(ids)
    trainer = cv2.face.LBPHFaceRecognizer_create()  # pip3 install opencv-contrib-python
    
    trainer.train(faces,ids)
    trainer.write("training.yml")
    print("Model trained") """
#---------------------------------------------------------------------------------------------------------------------
quitVideo = False
colorQueue = queue.Queue()
grayQueue  = queue.Queue()

def getCameraVideo():
    vid = cv2.VideoCapture(0)
    if vid != None:
        if vid.isOpened():
            success = False
            spf = 1
            targetHeight = 360
            targetWidth = 390
            while success != True:
                success, original = vid.read()

            try:
                fps = vid.get(cv2.CV_CAP_PROP_FPS)
            except:
                try:
                    fps = vid.get(cv2.CAP_PROP_FPS)
                except:
                    fps = 1
            if fps > 1:
                spf = int(1000 / fps)
            else:
                spf = 1
            
            try:
                hT, wT = original.shape
                targetWidth = int(wT / hT * targetHeight)
            except:
                pass
        inputStream = threading.Thread(target = getFrames,args=(vid,targetWidth,targetHeight))
        outputStream = threading.Thread(target = displayVideo,args=(vid,spf))
        inputStream.start()
        outputStream.start()
        inputStream.join()
        outputStream.join()
        vid.release()
        cv2.destroyAllWindows()
#---------------------------------------------------------------------------------------------------------------------
def getFrames(vidSrc,targetWidth,targetHeight):
    global quitVideo
    global colorQueue
    global grayQueue
    while not quitVideo and vidSrc.isOpened():
        try:
            success, original = vidSrc.read()
            if success:
                resizedImage  = cv2.resize(original, (targetWidth, targetHeight))
                rgbframe      = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
                grayframe     = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2GRAY)
                colorQueue.put(rgbframe)
                grayQueue.put(grayframe)
        except:
            pass
                        
def displayVideo(vidSrc,spf):
    global quitVideo
    global colorQueue
    global grayQueue
    face_cascade    = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    if face_cascade != None and face_recognizer != None:
        try:
            face_recognizer.read("./training.yml")
            names = ['Kee Boon Hwee']
            while not quitVideo and vidSrc.isOpened():
                try:
                    if colorQueue.qsize() > 0:
                        grayframe = grayQueue.get()
                        rgbframe = colorQueue.get()

                        faces = face_cascade.detectMultiScale(grayframe,scaleFactor=1.1,minNeighbors=4)
                        for (x,y,w,h) in faces:
                            try:
                                croppedGrayImage = grayframe[y:y+h , x:x+w]
                                id, confidence = face_recognizer.predict(croppedGrayImage)
                                color = (0,0,255)
                                if id:
                                    color = (0,255,0)
                                    cv2.putText(rgbframe,names[id - 1],(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
                                    print(str(id) + " = " + str(confidence))
                                else:
                                    cv2.putText(rgbframe,"Unknown",(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
                                cv2.rectangle(rgbframe,(x,y),(x+w,y+h),color,2)
                            except Exception as ce:
                                pass
                                
                        cv2.imshow("frame", rgbframe)
                    if  cv2.waitKey(spf) & 0xFF == ord("q"):
                        quitVideo = True
                except:
                    pass
        except Exception as e:
            print(str(e))
#---------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
def main():
    #getCameraVideo()
    SaveFaces("Kee Boon Hwee")
#---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------