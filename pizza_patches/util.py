def get_pizza_id(tilename, slice_id):
    return '%s-%04d' % (tilename, slice_id)


def get_pizza_ids(tilenames, slice_ids):
    import numpy as np
    return np.array([
        get_pizza_id(tilename, slice_id)
        for tilename, slice_id in zip(tilenames, slice_ids)
    ])


def get_pizza_id_dtype():
    IDSIZE = 17
    return 'U%d' % IDSIZE


def make_output(pizza_ids, labels):
    import numpy as np

    # 12 for tilename, one for - and four for slice_id
    id_dtype = get_pizza_id_dtype()
    output = np.zeros(
        len(pizza_ids),
        dtype=[('pizza_id', id_dtype), ('patch_num', 'i2')],
    )
    output['pizza_id'] = pizza_ids
    output['patch_num'] = labels
    return output
