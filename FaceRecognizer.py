try:
    import os
    import cv2               # sudo pip3 install opencv_contrib_python; dependencies include numpy and dlib
    import numpy as np
    import face_recognition  # sudo pip3 install face_recognition
except Exception as e:
    print(e)

def getCameraVideo(*args, **kwargs):
    try:
        src = kwargs.get("source", 0)
        print("VideoSrc="+str(src))
        vid = cv2.VideoCapture(src)
        if vid is not None:
            try:
                fps = vid.get(cv2.CV_CAP_PROP_FPS)
            except Exception as a:
                try:
                    print("vid.get(cv2.CV_CAP_PROP_FPS) : " + str(a))
                    fps = vid.get(cv2.CAP_PROP_FPS)
                except Exception as b:
                    print("vid.get(cv2.CAP_PROP_FPS) : " + str(b))
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

                        try:
                            facesCurFrame = face_recognition.face_locations(grayframe)[0]
                            cv2.rectangle(original,(facesCurFrame[3],facesCurFrame[0]),(facesCurFrame[1],facesCurFrame[2]),(0,255,0),2)
                        except Exception as fe:
                            print(str(fe))
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

def main():
    getCameraVideo()

if __name__ == "__main__":
    main()