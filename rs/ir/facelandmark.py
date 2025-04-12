"""Extract face landmarks."""
import os
import cv2
import dlib
import numpy as np
import argparse
import glob
import tqdm
import pickle
from PIL import Image, ImageDraw
import concurrent.futures
import functools

def get_landmark(image: str, detector, predictor,
                 visualize: bool = False,
                 visualize_path: str = None,
                 save: bool = False,
                 save_path: str = None,
                 verbose: bool = False,
                 ) -> np.ndarray:
    landmarks = []
    img = dlib.load_rgb_image(image)
    dets = detector(img, 1)

    if visualize:
        im = Image.open(image).convert('RGB')
        draw = ImageDraw.Draw(im)

    for k, d in enumerate(dets):
        if verbose:
            print('detection:', d.left(), d.top(), d.right(), d.bottom())
        if visualize:
            draw.rectangle([d.left(), d.top(), d.right(), d.bottom()], fill=None, outline='red', width=2)
        shape = predictor(img, d)
        if verbose:
            print('parts:', shape.part(0), shape.part(1))
        for i in range(68):
            landmarks.append([shape.part(i).x, shape.part(i).y])
            if visualize:
                draw.circle([shape.part(i).x, shape.part(i).y], 3, fill='red')
        break  # we only use one face

    if len(landmarks) == 0:
        return None
    landmarks = np.array(landmarks)
    assert landmarks.shape == (68, 2), f'{landmarks.shape}'

    if save:
        basename = os.path.basename(image).replace('.png', '.npy')
        save_dest = os.path.join(save_path, basename)
        np.save(save_dest, landmarks)

    if visualize:
        basename = os.path.basename(image)
        vis_dest = os.path.join(visualize_path, basename)
        im.save(vis_dest)

    return os.path.basename(image), landmarks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', '-s', type=str, default='FFHQ/images512x512')
    parser.add_argument('--dst', '-d', type=str, default='FFHQ/landmarks.npy')
    parser.add_argument('--individual', action='store_true', help='dump individual landmarks')
    parser.add_argument('--individual_dst', type=str, default='FFHQ/landmarks')
    parser.add_argument('--glob', '-g', type=str, default='*.png')
    parser.add_argument('--vis', action='store_true', help='dump visualization')
    parser.add_argument('--vis_path', type=str, default='FFHQ/landmarks_vis')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--jobs', '-j', type=int, default=8)
    args = parser.parse_args()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    os.makedirs(args.vis_path, exist_ok=True)
    os.makedirs(args.individual_dst, exist_ok=True)

    images = glob.glob(os.path.join(args.src, args.glob))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        func = functools.partial(get_landmark,
                                 detector=detector,
                                 predictor=predictor,
                                 visualize=args.vis,
                                 visualize_path=args.vis_path,
                                 save=args.individual,
                                 save_path=args.individual_dst,
                                 verbose=args.verbose)
        results = list(tqdm.tqdm(executor.map(func, images), total=len(images)))

    fn2lm = dict()
    for pack in results:
        if pack is None:
            continue
        fn, lm = pack
        fn2lm[fn] = lm
    print('valid landmark detections:', len(fn2lm))

    print('dealing with failed ones')
    avg_lm = np.mean([v for v in fn2lm.values() if v is not None], axis=0)
    assert avg_lm.shape == (68, 2)
    for image in images:
        key = os.path.basename(image)
        if key not in fn2lm:
            fn2lm[key] = avg_lm

            basename = key.replace('.png', '.npy')
            save_dest = os.path.join(args.individual_dst, basename)
            np.save(save_dest, avg_lm)

    with open(args.dst, 'wb') as f:
        pickle.dump(fn2lm, f)
    print('landmarks saved to:', args.dst)