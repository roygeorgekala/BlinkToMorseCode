import cv2
#import numpy as np


capture = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

testing = []

while True:
    ret, frame = capture.read()

    # Flipping image to ensure mirroring
    frame = cv2.flip(frame, 1)

    # Height and width of video feed
    width = int(capture.get(3))
    height = int(capture.get(4))

    # Grayscale image for facial  detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, 1.2, 3)

    # TODO: Change from for loops to just singular, skips for if more than one face detected
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 3)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Rectangle for showing outputs
    cv2.rectangle(frame, (10, height - 60),
                  (width-10, height-10), (255, 0, 0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # What is to be displayed
    content = 'FPS:' + str(capture.get(cv2.CAP_PROP_FPS))

    cv2.putText(frame, content, (50, height-20), font, 0.5,
                (0, 0, 0), 1, lineType=cv2.LINE_AA)
    # Frame resizing to make the output look bigger
    frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
    cv2.imshow("Camera output", frame)

    # Wait until Q is pressed to exit the application
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
