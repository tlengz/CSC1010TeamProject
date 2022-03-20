import imutils   # sudo pip3 install imutils
from imutils.video import VideoStream

_height = 368
_width = 400
_resolution = (_height,_width)
cf = VideoStream( usePiCamera=True , resolution=_resolution , framerate=30 )
cf.start()

while True:
    frame = cf.read()


    """ def SaveFaces(key):
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
        print("SaveFaces() : " + str(e)) """
#---------------------------------------------------------------------------------------------------------------------
"""  """


    """ def displayVideo(vidSrc,spf):
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
            print(str(e)) """