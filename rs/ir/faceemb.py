'''
ArcFace embedding extraction using ONNX model.

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
from tqdm import tqdm


class ArcFace:
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
    
    def preprocess(self, img):
        img = cv2.resize(img, self.input_size)
        blob = cv2.dnn.blobFromImage(img,
                                1.0 / self.input_std, self.input_size,
                                (self.input_mean, self.input_mean, self.input_mean),
                                swapRB=True)
        return blob

    def embedding(self, img: str):
        img = self.read_image(img)
        blob = self.preprocess(img)
        net_out = self.session.run(self.output_names, {self.input_name: blob})[0]
        return net_out

    def __call__(self, img: str) -> np.ndarray:
        return self.embedding(img).ravel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', required=True, help='Path to source image directory')
    parser.add_argument('--destination', '-d', required=True, help='Path to destination output directory')
    parser.add_argument('--glob', '-g', help='Glob pattern', default='*.png')
    parser.add_argument('--model_path', type=str, default='webface_r50.onnx')
    args = parser.parse_args()

    arcface = ArcFace(args.model_path)
    os.makedirs(args.destination, exist_ok=True)
    images = glob.glob(os.path.join(args.source, args.glob))
    for img in tqdm(images):
        emb = arcface(img)
        output_path = os.path.join(args.destination, os.path.basename(img).split('.')[0] + '.npy')
        np.save(output_path, emb)
