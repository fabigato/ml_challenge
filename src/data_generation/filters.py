from scipy.ndimage.filters import gaussian_filter
import numpy as np
import random


def blurr(img, metadata, sigma=1):
    """
    Gaussian noise
    :param img: image to apply noise to
    :param sigma: std of the gaussian
    :param metadata: dictionary to log configs of this transformation
    :return: blurred image
    """
    metadata['config']['sigma'] = sigma
    return gaussian_filter(img, sigma=sigma, order=0)


def pixel_noise(img, metadata, num_pixels, dark=True, seed=None):
    """
    applies noise to a set of pixels. The value of those pixels is set to black (i.e.
    highest value of the matrix)
    :param img: image to apply noise to
    :param metadata: dictionary to log configs of this transformation
    :param num_pixels: number of pixels to apply noise to
    :param dark: if True, the selected pixels are set to the highest value in the matrix. If false, each pixel is set
    to a random value in [0, 1]
    :param seed: this, along with the matrix dimensions, determines the pixels that will be changed. That is, given
    fixed dimensions, a given seed will always produce the same noise pattern. If None, a random seed will be used
    :return: noised matrix
    """
    img = np.array(img)
    indexes = [i for i in range(0, img.shape[0] * img.shape[1])]
    if seed:
        random.seed(seed)
    random.shuffle(indexes)
    indexes = indexes[0:num_pixels]
    rows, cols = index2row_col(indexes, img.shape[1])
    if dark:
        img[rows, cols] = img.max() if len(set(img.flatten())) > 1 else 1  # img.max() if img.max() > 0 else 1
    else:
        img[rows, cols] = [np.random.rand() for _ in range(0, len(rows))]
    if 'indexes' in metadata:
        metadata['indexes'].append(indexes)
    else:
        metadata['indexes'] = [indexes]
    return img


def background_shader(img, metadata, grey=None):
    """
    Applies a grey layer to an entire matrix (overwriting any previous values)
    :param img: image to apply the background layer to
    :param metadata: dictionary to log configs of this transformation
    :param grey: level of grey shade as float. grey=0 means no shade and grey=1 is completely black. If None, it's
    randomly chosen from [0, 1]. If Tuple[Int], then tone is randomly chosen from [grey[0], grey[1]]
    :return: image with uniform grey shade
    """
    grey = np.random.rand() if not grey else grey
    grey = np.random.rand() * (grey[1] - grey[0]) + grey[0] if hasattr(grey, '__iter__') else grey
    img = np.array(img)
    img[:, :] = grey
    metadata['greys'] = [grey] if 'greys' not in metadata else metadata['greys'] + [grey]
    return img


def index2row_col(indexes, num_cols):
    """
    Converts vector indexed matrix entries to row, col coordinates
    :param indexes: Iterable with indexes
    :param num_cols: number of columns of the target matrix
    :return: rows, cols, both lists with the respective dimension coordinates
    """
    cols = [i % num_cols for i in indexes]
    return [(i - c) // num_cols for i, c in zip(indexes, cols)], cols