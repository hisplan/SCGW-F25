# Single Cell Genomics Workshop F2025

## Setup

### Prerequisites

For a smooth installation, ensure that your machine is running Miniconda version `25.5.1` or later.

### Mac

The following setup instructions were validated on a Mac with an Apple M2 chip, using Miniconda version `25.5.1`.

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab
conda activate scgw_f25

conda install -c conda-forge scanpy leidenalg python-igraph jaxlib jax conda-forge::scvi-tools bioconda::gseapy conda-forge::hnswlib conda-forge::python-annoy
pip install scrublet scimilarity Cython
```

### Windows

The following setup instructions were validated on a Windows 11, using Miniconda version `25.7.0`.

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab
conda activate scgw_f25

conda install -c conda-forge scanpy leidenalg python-igraph jaxlib jax conda-forge::hnswlib conda-forge::python-annoy
pip install scrublet gseapy scvi-tools scimilarity Cython
```

### Verify Installation

Please run the following command and ensure that each item is successfully verified and marked as complete ✅.

```bash
python check_env.py
```
