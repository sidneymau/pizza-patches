def get_centers(ra, dec, mask, npatch, seed, alt=True):
    """
    get kmeans centers using the treecorr code

    Only ra/dec ok for mask are used to define patches

    We throw out a patch in the turret to try to make them be a big
    larger, closer to size of the main area patches

    Parameters
    -----------
    ra: array
        Array of ra to use for kmeans
    dec: array
        Array of dec to use for kmeans
    mask: HealSparseMap
        The healsparse map
    npatch: int
        Number of kmeans patches
    seed: int
        Seed for random number generator, used to make
        patch center guesses
    alt: bool, optional
        If set to True, use alternate algorithm

    Returns
    -------
    centers: (npatch, 3)
    """
    import treecorr
    import numpy as np

    rng = np.random.RandomState(seed)

    print('getting mask values')
    vals = mask.get_values_pos(ra, dec)
    w, = np.where(vals == 1)

    print('getting centers')
    subcat = treecorr.Catalog(
        ra=ra[w],
        dec=dec[w],
        ra_units='deg',
        dec_units='deg',
    )
    subfield = subcat.getNField()

    centers = subfield.kmeans_initialize_centers(
        npatch + 1, init='tree', rng=rng,
    )
    subfield.kmeans_refine_centers(centers, alt=alt)

    # Remove the upper right center.
    # z-y is roughly up/right direction.
    upper_right = np.argmax(centers[:, 2] - centers[:, 1])
    centers = centers[np.arange(npatch + 1) != upper_right]

    # redo refinement with this adjustment, will need extra
    # iterations
    subfield.kmeans_refine_centers(centers, alt=alt, max_iter=2000)

    return centers


def get_labels(ra, dec, centers):
    """
    get kmeans labels using the treecorr code

    Only ra/dec ok for mask are used to define patches, but all ra dec
    are given labels

    We throw out a patch in the turrent to try to make them be a big
    larger, closer to size of the main area patches

    Parameters
    -----------
    ra: array
        Array of ra to use for kmeans
    dec: array
        Array of dec to use for kmeans
    centers: array
        (npatch, 3) x y z

    Returns
    -------
    labelnums: array of patch ids as integers
    """
    import treecorr
    import numpy as np
    from tqdm import trange

    print('getting labels')

    chunksize = 100000
    nchunks = ra.size // chunksize
    if ra.size % chunksize != 0:
        nchunks += 1

    tlist = []
    for i in trange(nchunks):
        start = i * chunksize
        end = (i + 1) * chunksize

        tra = ra[start:end]
        tdec = dec[start:end]

        tcat = treecorr.Catalog(
            ra=tra,
            dec=tdec,
            ra_units='deg',
            dec_units='deg',
        )
        tfield = tcat.getNField()

        tlabelnums = tfield.kmeans_assign_patches(centers)
        assert tlabelnums.size == tra.size

        tlist.append(tlabelnums)

        del tfield
        del tcat

    labelnums = np.hstack(tlist)
    return labelnums


def make_patches_output(pizza_ids, ra, dec, labels):
    """
    Make the patches output struct

    Parameters
    ----------
    pizza_ids: array of strings
        The pizza cutter ids created from tilename and
        slice id.  See util.get_pizza_id and get_pizza_ids
    ra: array
        position array
    dec: array
        position array
    labels: array of int
        See get_labels

    Returns
    --------
    array with inputs packed in
    """
    import numpy as np

    # 17 is 12 for tilename, one for - and four for slice_id
    output = np.zeros(
        len(pizza_ids),
        dtype=[
            ('pizza_id', 'U17'),
            ('ra', 'f8'), ('dec', 'f8'),
            ('patch_num', 'i2'),
        ],
    )
    output['pizza_id'] = pizza_ids
    output['ra'] = ra
    output['dec'] = dec
    output['patch_num'] = labels
    return output
