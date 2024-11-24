import cv2
from argparse import ArgumentParser
from face import FaceDetector
from cursor import CursorController


PITCH_THRESHOLD = (10, 18)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--frame", type=bool, default=False)
    args = parser.parse_args()

    face = FaceDetector()
    cursor = CursorController()

    while(True):
        result = face.main()
        if result is None:
            continue
        yaw, pitch, roll = result

        if args.frame:
            cv2.imshow("Frame", face.frame)
            cv2.waitKey(1)

        if pitch < PITCH_THRESHOLD[0]:
            cursor.switch(0)
        if pitch > PITCH_THRESHOLD[1]:
            cursor.switch(1)

    capture.release()
    cv2.destroyAllWindows()
