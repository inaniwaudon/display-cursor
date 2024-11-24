import cv2
import dlib
import imutils
import numpy as np
from imutils import face_utils


class FaceDetector:
    DEVICE_ID = 1
    PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat"

    capture = cv2.VideoCapture(DEVICE_ID)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

    def __init__(self):
        self.feature_points = None

    # 特徴点を取得
    def _get_feature_points(self):
        return np.array([
            self.shape[31 - 1], # 鼻
            self.shape[37 - 1], # 左目
            self.shape[46 - 1], # 右目
            self.shape[9 - 1],  # 顎
            self.shape[49 - 1], # 左口角
            self.shape[55 - 1], # 右口角
            self.shape[1 - 1],  # 左顔輪郭
            self.shape[17 - 1]  # 右顔輪郭
        ], dtype="double")

    # 頭部方向を計算
    def calculate_angle(self, current_feature_points):
        focal_length = self.frame.shape[1]
        center = (self.frame.shape[1] // 2, self.frame.shape[0] // 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")
        dist_coeffs = np.zeros((4, 1), dtype="double")

        _, rotation_vector, translation_vector = cv2.solvePnP(
            self.feature_points,
            current_feature_points,
            camera_matrix,
            dist_coeffs,
        )
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        mat = np.hstack((rotation_matrix, translation_vector))
        _, _, _, _, _, _, eulerAngles = cv2.decomposeProjectionMatrix(mat)
        yaw = eulerAngles[1]
        pitch = eulerAngles[0]
        roll = eulerAngles[2]
        return yaw, pitch, roll

    def main(self):
        ret, frame = self.capture.read()
        if not ret:
            print("Failed to capture image")
            return

        frame = imutils.resize(frame, width=1000)
        self.frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # 顔およびランドマークの検出
        rects = self.detector(gray, 0)
        if len(rects) != 1:
            print("Only one face can be detected")
            return

        rect = rects[0]
        shape = self.predictor(gray, rect)
        self.shape = face_utils.shape_to_np(shape)
        for (x, y) in self.shape:
            cv2.circle(self.frame, (x, y), 1, (255, 255, 255), -1)

        if self.feature_points is None:
            self.feature_points = self._get_feature_points()
            new_column = [[0], [-60], [-120], [-120], [-130], [-130], [-150], [-150]]
            self.feature_points = np.append(self.feature_points, new_column, axis=1)
            print("Deletection of reference points is completed")

        current_feature_points = self._get_feature_points()
        yaw, pitch, roll = self.calculate_angle(current_feature_points)
        cv2.putText(
            self.frame,
            f"{yaw} {pitch} {roll}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255)
        )
        return yaw, pitch, roll
