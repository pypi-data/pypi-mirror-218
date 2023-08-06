#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="alphacore",
    version="0.0.8",
    description="Core statistical functions for alpha",
    author="Matthew Reid",
    author_email="alpha.reliability@gmail.com",
    license="LGPLv3",
    url="https://pypi.org/project/alphacore/",
    long_description="Core statistical functions for alpha",
    long_description_content_type="text/x-rst",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    install_requires=[
        "scipy>=1.10.1",
        "numpy>=1.24.2",
        "autograd>=1.5",
        "autograd-gamma>=0.5.0"
    ],
    python_requires=">=3.8",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*"]
    ),
)
