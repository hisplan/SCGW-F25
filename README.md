# Single Cell Genomics Workshop F2025

## Setup

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab
conda activate scgw_f25

conda install -c conda-forge scanpy leidenalg python-igraph scrublet jaxlib jax conda-forge::scvi-tools bioconda::gseapy conda-forge::hnswlib

pip install scimilarity Cython
```
