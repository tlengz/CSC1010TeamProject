try:
    import cv2
    import numpy as np
except Exception as e:
    print(e)


def getCameraVideo(*args, **kwargs):
    try:
        src = kwargs.get("source", 0)
        vid = cv2.VideoCapture(src)
        if vid is not None:
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
                        cv2.imshow("frame", grayframe)

                    if cv2.waitKey(spf) & 0xFF == ord("q"):
                        break
                    else:
                        rawframe1 = rawframe2
                        success1 = success2
                except Exception as exc:
                    print(str(exc))
    except Exception as e:
        print(str(e))

def main():
    getCameraVideo()

if __name__ == "__main__":
    main()