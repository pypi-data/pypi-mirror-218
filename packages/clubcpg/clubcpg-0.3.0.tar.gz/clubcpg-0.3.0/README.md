# CluBCpG: Cluster-Based analysis of CpG methylation

[![Documentation Status](https://readthedocs.org/projects/clubcpg/badge/?version=latest)](https://clubcpg.readthedocs.io/en/latest/?badge=latest)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/waterlandlab/CluBCpG.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/waterlandlab/CluBCpG/context:python)
[![DOI](https://zenodo.org/badge/179135025.svg)](https://zenodo.org/badge/latestdoi/179135025)

## Whats new?
### v0.3.0
* A major overhaul and modernization of the ClubCpG dependencies.
* `setup.py` removed in favor of a `pyproject.toml`
* All project dependencies updated to modern versions
* Support of python 3.5, 3.6, 3.7, and 3.8 dropped
* Minimum version of python is now 3.9
* Added GitHub Actions workflows to automate testing of python 3.9 and 3.10
* Updated readthedocs build configuration ahead of deprecation of old method


## What is CluBCpG?
CluBCpG is a software package built to analyze whole genome bisulfite sequencing (WGBS) data. This toolkit will divide each chromosome into small user-defined intervals, extract all WGBS reads within those intervals, cluster them based on identity, and write a final report to the use containing all identified CpG methylation patterns.

## How do I use this?
Full documentation is available on [ReadTheDocs](https://clubcpg.readthedocs.io/en/latest/index.html)

### Requirements
* Python >= 3.9, <3.11
* Installation of Samtools on your PATH

### Install
* __(Optional, but HIGHLY recommended)__ Create a new python virtual environment and activate that virualenv
* Execute `pip install clubcpg` to install the package. Requirements will automatically be installed if not already present.

### Developer Install
* Ensure all dependencies in `ubuntu-preinsatll.sh` are installed on the system. (Or equivilant packages if using fedora based system)
* Install samtools, use `install-samtools.sh`
* Make sure you have a compatible version of python installed
* Install Poetry `pip3 install poetry`
* Run `poetry install` to install required packages and clubcpg
* To install optional packages for docs building. Run `poetry install --with docs`

## Help! This isnt working.
Open an [Issue](https://github.com/waterlandlab/CluBCpG/issues/new/choose)

## Can you make it do this?
Open a [Feature Request](https://github.com/waterlandlab/CluBCpG/issues/new/choose)
