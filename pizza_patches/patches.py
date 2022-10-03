def get_labels(ra, dec, npatch, seed):
    import treecorr
    import numpy as np

    rng = np.random.RandomState(seed)

    cat = treecorr.Catalog(
        ra=ra,
        dec=dec,
        ra_units='deg',
        dec_units='deg',
    )
    field = cat.getNField()
    labelnums, centers = field.run_kmeans(
        npatch,
        rng=rng,
    )
    return labelnums
