import random
import numpy as np


def vectorize(img):
    return img.flatten()


def cut(img_vector, first, last):
    return img_vector[first:-last]


def encode(l, key, metadata=None):
    random.seed(key)
    order = list(range(0, len(l)))
    random.shuffle(order)
    if metadata:
        metadata['col_shuffle'] = order
    return l[order]


def decode(l, key):
    """
    Decodes an encoded vector
    :param l: vector
    :param key: an iterable with the encoded order of the columns. If not an iterable, key is interpreted as the seed
    to generate this iterable
    :return:
    """
    if hasattr(key, '__iter__'):
        order = key
    else:
        random.seed(key)
        order = list(range(0, len(l)))
        random.shuffle(order)
    reshuffle = [order.index(i) for i in range(0, len(order))]
    return l[reshuffle]


def reconstruct(img, meta):
    """
    Reconstruct an image that went over several transformations
    :param img: transformed image
    :param meta: a list of transformations, in the order they were applied. Each transformation is a dictionary with
    keys 'transformation' and optionally 'config'
    :return: reconstructed image
    """
    for t in meta[::-1]:
        if t['transformation'] == 'shuffle':
            img = decode(img, key=t['config']['key'])
        elif t['transformation'] == 'cut':
            if len(img.shape) == 2:  # i.e. matrix
                img = np.concatenate((np.array([[0] * img.shape[1]] * t['config']['first']), img,
                                      np.array([[0] * img.shape[1]] * t['config']['last'])))
            elif len(img.shape) == 1:
                img = np.concatenate((np.array([0] * t['config']['first']), img, np.array([0] * t['config']['last'])))
            else:
                raise Exception('invalid image dimensions, can only be 1 or 2, got {}'.format(img.shape))
        elif t['transformation'] == 'vectorize':
            img = np.reshape(img, newshape=(t['config']['img_h'], t['config']['img_w']))
        else:
            raise Exception('invalid transformation: {}'.format(t['transformation']))
    return img

