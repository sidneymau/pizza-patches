import numpy as np

from ..patches import get_labels, NPATCH
from ..util import make_output, get_pizza_ids


def get_positions(seed):
    import esutil as eu

    rng = np.random.RandomState(seed=seed)

    ra, dec = eu.coords.randsphere(
        num=10000,
        ra_range=[10, 100],
        dec_range=[-60, 0],
        rng=rng,
    )
    return ra, dec


def test_labels():

    ra, dec = get_positions(seed=100)
    labels = get_labels(ra=ra, dec=dec)
    assert labels.size == ra.size
    assert np.unique(labels).size == NPATCH


def test_make_output():
    ra, dec = get_positions(seed=100)
    labels = get_labels(ra=ra, dec=dec)

    tilenames = ['DES0000-0333'] * ra.size
    slice_ids = np.arange(ra.size)

    output = make_output(
        tilenames=tilenames,
        slice_ids=slice_ids,
        labels=labels,
    )

    assert np.all(output['pizza_id'] == get_pizza_ids(tilenames, slice_ids))
    assert np.all(output['patch_num'] == get_labels(ra=ra, dec=dec))
