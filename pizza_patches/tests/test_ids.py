from ..util import get_patch_ids


def test_ids():
    import numpy as np

    seed = 952
    rng = np.random.RandomState(seed=seed)

    tilenames = [
        'DES0000-0333',
        'DES0000+0252',
        'DES0001-3457',
        'DES0001-0541',
        'DES0000-0207',
        'DES0000-3623',
        'DES0000-4831',
        'DES0000-3706',
        'DES0000-5914',
        'DES0000-5622',
    ]
    slice_ids = [
        rng.randint(0, 9000)
        for i in range(len(tilenames))
    ]

    ids = get_patch_ids(tilenames=tilenames, slice_ids=slice_ids)
    assert ids.size == len(tilenames)
    for i, id in enumerate(ids):
        assert len(id) == 17
        assert id == '%s-%04d' % (tilenames[i], slice_ids[i])
