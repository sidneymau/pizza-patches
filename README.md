# pizza-patches
Create patches for pizza slices and generate patch files

## Steps to Make the HDF5 Files

```bash
# combine the individual info files into a file that has
# a ra, dec and a unique pizza_id
pizza-patches-combine-info \
    --info-files /gpfs02/astro/workarea/beckermr/des-y6-analysis/2022_10_03_extract_slice_info/pz_data/*fits \
    --output slice-info.fits.gz

# assign patches.  You can also seend --npatch and --seed, which
# default to 200 and 9999 respectively
pizza-patches-assign \
    --info slice-info.fits.gz \
    --mask y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v3.fits \
    --npatch 200 \
    --seed 8888 \
    --output patches-altrem-npatch200-seed8888.fits.gz

# make a plot of the patches (optionally with mask)
pizza-patches-plot \
    --seed 3 \
    --mask y6-combined-hleda-gaiafull-des-stars-hsmap16384-nomdet-v3.fits \
    --patches patches-altrem-npatch200-seed8888.fits.gz \
    --output patches-altrem-npatch200-seed8888-pseed3.png

ls /gpfs02/astro/workarea/beckermr/des-y6-analysis/2023_02_25_run_mdet_nocoadd/mdet_data/*.fits > mdet_flist.txt
pizza-patches-make-uids --flist=mdet_flist.txt --output=mdet_uids.yaml --n-jobs=-1

ls /gpfs02/astro/workarea/beckermr/des-y6-analysis/2023_02_25_run_mdet_nocoadd/mdet_data/*.fits > mdet_flist.txt
pizza-patches-make-cut-files \
    --flist=`pwd`/mdet_flist.txt \
    --uid-info=`pwd`/mdet_uids.yaml \
    --patches="/astro/u/esheldon/y6patches/patches-altrem-npatch200-seed8888.fits.gz" \
    --outdir=`pwd`/mdet_data_v6cuts \
    --keep-coarse-cuts

chmod go-rwx mdet_data_v6cuts/*.fits
chmod u-w mdet_data_v6cuts/*.fits

pizza-patches-make-hdf5-cats \
    --output-file-base="metadetect_cutsv6" \
    --input-file-dir=`pwd`/mdet_data_v6cuts

chmod go-rwx metadetect_cutsv6_all.h5
chmod go-rwx metadetect_cutsv6_patch*.h5
chmod u-w metadetect_cutsv6_all.h5
chmod u-w metadetect_cutsv6_patch*.h5
```

## Using library functions

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


patches = fitsio.read('patches-altrem-npatch200-seed8888.fits.gz')
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
