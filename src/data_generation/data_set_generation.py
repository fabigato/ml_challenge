from src.data_generation import paint_figures
from src.data_generation import filters
from src.data_generation import transformations
import numpy as np
import yaml
import random
from copy import deepcopy

class2generator = {
    'ellipse': paint_figures.get_ellipsis,
    'dipole': paint_figures.get_dipole,
    'snow': paint_figures.get_snow
}


def get_config(config_filename):
    """
    Reads the config file to generate a dataset
    :param config_filename: name of the yaml config file
    :return: config, a dictionary with mandatory keys 'img_h', 'img_w' and 'shapes'
    """
    with open(config_filename, "r") as config_fh:
        config = yaml.load(config_fh)
    for c in config['shapes']:
        c['config']['img_h'] = config['img_h']
        c['config']['img_w'] = config['img_w']
    for t in config['transformations']:
        if t['transformation'] == 'vectorize':
            t['config'] = {'img_w': config['img_w'], 'img_h': config['img_h']}  # required when reconstructing
    return config


def produce_dataset(config_filename):
    """
    Produces a dataset given specifications in a config yaml file.
    :param config_filename: name of the yaml config file
    :return dataset as a (data_points, labels, metadata) tuple. Data points are randomly shuffled.
    """
    config = get_config(config_filename)
    meta = deepcopy(config)
    data_points, labels = [], []
    for ci, c in enumerate(config['shapes']):
        num_samples = c['config']['samples'] if 'samples' in c['config'] else 1
        c['config']['samples'] = num_samples
        # shape_meta_data = c
        # shape_meta_data['filters'] = []
        canvas = [np.zeros((config['img_h'], config['img_w'])) for _ in range(0, num_samples)]  # empty canvas
        meta['shapes'][ci]['filters'] = []#deepcopy(config['filters'])  # meta data over each filter applied to each class
        for fi, _filter in enumerate(config['filters']):  # add here if you want to consider shape specific filters
            if _filter['filter'] == 'background_shader':  # generate grayed canvas van tevoren
                # meta['shapes'][ci]['filters'].append(deepcopy(_filter))
                filter_meta = meta['filters'][fi]
                canvas = [filters.background_shader(m, metadata=filter_meta, **_filter['config'])
                          if 'config' in _filter else filters.background_shader(canvas, metadata=filter_meta)
                          for m in canvas]
            if _filter['filter'] == 'background_noise':
                # meta['shapes'][ci]['filters'].append(deepcopy(_filter))
                filter_meta = meta['filters'][fi]
                canvas = [filters.pixel_noise(m, metadata=filter_meta, **_filter['config'])
                          if 'config' in _filter else filters.pixel_noise(canvas, metadata=filter_meta)
                          for m in canvas]
            if _filter['filter'] == 'background_blurr':
                # meta['shapes'][ci]['filters'].append(deepcopy(_filter))
                filter_meta = meta['filters'][fi]
                canvas = [filters.blurr(m, metadata=filter_meta, **_filter['config'])
                          if 'config' in _filter else filters.blurr(canvas, metadata=filter_meta) for m in canvas]
            #shape_meta_data['filters'] += filter_metadata
        #meta_data['shapes'] += shape_meta_data
        c['config']['samples'] = canvas
        meta['shapes'][ci]['config']['samples'] = len(canvas)
        # del c['config']['samples']
        data = class2generator[c['shape']](**c['config'])
        # c['config']['samples'] = len(canvas)
        label = [c['shape']] * len(data)
        data_points += data
        labels += label
    consistent_seed = np.random.rand()
    # meta_data['filters'] = []
    for fi, _filter in enumerate(config['filters']):
        filter_meta = meta['filters'][fi]
        # filter_metadata = _filter
        if _filter['filter'] == 'blurr':
            data_points = [filters.blurr(m, metadata=filter_meta, **_filter['config']) if 'config' in _filter
                           else filters.blurr(m, metadata=filter_meta) for m in data_points]
        if _filter['filter'] == 'pixel_noise':
            data_points = [filters.pixel_noise(m, metadata=filter_meta, **_filter['config']) for m in data_points]
        if _filter['filter'] == 'consistent_noise':
            if 'seed' not in _filter['config']:
                _filter['config']['seed'] = consistent_seed
            data_points = [filters.pixel_noise(m, metadata=filter_meta, **_filter['config']) for m in data_points]
            filter_meta['indexes'] = filter_meta['indexes'][0]  # cheap fix to remove identical pixel lists
        # meta_data['filters'] += filter_metadata
    # meta_data['transformations'] =
    for ti, t in enumerate(config['transformations']):
        meta_trans = meta['transformations'][ti]
        if t['transformation'] == "vectorize":
            data_points = [transformations.vectorize(m) for m in data_points]
        if t['transformation'] == "cut":
            data_points = [transformations.cut(m, **t['config']) for m in data_points]
        if t['transformation'] == "shuffle":
            data_points = [transformations.encode(m, metadata=meta['transformations'][ti], **t['config'])
                           for m in data_points]
    order = [i for i in range(0, len(data_points))]
    random.shuffle(order)
    meta['shuffle'] = order
    shuffle_filters(meta, order)
    return [data_points[d] for d in order], [labels[l] for l in order], meta


def shuffle_filters(meta, order):
    for f in meta['filters']:
        if f['filter'] == 'background_shader':
            f['greys'] = [f['greys'][g] for g in order]
        if f['filter'] == 'background_noise':
            f['indexes'] = [f['indexes'][p] for p in order]
        if f['filter'] == 'pixel_noise':
            f['indexes'] = [f['indexes'][p] for p in order]

