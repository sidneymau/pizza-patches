import numpy as np

from ..patches import get_labels
from ..util import make_output, get_pizza_ids

NPATCH = 150


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
    labels = get_labels(ra=ra, dec=dec, npatch=NPATCH, seed=12345)
    assert labels.size == ra.size
    assert np.unique(labels).size == NPATCH


def test_make_output():
    ra, dec = get_positions(seed=300)

    seed = 8
    labels = get_labels(ra=ra, dec=dec, npatch=NPATCH, seed=seed)

    tilenames = ['DES0000-0333'] * ra.size
    slice_ids = np.arange(ra.size)
    pizza_ids = get_pizza_ids(tilenames=tilenames, slice_ids=slice_ids)

    output = make_output(
        pizza_ids=pizza_ids,
        ra=ra, dec=dec,
        labels=labels,
    )

    assert np.all(output['pizza_id'] == get_pizza_ids(tilenames, slice_ids))
    assert np.all(output['ra'] == ra)
    assert np.all(output['dec'] == dec)

    # also tests repeatability
    assert np.all(
        output['patch_num'] == get_labels(
            ra=ra, dec=dec, npatch=NPATCH, seed=seed,
        )
    )
