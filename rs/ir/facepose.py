'''
Calculate face pose.
Yaw (left, right), pitch (up, down), roll (rotate).
'''
import os
import cv2
import dlib
import numpy as np
import argparse
import glob

def get_yaw_angle(image, detector, predictor) -> float:
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return 0.0
    face = faces[0]
    landmarks = predictor(gray, face)

    left_eye = (landmarks.part(36).x, landmarks.part(36).y)
    right_eye = (landmarks.part(45).x, landmarks.part(45).y)
    nose = (landmarks.part(30).x, landmarks.part(30).y)
    mid_x = (left_eye[0] + right_eye[0]) / 2
    yaw_ratio = (nose[0] - mid_x) / (right_eye[0] - left_eye[0])
    yaw_angle = yaw_ratio * 90 
    return yaw_angle


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    args = parser.parse_args()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    if os.path.isdir(args.image):
        images = glob.glob(os.path.join(args.image, '*.png'))
        for image in images:
            yaw_angle = get_yaw_angle(image, detector, predictor)
            print(image, 'Yaw angle:', yaw_angle)
            with open(image + '.yaw', 'wt') as f:
                f.write(str(yaw_angle))
    else:
        yaw_angle = get_yaw_angle(args.image, detector, predictor)
        print('Yaw angle:', yaw_angle)

