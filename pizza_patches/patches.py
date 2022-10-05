def get_labels(ra, dec, npatch, seed, alt=True):
    """
    get kmeans labels using the treecorr code

    We throw out a patch in the turrent to try to make them be a big
    larger, closer to size of the main area patches

    Parameters
    -----------
    ra: array
        Array of ra to use for kmeans
    dec: array
        Array of dec to use for kmeans
    npatch: int
        Number of kmeans patches
    seed: int
        Seed for random number generator, used to make
        patch center guesses
    alt: bool, optional
        If set to True, use alternate algorithm

    Returns
    -------
    labelnums: array of patch ids as integers
    """
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

    centers = field.kmeans_initialize_centers(
        npatch + 1, init='tree', rng=rng,
    )
    field.kmeans_refine_centers(centers, alt=alt)

    # Remove the upper right center.
    # z-y is roughly up/right direction.
    upper_right = np.argmax(centers[:, 2] - centers[:, 1])
    centers = centers[np.arange(npatch + 1) != upper_right]

    # redo refinement with this adjustment, will need extra
    # iterations
    field.kmeans_refine_centers(centers, alt=alt, max_iter=2000)
    labelnums = field.kmeans_assign_patches(centers)

    # here is the more standard call, for reference
    # labelnums, centers = field.run_kmeans(
    #     npatch,
    #     rng=rng,
    #     alt=True,
    # )
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
