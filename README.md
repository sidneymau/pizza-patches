# pizza-patches
Create patches for pizza slices and generate patch files

Examples
--------
```bash

# combine the individual info files into a file that has
# a ra, dec and a unique pizza_id
pizza-patches-combine-info \
    --info-files /path/to/2022_10_03_extract_slice_info/pz_data/*fits \
    --output 2022_10_03_extract_slice_info_combined.fits.gz

# assign patches.  You can also seend --npatch and --seed, which
# default to 150 and 998877 respectively
pizza-patches-assign \
    --info 2022_10_03_extract_slice_info_combined.fits.gz \
    --output 2022_10_03_extract_slice_info_patches.fits.gz

# make a plot of the patches
pizza-patches-plot \
    --patches 2022_10_03_extract_slice_info_patches.fits.gz \
    --output 2022_10_03_extract_slice_info_patches.png
```

Find the `pizza_id` for a set of objects from the metadetect
output files and get the patch number
```python
import os
import fitsio
from pizza_patches.util import get_pizza_ids


def match_ids(arr1, arr2, sort1=None):
    if sortind1 is None:
        sort1 = arr1.argsort()
    sub1 = np.searchsorted(arr1, arr2, sorter=sort1)
    sub2, = np.where(arr1[sort1[sub1]] == arr2)
    sub1 = sort1[sub1[sub2]]

    return sub1, sub2


patches = fitsio.read('2022_10_03_extract_slice_info_patches.fits.gz')
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
![Patches](data/patches150.png?raw=true "150 patches")
