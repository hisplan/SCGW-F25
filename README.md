# Single Cell Genomics Workshop F2025

The following setup instructions were validated on a Mac with an Apple M2 chip, using Miniconda version 25.5.1.

## Setup

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab
conda activate scgw_f25

conda install -c conda-forge scanpy leidenalg python-igraph scrublet jaxlib jax conda-forge::scvi-tools bioconda::gseapy conda-forge::hnswlib

pip install scimilarity Cython
```

## Verify Installation

```python
import scanpy as sc
import pandas as pd
import numpy as np
import scipy
import scvi
import scimilarity
import gseapy
import scrublet
import anndata
```
