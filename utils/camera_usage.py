from datetime import datetime
import cv2 as cv

session_in_progress = False

def capture_camera():

    global session_in_progress
    vid = cv.VideoCapture(0)

    # cv.namedWindow("Photo Booth", cv.WINDOW_NORMAL)
    # cv.setWindowProperty("Photo Booth", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    ret, frame = vid.read()
    screen_center = (int(vid.get(3)/2), int(vid.get(4)/2))

    while True:
         
        ret, frame = vid.read()

        if not ret:
            print('Could not receive the stream. Exiting...')
            break

        font = cv.FONT_HERSHEY_PLAIN

        cv.putText(frame,  
                'Press space to start',  
                screen_center,  
                font, 2,  
                (255, 255, 255),  
                2) 

        cv.imshow('Photo Booth', frame)

        key = cv.waitKey(1)

        if key == ord('q'):
            print('Exiting due to user interaction...')
            break
            
        if key == ord(' '):
            if not session_in_progress:
                session_in_progress = True
                print('Photo session started ' + str(datetime.now()))

                # session here

    vid.release()
    cv.destroyAllWindows()
         
capture_camera()