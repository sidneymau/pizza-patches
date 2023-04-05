# pizza-patches
Create patches for pizza slices and generate patch files

Examples
--------
```bash

# combine the individual info files into a file that has
# a ra, dec and a unique pizza_id
pizza-patches-combine-info \
    --info-files /path/to/2022_10_03_extract_slice_info/pz_data/*fits \
    --output slice-info.fits.gz

# assign patches.  You can also seend --npatch and --seed, which
# default to 200 and 9999 respectively
pizza-patches-assign \
    --info slice-info.fits.gz \
    --mask y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v3.fits \
    --npatch 200 \  # same as the default number of patches
    --seed 9999 \ # same as the default seed
    --output patches-altrem-npatch200-seed9999.fits.gz

# make a plot of the patches (optionally with mask)
pizza-patches-plot \
    --seed 3 \
    --mask y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v3.fits \
    --patches patches-altrem-npatch200-seed9999.fits.gz \
    --output patches-altrem-npatch200-seed9999-pseed3.png

# partition metadetect outputs into files by patch
find /path/to/metadetect/ -name "*.fits" | sort > flist.txt

# make the unique ids
pizza-patches-make-uids --flist flist.txt --output uids.yaml

# split into chunks for parallel processing
split-file --prefix "flist-split" -n 8 -f flist.txt

# process each separately.  Processing split 3
pizza-patches-partition \
        --flist flist-split3.txt \
        --patches patches-altrem-npatch200-seed9999.fits.gz \
        --outdir patches3/ \
        --uid-info uids.yaml

# More than one of the above splits can add objects
# to the same patch.  We need to merge the patches
# Here is an example for patch 135
ls patches[0-9]/*fits > unmerged-patch-files.txt
patchname=patch-0135
tmpfile=/tmp/patch-${patchname}.txt
grep ${patchname} unmerged-patch-files.txt > ${tmpfile}

pizza-patches-merge-patch --flist ${tmpfile} --outdir patches
```


Using library functions.
------------------------
Find the `pizza_id` for a set of objects from the metadetect
output files and get the patch number
```python
import os
import fitsio
from pizza_patches.util import get_pizza_ids


def match_ids(arr1, arr2, sort1=None):
    if sort1 is None:
        sort1 = arr1.argsort()
    sub1 = np.searchsorted(arr1, arr2, sorter=sort1)
    sub2, = np.where(arr1[sort1[sub1]] == arr2)
    sub1 = sort1[sub1[sub2]]

    return sub1, sub2


patches = fitsio.read('patches-altrem-npatch200-seed9999.fits.gz')
mdet_fname = '/path/to/DES0008+0209_r5935p01_metadetect.fits'

data = fitsio.read(mdet_fname)
tilename = os.path.basename(mdet_fname)[:12]

pizza_ids = get_pizza_ids(
    tilenames=[tilenames] * data.size,
    slice_ids=data['id'],
)

mpatches, mobjects = match_ids(patches['pizza_ids'], pizza_ids)
patch_nums = patches['patch_num'][mpatches]
```
Example patches
----------------
![Patches](data/patches-altrem-npatch200-seed9999-Spectral-pseed3.png?raw=true "200 patches")
