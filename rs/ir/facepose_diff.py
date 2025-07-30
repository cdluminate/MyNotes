'''
Calculate face pose difference.
Yaw (left, right), pitch (up, down), roll (rotate).
'''
import os
import cv2
import dlib
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
    parser.add_argument('--reference', type=str, required=True)
    args = parser.parse_args()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    if os.path.isdir(args.image):
        images = glob.glob(os.path.join(args.image, '*.png'))
        for image in images:
            yaw_angle = get_yaw_angle(image, detector, predictor)
            basename = os.path.basename(image)
            ref_path = os.path.join(args.reference, basename)
            ref_angle = get_yaw_angle(ref_path, detector, predictor)
            print('Yaw angle diff:', abs(yaw_angle - ref_angle))
    else:
        yaw_angle = get_yaw_angle(args.image, detector, predictor)
        ref_angle = get_yaw_angle(args.reference, detector, predictor)
        print('Yaw angle diff:', abs(yaw_angle - ref_angle))

