import cv2
import numpy as np

def trial():
    TOLX = 10
    TOLY = 40
    frame = cv2.imread('avisa1.jpg')
    ex1, ex2, ey1, ey2 = 214, 274, 200, 360
    eyes = frame[ex1-TOLX:ex2+TOLX, ey1-TOLY:ey2+TOLY]
    #eye2 = frame[214:274, 300:360]

    glass = cv2.imread('glasses2.png')
    glass2 = cv2.resize(glass, dsize=(ey2-ey1 + TOLY*2, ex2-ex1 + TOLX*2))

    result = cv2.addWeighted(glass2, 0.1, eyes, 0.5, 0)

    frame[ex1 - TOLX:ex2 + TOLX, ey1 - TOLY:ey2 + TOLY] = result

    cv2.imshow("Eyes", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def overlayer():
    TOLX = 10
    TOLY = 40
    glass = cv2.imread('glasses_overlay.png')
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
    )

    frame = cv2.imread('avisa1.jpg')

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y: y + h, x: x + w]
        roi_color = frame[y: y + h, x: x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # try to put glasses instead of rectangle
            glass2 = cv2.resize(glass, dsize=(ew, eh))
            eyes = frame[ex - TOLX:ew + TOLX, ey - TOLY:eh + TOLY]
            result = cv2.addWeighted(glass2, 0.1, eyes, 0.5, 0)
            # frame[ey:ey + eh, ex:ex + (ew*2)] = glass2
            frame[ex:ex + ew, ey:ey + eh] = result
            cv2.rectangle(
                roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
            )
            break
    # display the frame
    cv2.imshow("Filter", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     break

overlayer()