from collections import UserList


try:
    import os
    import cv2               # sudo pip3 install opencv_contrib_python; dependencies include numpy and dlib - DO NOT INSTALL opencv-python
    import numpy as np
    import face_recognition  # sudo pip3 install face_recognition
    from PIL import Image
except Exception as e:
    print(e)
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
def SaveFaces(key):
    try:
        vid          = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
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
                        hT, wT = original.shape
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
                            hT, wT = croppedImage.shape
                            targetWidth = int(wT / hT * targetHeight)
                        except Exception as ed:
                            pass
                        try:
                            croppedImage  = cv2.resize(croppedImage, (targetWidth, targetHeight))
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
        print("SaveFaces() : "+ str(e))
#---------------------------------------------------------------------------------------------------------------------
def getCameraVideo(*args, **kwargs):
    try:
        src = kwargs.get("source", 0)
        vid          = cv2.VideoCapture(src)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
        if vid is not None and face_cascade is not None:
            BASEDIR = os.path.dirname(os.path.abspath(__file__))  # /home/pi/Documents/CSC1010/CSC1010TeamProject

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
            success1, rawframe1 = vid.read()
            if success1:
                    hT, wT, cT = rawframe1.shape
                    targetHeight = 360
                    targetWidth = int(wT / hT * targetHeight)

            while vid.isOpened():
                try:
                    success2, rawframe2 = vid.read()
                    if success1 and success2:
                        original  = cv2.resize(rawframe1, (targetWidth, targetHeight))
                        grayframe = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(grayframe,scaleFactor=1.1,minNeighbors=4)
                        for (x,y,w,h) in faces:
                            cv2.rectangle(original,(x,y),(x+w,y+h),(0,255,0),2)

                        cv2.imshow("frame", original)

                    if cv2.waitKey(spf) & 0xFF == ord("q"):
                        break
                    else:
                        rawframe1 = rawframe2
                        success1 = success2
                except Exception as exc:
                    print("vid.isOpened() : " + str(exc))
            vid.release()
            cv2.destroyAllWindows()
    except Exception as e:
        print("getCameraVideo() : "+ str(e))
#---------------------------------------------------------------------------------------------------------------------
def TrainModel():
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
    print("Model trained")
#---------------------------------------------------------------------------------------------------------------------
def main():
    TrainModel()
#---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------