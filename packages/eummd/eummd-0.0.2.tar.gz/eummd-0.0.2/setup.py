import os

import numpy as np

from os.path import join
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Define the extension
ext = Extension(
    'eummd.cppsrc.cppmethods',
    sources=[
        os.path.join('eummd', 'cppsrc', 'cppmethods.pyx'),
        os.path.join('eummd', 'cppsrc', 'eummd.cpp'),
        os.path.join('eummd', 'cppsrc', 'medianHeuristic.cpp'),
        os.path.join('eummd', 'cppsrc', 'meammd.cpp'),
        os.path.join('eummd', 'cppsrc', 'naive.cpp')
    ],
    include_dirs=[np.get_include()],
    language='c++',
    extra_compile_args=["-std=c++11"]
)

# Use cythonize on the extension object.
setup(
    name='eummd',
    version="0.0.2",
    python_requires=">=3.6",
    install_requires=["scipy>=1", "numpy>=1"],
    author="Dean Bodenham",
    author_email="deanbodenhampkgs@gmail.com",
    description="Computes maximum mean discrepancy two-sample test for univariate data using the Laplacian kernel. It is also possible to compute the p-value using permutations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/eummd",
    ext_modules=cythonize(ext, language_level="3"),
    packages=find_packages(),
    package_data={
        "eummd": ["cppsrc/*.pyx", "cppsrc/*.cpp", "cppsrc/*.h", "cppsrc/*.so", "cppsrc/*.pyd"]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)

