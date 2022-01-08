import cv2

# initializing modifiable values
CAMERA_INPUT = 0  # Select which camera to use, 0 usually works for inbuilt webcams

# Number of frames at 30fps where closed eyes indicate short blink aka a dot
SHORT_BLINK_THRESHOLD = 3
# Number of frames at 30fps where closed eyes indicate long blink aka a dash
LONG_BLINK_THRESHOLD = 12

FACE_HAAR_CASCADE = "haarcascade_frontalface_alt2.xml"
EYE_HAAR_CASCADE = "haarcascade_eye_tree_eyeglasses.xml"


# Initializing working variables (Non Modifiable)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + FACE_HAAR_CASCADE)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + EYE_HAAR_CASCADE)
frame_count = 0
long_blink_count = 0
short_blink_count = 0
short_blink_status = True
long_blink_status = True


# Initalizing the video camera output
capture = cv2.VideoCapture(CAMERA_INPUT)

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

    # Blink Detection algorithm
    if len(faces) > 0:
        if len(eyes) == 0:
            frame_count += 1
        else:
            frame_count = 0
            short_blink_status = True
            long_blink_status = True

        if frame_count > SHORT_BLINK_THRESHOLD and short_blink_status:
            short_blink_count += 1
            short_blink_status = False

        elif long_blink_status and frame_count > LONG_BLINK_THRESHOLD:
            long_blink_status = False
            short_blink_count -= 1
            long_blink_count += 1
            frame_count = 0

    # Rectangle for showing outputs
    cv2.rectangle(frame, (10, height - 60),
                  (width-10, height-10), (255, 0, 0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Displayed information on the screen
    content = 'FPS:' + str(capture.get(cv2.CAP_PROP_FPS))
    content += " || Eye Closed Time: " + \
        str("%.3f" % (frame_count * (1.0/30))) + " ms"
    content += " || Long Blinks: " + str(long_blink_count)
    content += " || Short Blinks: " + str(short_blink_count)

    cv2.putText(frame, content, (50, height-20), font, 0.4,
                (0, 0, 0), 1, lineType=cv2.LINE_AA)

    # Frame resizing to make the output look bigger
    frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
    cv2.imshow("Camera output", frame)

    # Wait until Q is pressed to exit the application
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
