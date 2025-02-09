'''
Calculate face pose.
Yaw (left, right), pitch (up, down), roll (rotate).
'''
import cv2
import dlib
import numpy as np
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    args = parser.parse_args()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    img = cv2.imread(args.image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    #print(faces)

    for face in faces:
        landmarks = predictor(gray, face)

        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)
        nose = (landmarks.part(30).x, landmarks.part(30).y)
        mid_x = (left_eye[0] + right_eye[0]) / 2
        yaw_ratio = (nose[0] - mid_x) / (right_eye[0] - left_eye[0])
        yaw_angle = yaw_ratio * 90 
        print(f'yaw: {yaw_angle}')
