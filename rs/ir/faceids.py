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
    parser.add_argument('img1', help='Path to first image')
    parser.add_argument('img2', help='Path to second image')
    parser.add_argument('--dump', '-d', action='store_true', help='Dump the ids')
    parser.add_argument('--jobs', '-j', type=int, default=1, help='Number of jobs')
    args = parser.parse_args()

    ids = IDS()

    if os.path.isfile(args.img1) and os.path.isfile(args.img2):
        # two image files: compare them and report score
        print(ids(args.img1, args.img2))
    elif os.path.isdir(args.img1) and os.path.isdir(args.img2):
        # two directories: compare all pairs of images and report scores
        targets = glob.glob(os.path.join(args.img2, '*.png'))
        references = [os.path.join(args.img1, os.path.basename(target)) for target in targets]
        if args.jobs > 1:
            print('onnxruntime session seems not thread safe, so we create a new session for each thread')
            with ThreadPoolExecutor(max_workers=args.jobs) as executor:
                scores = track(executor.map(ids.reload_and_call, references, targets), total=len(references))
            for ref, tar, score in zip(references, targets, scores):
                print('Ref=', ref, 'Tar=', tar, 'IDS=', score)
                if args.dump:
                    with open(tar + '.ids', 'w') as f:
                        f.write(f'{score}\n')
        else:
            scores = []
            for ref, tar in zip(references, targets):
                score = ids(ref, tar)
                scores.append(score)
                print('Ref=', ref, 'Tar=', tar, 'IDS=', score)
                if args.dump:
                    with open(tar + '.ids', 'w') as f:
                        f.write(f'{score}\n')
        print('Mean IDS=', np.mean(scores))
