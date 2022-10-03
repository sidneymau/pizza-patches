SEED = 998877
NPATCH = 200


def get_labels(ra, dec):
    import treecorr
    import numpy as np
    cat = treecorr.Catalog(
        ra=ra,
        dec=dec,
        ra_units='deg',
        dec_units='deg',
    )
    field = cat.getNField()
    labelnums, centers = field.run_kmeans(
        NPATCH,
        rng=np.random.RandomState(SEED),
    )
    return labelnums
