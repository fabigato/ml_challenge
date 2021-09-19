import numpy as np
from math import sin, cos


def paint_ellipse(m, a, b, r, alpha, origin=(0, 0), dark=False):
    """
    Receives a zero filled matrix and fills it with numbers in the pattern of an ellipse
    :param m: zero filled matrix to paint
    :param a: axis 1 of ellipse
    :param b: axis 2 of ellipse
    :param r: sum of distances each point in the ellipse must satisfy from the two foci
    :param alpha: rotation angle
    :param origin: origin offset, as Iterable[Int] of len 2
    :param dark: if True, all points within the matrix are 1 (resulting in a completely black ellipse). Else, each point
    is colored proportionally to their summed distance from the foci, resulting in a greyscaled gradient
    :return: None. The original matrix m is updated
    """
    # m = np.array(m)
    x_max, y_max = m.shape[0] // 2, m.shape[1] // 2
    tone = 1 # m.max() if len(set(m.flatten())) > 1 else 1  # check not all values are same (background grey filter does it)
    for row in range(0, m.shape[0]):
        for col in range(0, m.shape[1]):
            x, y = (x_max - col + origin[0]), (row - y_max + origin[1])
            if ((x*cos(alpha) - y*sin(alpha))/a)**2 + ((x*sin(alpha) + y*cos(alpha))/b)**2 <= r**2:
                m[row][col] = tone if dark else (((x * cos(alpha) - y * sin(alpha))/a) ** 2 +
                                                 ((x * sin(alpha) + y * cos(alpha))/b) ** 2) / r**2  # * tone


def get_ellipsis(samples=1, dark=False, img_h=100, img_w=100, o_margin=0.5, a=None, b=None, r=None, alpha=None,
                 origin=(0, 0)):
    """
    Produces samples from the ellipse class, as float matrices that can be displayed as an image
    :param samples: an iterable of matrices where the ellipsis are to be painted. Alternatively, it could be a number
    indicating the amount of samples to produce
    :param dark: if True, all points within the matrix are 1 (resulting in a completely black ellipse). Else, each point
    is colored proportionally to their summed distance from the foci, resulting in a greyscaled gradient
    :param img_h: matrix height (num rows)
    :param img_w: matrix width (num cols)
    :param o_margin: how many cols/rows must the origin be kept apart from any boundary, as a percentage of the sizes.
    Ignored if origin is explicitly set
    :param a: size of axis 1. If None, it will be randomly chosen to be within a 2 and a 0.5 percent of the image size
    :param b: size of axis 2. If None, it will be randomly chosen just like a
    :param r: total distance any point on the rim must satisfy from the two foci of an ellipse. If None it will be
    randomly chosen to be inversely proportional to the image size
    :param alpha: rotation angle in radians. If None it will be randomly chosen between 0 and and 3/2 Pi
    :param origin: origin offset as an Iterable[int] of size 2. If provided, o_margin has no effect
    :return: Iterable with samples, each a matrix of floats
    """
    result = [np.zeros((img_h, img_w)) for _ in range(0, samples)] if isinstance(samples, int) else samples
    for mat in result:
        _a = a if a else int((img_h * img_w * 0.02 - img_h * img_w * 0.005) * np.random.rand() + img_h * img_w * 0.005)
        _b = b if b else int((img_w * img_h * 0.02 - img_w * img_h * 0.005) * np.random.rand() + img_w * img_h * 0.005)
        _r = r if r else (np.random.rand() * 20 + 40)/(img_h + img_w)
        _alpha = np.random.rand() * 4.71 if not alpha else alpha
        _origin = origin if origin else [int((1 - o_margin) * 2 * img_w * np.random.rand() + (o_margin-1) * img_w),
                                         int((1 - o_margin) * 2 * img_h * np.random.rand() + (o_margin - 1) * img_h)]
        paint_ellipse(m=mat, a=_a, b=_b, r=_r, alpha=_alpha, origin=_origin, dark=dark)
    return result


def get_dipole(samples=1, img_h=100, img_w=100, **kwargs):
    """
    Produces samples from the dipole class, as float matrices that can be displayed as an image. Each dipole is created
    by calling get_ellipsis twice on the same matrix, therefore subsequent parameters are passed to get_ellipsis
    :param samples: an iterable of matrices where the ellipsis are to be painted. Alternatively, it could be a number
    indicating the amount of samples to produce
    :param img_h: matrix height (num rows)
    :param img_w: matrix width (num cols)
    :return: Iterable with samples, each a matrix of floats
    """
    result = [np.zeros((img_h, img_w)) for _ in range(0, samples)] if isinstance(samples, int) else samples
    get_ellipsis(samples=result, img_h=img_h, img_w=img_w, **kwargs)
    get_ellipsis(samples=result, img_h=img_h, img_w=img_w, **kwargs)
    return result


def get_snow(samples=1, num_dots=10, dark=True, img_h=100, img_w=100, **kwargs):
    """
    Produces samples from the snow class, as float matrices that can be displayed as an image. Each snow sample is
    createdby calling get_ellipsis num_dots times on the same matrix, therefore subsequent parameters are passed to
    get_ellipsis
    :param samples: an iterable of matrices where the ellipsis are to be painted. Alternatively, it could be a number
    indicating the amount of samples to produce
    :param num_dots: number of dots in each sample. If None, a random number will be selected between 10 and 20
    :param dark: if True, all points within the matrix are 1 (resulting in a completely black ellipse). Else, each point
    is colored proportionally to their summed distance from the foci, resulting in a greyscaled gradient
    :param img_h: matrix height (num rows)
    :param img_w: matrix width (num cols)
    :return: Iterable with samples, each a matrix of floats
    """
    result = [np.zeros((img_h, img_w)) for _ in range(0, samples)] if isinstance(samples, int) else samples
    num_dots = 10 * np.random.rand() + 10 if not num_dots else num_dots
    for _ in range(0, num_dots):
        r = (np.random.rand() * 5 + 5) / (img_h + img_w)
        get_ellipsis(samples=result, dark=dark, img_h=img_h, img_w=img_w, r=r, **kwargs)
    return result
