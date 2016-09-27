#!/usr/bin/python3

import platform
try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

if platform.system() == "Linux":
    bin_dir = "bins/linux"
elif platform.system() == "Darwin":
    bin_dir = "bins/osx"

structure_bin = bin_dir + "/structure"
faststructure_bin = bin_dir + "/fastStructure"

setup(
    name="structure_threader",
    version="0.1.5",
    packages=["structure_threader",
              "structure_threader.evanno",
              "structure_threader.plotter",
              "structure_threader.sanity_checks"],
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    description=("A program to parallelize runs of 'Structure' and "
                 "'fastStructure'."),
    url="https://github.com/StuntsPT/Structure_threader",
    author="Francisco Pina-Martins",
    author_email="f.pinamartins@gmail.com",
    license="GPL3",
    classifiers=["Intended Audience :: Science/Research",
                 "License :: OSI Approved :: GNU General Public License v3 ("
                 "GPLv3)",
                 "Natural Language :: English",
                 "Operating System:: POSIX:: Linux",
                 "Topic :: Scientific/Engineering :: Bio-Informatics"],
    data_files=[('bin', [faststructure_bin, structure_bin])],
    entry_points={
        "console_scripts": [
            "structure_threader = structure_threader.structure_threader:main",
        ]
    },
)