import os
from glob import glob
from setuptools import setup, find_packages

__version__ = None

version_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "pizza_patches",
    "version.py"
)
with open(version_file, 'r') as fp:
    exec(fp.read())

scripts = glob('bin/*')
scripts = [s for s in scripts if '~' not in s]

setup(
    name="pizza-patches",
    author="Erin Sheldon",
    url="https://github.com/esheldon/pizza-patches",
    description=(
        "Make kmeans patches for pizza cutter slices and create patch files"
    ),
    packages=find_packages(),
    scripts=scripts,
    version=__version__,
)
