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


def get_patch_basename(patch_num):
    return f'patch-{patch_num:04d}.fits'


def get_patch_file(dir, patch_num):
    import os
    return os.path.join(dir, get_patch_basename(patch_num))


def make_output(pizza_ids, ra, dec, labels):
    import numpy as np

    # 12 for tilename, one for - and four for slice_id
    id_dtype = get_pizza_id_dtype()
    output = np.zeros(
        len(pizza_ids),
        dtype=[
            ('pizza_id', id_dtype),
            ('ra', 'f8'), ('dec', 'f8'),
            ('patch_num', 'i2'),
        ],
    )
    output['pizza_id'] = pizza_ids
    output['ra'] = ra
    output['dec'] = dec
    output['patch_num'] = labels
    return output


def load_flist(fname):
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
