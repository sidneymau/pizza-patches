def get_pizza_id(tilename, slice_id):
    """
    defines a unique pizza slice id tilename-slice_id
    """
    return '%s-%04d' % (tilename, slice_id)


def get_pizza_ids(tilenames, slice_ids):
    """
    get pizza ids for a list of objects
    """
    import numpy as np
    return np.array([
        get_pizza_id(tilename, slice_id)
        for tilename, slice_id in zip(tilenames, slice_ids)
    ])


def get_mdet_patch_basename(patch_num):
    """
    get the mdet outputs file for a given patch
    """
    return f'patch-{patch_num:04d}.fits'


def get_mdet_patch_file(dir, patch_num):
    """
    get the full path mdet outputs file for a given patch
    """
    import os
    return os.path.join(dir, get_mdet_patch_basename(patch_num))


def load_flist(fname):
    """
    load a list of files from a file, one per line.  Drop
    empty lines.
    """
    print('reading flist:', fname)
    with open(fname) as fobj:
        flist = []
        for line in fobj:
            line = line.strip()
            if line != '':
                flist.append(line)
    return flist


def load_yaml(fname):
    import yaml
    print('reading:', fname)
    with open(fname) as fobj:
        data = yaml.safe_load(fobj)
    return data
