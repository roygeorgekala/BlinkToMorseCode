import cv2
import interpreter
import numpy as np
import threading as th
import time

# initializing modifiable values
CAMERA_INPUT = 0  # Select which camera to use, 0 usually works for in-built webcams

# Number of frames at 30fps where closed eyes indicate short blink aka a dot
SHORT_BLINK_THRESHOLD = 3
# Number of frames at 30fps where closed eyes indicate long blink aka a dash
LONG_BLINK_THRESHOLD = 8

# Duration of a break
IN_BETWEEN_THRESHOLD = 30

# The cascades are listed on https://github.com/opencv/opencv/tree/master/data/haarcascades
FACE_HAAR_CASCADE = "haarcascade_frontalface_alt2.xml"
EYE_HAAR_CASCADE = "haarcascade_eye_tree_eyeglasses.xml"

# Global Variables
CONTENT = ""
SUGGESTIONS = [""]*8


def get_content():
    global SUGGESTIONS
    while True:
        time.sleep(0.25)
        ret = interpreter.content_return(CONTENT)
        if len(ret) > 8:
            SUGGESTIONS = ret[:8]
        else:
            SUGGESTIONS[:len(ret)] = ret
            SUGGESTIONS[len(ret):] = [""]*(8-len(ret))
        # print(SUGGESTIONS)


def main():

    # Initializing working variables (Non Modifiable)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + FACE_HAAR_CASCADE)
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + EYE_HAAR_CASCADE)
    frame_count = 0
    open_eye_count = 0
    short_blink_status = True
    long_blink_status = True
    open_status = True
    read = ""
    global CONTENT
    content_thread = th.Thread(target=get_content)
    content_thread.daemon = True
    content_thread.start()
    # Initalizing the video camera output
    capture = cv2.VideoCapture(CAMERA_INPUT)

    # First Frame captured to retrieve height and width
    ret, frame = capture.read()

    # Height and width of video feed
    width = int(capture.get(3))
    height = int(capture.get(4))

    infoDisplayArea = []
    for i in range(0, int(height)):
        current = []
        for j in range(0, int(width/3)):
            if i % (height//8) == 0:
                current += [[0, 0, 0]]
            else:
                current += [[255, 255, 255]]

        infoDisplayArea += [current]

    infoDisplayArea = np.array(infoDisplayArea, dtype=np.uint8)

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

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray_frame[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 3)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (0, 255, 0), 2)

        # Blink Detection algorithm
        if len(faces) > 0:

            if len(eyes) == 0:
                # Increment number of frames where eyes have been closed
                frame_count += 1
                open_eye_count = 0
                open_status = True
            else:
                # Reset number of frames and blink status' when eyes are opened
                frame_count = 0
                short_blink_status = True
                long_blink_status = True
                open_eye_count += 1

                if open_eye_count > IN_BETWEEN_THRESHOLD and open_status:

                    CONTENT += interpreter.interpret(read.strip())
                    read = ""
                    open_status = False

            if short_blink_status and frame_count > SHORT_BLINK_THRESHOLD:
                read += ". "
                short_blink_status = False

            elif long_blink_status and frame_count > LONG_BLINK_THRESHOLD:
                long_blink_status = False
                read = read[:-2]+"_ "
                frame_count = 0

        # Rectangle for showing outputs
        cv2.rectangle(frame, (10, height - 60),
                      (width-10, height-10), (255, 255, 255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame, CONTENT+read, (50, height-20), font, 0.5,
                    (0, 0, 0), 1, lineType=cv2.LINE_AA)

        # Frame resizing to make the output look bigger
        frame = np.append(frame, infoDisplayArea, axis=1)
        frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)

        adder = frame.shape[0]//8
        cv2.putText(frame, "1. " + SUGGESTIONS[0], (int(width*1.5)+5, 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "2. " + SUGGESTIONS[1], (int(width*1.5)+5, adder+50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "3. " + SUGGESTIONS[2], (int(width*1.5)+5, 2*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "4. " + SUGGESTIONS[3], (int(width*1.5)+5, 3*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "5. " + SUGGESTIONS[4], (int(width*1.5)+5, 4*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "6. " + SUGGESTIONS[5], (int(width*1.5)+5, 5*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "7. " + SUGGESTIONS[6], (int(width*1.5)+5, 6*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "8. " + SUGGESTIONS[7], (int(width*1.5)+5, 7*adder + 50),
                    font, 0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)

        cv2.imshow("Camera output", frame)

        # Wait until Q is pressed to exit the application
        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
