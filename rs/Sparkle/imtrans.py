import numpy as np

def GCN(image: np.ndarray, s: float, λ: float, ϵ: float) -> np.ndarray:
    '''
    Apply Global Contrast Normalization
    reference: Ian, Deep Learning
    '''
    return s * (image - image.mean()) / np.max((ϵ,
           np.sqrt(λ + ((image - image.mean())**2).mean())))

