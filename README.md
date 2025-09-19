# Single Cell Genomics Workshop F2025

"평균의 종말, 세포 하나의 이야기를 듣다"

- 장소: 한동대학교 에벤에셀관 헤브론홀
- 일시: 2025년 9월 6일 ~ 10월 4일 매주 토요일 09:00 AM ~ 11:59 AM (총 5회)

## Setup

### Prerequisites

If you have Annaconda or Python from python.org installed, please uninstall them and use Miniconda instead to avoid potential conflicts.

For a smooth installation, ensure that your machine is running Miniconda version `25.5.1` or later.

### Mac

The following setup instructions were validated on a Mac with an Apple M2 chip, using Miniconda version `25.5.1`.

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab -y
conda activate scgw_f25

conda install -c conda-forge scanpy=1.11.4 leidenalg=0.10.2 python-igraph=0.11.9 jaxlib=0.5.3 jax=0.5.3 conda-forge::scvi-tools=1.3.3 bioconda::gseapy=1.1.9 conda-forge::hnswlib=0.8.0 conda-forge::python-annoy=1.17.3
pip install scikit-misc==0.5.1 scrublet==0.2.3 scimilarity==0.4.1 Cython==3.1.3
```

### Windows

The following setup instructions were validated on a Windows 11, using Miniconda version `25.7.0`.

```bash
conda create -n scgw_f25 python=3.12 pip jupyterlab -y
conda activate scgw_f25

conda install -c conda-forge scanpy leidenalg python-igraph jaxlib jax conda-forge::hnswlib conda-forge::python-annoy
pip install scikit-misc==0.5.1 scrublet gseapy scvi-tools scimilarity Cython
```

### Verify Installation

Please run the following command and ensure that each item is successfully verified and marked as complete ✅.

```bash
python check_env.py
```

## Sample Dataset

We will be using a public dataset from [10x Genomics](https://www.10xgenomics.com/datasets/10-k-pbm-cs-from-a-healthy-donor-v-3-chemistry-3-standard-3-0-0) that contains about 11 thousand peripheral blood mononuclear cells (PBMCs) from a healthy donor. The dataset can be downloaded from [here](https://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_10k_v3/pbmc_10k_v3_filtered_feature_bc_matrix.h5). You can also use `wget` or `curl` to download the file from the command line.

```bash
wget https://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_10k_v3/pbmc_10k_v3_filtered_feature_bc_matrix.h5
```

![Download](./img/pbmc_10k_v3_filtered_feature_bc_matrix.png)