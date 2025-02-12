'''
IDS for face recognition.
Compare the same file name under two folders, a/face1.png and b/face1.png
We assume the faces are already aligned.

Reference:
https://github.com/deepinsight/insightface/blob/master/python-package/insightface/model_zoo/arcface_onnx.py
https://github.com/ChiWeiHsiao/ref-ldm/blob/main/ldm/modules/losses/identity_loss.py

Requires webface_r50.onnx downloaded from the insightface model zoo:
https://drive.google.com/file/d/1N0GL-8ehw_bz2eZQWz2b0A5XBdXdxZhg/view?usp=sharing
https://github.com/deepinsight/insightface/tree/master/model_zoo
'''

import os
import numpy as np
import cv2
import onnx
import onnxruntime as ort
import argparse
import glob
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor


class IDS:
    def __init__(self, model_path='webface_r50.onnx'):
        self.model_path = model_path
        self.input_mean = 127.5
        self.input_std = 127.5
        self.session = ort.InferenceSession(self.model_path)
        input_cfg = self.session.get_inputs()[0]
        self.input_name = input_cfg.name
        self.input_size = tuple(input_cfg.shape[2:4][::-1])
        self.input_shape = input_cfg.shape
        outputs = self.session.get_outputs()
        self.output_names = [output.name for output in outputs]
        assert len(self.output_names) == 1
        self.output_shape = outputs[0].shape

    def read_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Image at {img_path} could not be read.")
        return img

    def embedding(self, img, session=None):
        img = cv2.resize(img, self.input_size)
        blob = cv2.dnn.blobFromImage(img,
                                     1.0 / self.input_std, self.input_size,
                                     (self.input_mean, self.input_mean, self.input_mean),
                                     swapRB=True)
        if session is None:
            net_out = self.session.run(self.output_names, {self.input_name: blob})[0]
        else:
            net_out = session.run(self.output_names, {self.input_name: blob})[0]
        return net_out

    def __call__(self, img1, img2, session=None):
        if isinstance(img1, str):
            img1 = self.read_image(img1)
        if isinstance(img2, str):
            img2 = self.read_image(img2)
        emb1 = self.embedding(img1, session).ravel()
        emb2 = self.embedding(img2, session).ravel()
        # cosine similarity
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def reload_and_call(self, img1, img2):
        # for thread safety
        sess = ort.InferenceSession(self.model_path)
        return self(img1, img2, sess)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('img1', help='Path to first image (target)')
    parser.add_argument('img2', help='Path to second image (ref1)')
    parser.add_argument('--img2postfix', type=str, default='.png')
    parser.add_argument('img3', help='Path to third image (ref2)')
    parser.add_argument('--img3postfix', type=str, default='.png')
    parser.add_argument('img4', help='Path to fourth image (ref3)')
    parser.add_argument('--img4postfix', type=str, default='.png')
    args = parser.parse_args()

    ids = IDS()

    assert os.path.isdir(args.img1)
    assert os.path.isdir(args.img2)
    assert os.path.isdir(args.img3)
    assert os.path.isdir(args.img4)

    targets = glob.glob(os.path.join(args.img1, '*.png'))
    ref1 = [os.path.join(args.img2, os.path.basename(target)) for target in targets]
    ref1 = [x[:-4] + args.img2postfix for x in ref1]
    ref2 = [os.path.join(args.img3, os.path.basename(target)) for target in targets]
    ref2 = [x[:-4] + args.img3postfix for x in ref2]
    ref3 = [os.path.join(args.img4, os.path.basename(target)) for target in targets]
    ref3 = [x[:-4] + args.img4postfix for x in ref3]

    scores_mean = []
    scores_min = []
    scores_max = []
    for tar, r1, r2, r3 in zip(targets, ref1, ref2, ref3):
        s1 = ids(r1, tar)
        s2 = ids(r2, tar)
        s3 = ids(r3, tar)
        score_min = min(s1, s2, s3)
        score_mean = (s1 + s2 + s3) / 3
        score_max = max(s1, s2, s3)
        scores_mean.append(score_mean)
        scores_min.append(score_min)
        scores_max.append(score_max)

        print('Image:', tar, 'minIDS', score_min, 'meanIDS', score_mean, 'maxIDS', score_max)
    print('Mean minIDS=', np.mean(scores_min))
    print('Mean meanIDS=', np.mean(scores_mean))
    print('Mean maxIDS=', np.mean(scores_max))
