IDSIZE = 17
ID_DTYPE = 'U%d' % IDSIZE


def get_pizza_id(tilename, slice_id):
    return '%s-%04d' % (tilename, slice_id)


def get_pizza_ids(tilenames, slice_ids):
    import numpy as np
    return np.array([
        get_pizza_id(tilename, slice_id)
        for tilename, slice_id in zip(tilenames, slice_ids)
    ])


def make_output(tilenames, slice_ids, labels):
    import numpy as np

    # 12 for tilename, one for - and four for slice_id
    output = np.zeros(
        len(tilenames),
        dtype=[('pizza_id', ID_DTYPE), ('patch_num', 'i2')],
    )
    output['pizza_id'] = get_pizza_ids(tilenames, slice_ids)
    output['patch_num'] = labels
    return output
