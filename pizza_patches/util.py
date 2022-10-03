def get_patch_id(tilename, slice_id):
    return '%s-%04d' % (tilename, slice_id)


def get_patch_ids(tilenames, slice_ids):
    import numpy as np
    return np.array([
        get_patch_id(tilename, slice_id)
        for tilename, slice_id in zip(tilenames, slice_ids)
    ])
