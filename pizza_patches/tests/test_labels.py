from ..patches import get_labels, NPATCH


def test_labels():
    import numpy as np
    import esutil as eu
    seed = 100

    rng = np.random.RandomState(seed=seed)

    ra, dec = eu.coords.randsphere(
        num=10000,
        ra_range=[10, 100],
        dec_range=[-60, 0],
        rng=rng,
    )

    labels = get_labels(ra=ra, dec=dec)
    assert labels.size == ra.size
    assert np.unique(labels).size == NPATCH
