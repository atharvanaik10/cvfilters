import cv2
import nanocamera as nano

def glasses():
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
    )
    # Create the Camera instance
    camera = nano.Camera(flip=0, width=640, height=480, fps=30)
    print('CSI Camera status: ', camera.isReady())
    while camera.isReady():
        try:
            # read the camera image
            frame = camera.read()
            #convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #detect faces
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y: y + h, x: x + w]
                roi_color = frame[y: y + h, x: x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(
                        roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                    )
            # display the frame
            cv2.imshow("Filter", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()
    # close the camera instance
    camera.release()

    # remove camera object
    del camera

if __name__ == '__main__':
    glasses()
