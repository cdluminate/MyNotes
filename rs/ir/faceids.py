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

    def embedding(self, img):
        img = cv2.resize(img, self.input_size)
        blob = cv2.dnn.blobFromImage(img,
                                     1.0 / self.input_std, self.input_size,
                                     (self.input_mean, self.input_mean, self.input_mean),
                                     swapRB=True)
        net_out = self.session.run(self.output_names, {self.input_name: blob})[0]
        return net_out

    def __call__(self, img1, img2):
        if isinstance(img1, str):
            img1 = self.read_image(img1)
        if isinstance(img2, str):
            img2 = self.read_image(img2)
        emb1 = self.embedding(img1).ravel()
        emb2 = self.embedding(img2).ravel()
        # cosine similarity
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def reload_and_call(self, img1, img2):
        # for thread safety
        sess = ort.InferenceSession(self.model_path)
        return self(img1, img2, sess)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', '-r', help='Path to reference image(s)')
    parser.add_argument('--generated', '-g', help='Path to generated image(s)')
    parser.add_argument('--glob', default='*.png', help='Glob pattern for images in directories')
    args = parser.parse_args()

    ids = IDS()
    if os.path.isfile(args.reference) and os.path.isfile(args.generated):
        # two image files: compare them and report score
        print(ids(args.reference, args.generated))
    elif os.path.isdir(args.reference) and os.path.isdir(args.generated):
        # two directories: compare all pairs of images and report scores
        generated = glob.glob(os.path.join(args.generated, args.glob))
        references = [os.path.join(args.reference, os.path.basename(gen)) for gen in generated]

        scores = []
        for ref, gen in zip(references, generated):
            score = ids(ref, gen)
            scores.append(score)
            print('Ref=', ref, 'Gen=', gen, 'IDS=', score)
        print('Mean IDS=', np.mean(scores))
