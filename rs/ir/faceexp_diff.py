'''
Calculate brightness difference.
$ pip install git+https://github.com/openai/CLIP.git
'''
import os
from PIL import Image
import argparse
import glob
import torch
import clip
import functools as ft


FACEEXPS = [
    'neutral', 'happy', 'sad', 'angry',
    'surprised', 'disgusted', 'fearful', 'concempt', 
]


def load_clip_model():
    """
    Load the CLIP model and return the model and preprocess function.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

def classify_faceexp(model, preprocess, device, image_path: str):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text = clip.tokenize(FACEEXPS).to(device)

    with torch.no_grad():
        #image_features = model.encode_image(image)
        #text_features = model.encode_text(text)

        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    #print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]
    argmax = probs.argmax(axis=1)[0]
    label = FACEEXPS[argmax]
    return label

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--reference', type=str, required=True)
    parser.add_argument('--glob', type=str, default='*.png',
                        help='Glob pattern for image files in directory')
    args = parser.parse_args()

    model, preprocess, device = load_clip_model()
    get_faceexp = ft.partial(classify_faceexp, model, preprocess, device)

    if os.path.isdir(args.image):
        images = glob.glob(os.path.join(args.image, args.glob))
        for image in images:
            faceexp = get_faceexp(image)
            basename = os.path.basename(image)
            ref_path = os.path.join(args.reference, basename)
            ref_faceexp = get_faceexp(ref_path)
            print('Faceexp-diff:', basename, faceexp == ref_faceexp, faceexp, ref_faceexp)
    else:
        faceexp = get_faceexp(args.image)
        basename = os.path.basename(args.image)
        ref_faceexp = get_faceexp(args.reference)
        print('Faceexp-diff:', basename, faceexp == ref_faceexp, faceexp, ref_faceexp)

