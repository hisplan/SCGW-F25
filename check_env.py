"""
환경 헬스체크 원샷 스크립트 (Windows / scgw_F2025)
- 핵심 패키지 import
- 버전/디바이스 요약
- 간단 연산 스모크 테스트
- Scanpy 파이프라인 (HVG: cell_ranger)  ← skmisc 불필요
- scvi-tools 1 epoch 학습
- Scrublet (expected_doublet_rate는 생성자에 설정)
- hnswlib / annoy 인덱스 빌드/쿼리
- gseapy prerank (오프라인, dict gene set)
- JAX jit 테스트
"""

import os, sys, math, numpy as np, pandas as pd

np.random.seed(0)


def ok(msg):
    print("✅", msg)


def fail(msg, e):
    print("❌", msg, "->", repr(e))


# ---------- 1) IMPORT & VERSION ----------
mods = [
    "scanpy",
    "anndata",
    "pandas",
    "numpy",
    "scipy",
    "igraph",
    "leidenalg",
    "hnswlib",
    "annoy",
    "gseapy",
    "scrublet",
    "scvi",
    "torch",
    "jax",
    "jaxlib",
    "scimilarity",
]
for m in mods:
    try:
        __import__(m)
        ok(f"import {m}")
    except Exception as e:
        fail(f"import {m}", e)

try:
    import torch, scanpy as sc, scvi, jax

    print("\n[Versions]")
    print("python:", sys.version.split()[0])
    print("scanpy:", sc.__version__)
    print("anndata:", __import__("anndata").__version__)
    print("scvi-tools:", scvi.__version__)
    print("torch:", torch.__version__, "| CUDA runtime:", torch.version.cuda)
    print("jax:", jax.__version__)
    print("env python exe:", sys.executable)
    ok("version dump")
except Exception as e:
    fail("version dump", e)

# ---------- 2) TORCH / CUDA ----------
try:
    import torch

    print("\n[Torch / CUDA]")
    print("CUDA available:", torch.cuda.is_available())
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        print("GPU count:", torch.cuda.device_count())
        print("GPU name:", torch.cuda.get_device_name(0))
    x = torch.randn(1024, 1024, device=dev)
    y = x @ x
    _ = float(y.sum().item())
    ok(f"torch mm on {dev}")
except Exception as e:
    fail("torch / cuda test", e)

# ---------- 3) IGGRAPH + LEIDEN ----------
try:
    import igraph as ig, leidenalg

    g = ig.Graph.Erdos_Renyi(n=50, m=150)
    part = leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition)
    print("Leiden communities:", len(part))
    ok("igraph + leidenalg")
except Exception as e:
    fail("igraph + leidenalg", e)

# ---------- 4) SCANPY PIPELINE (no skmisc) ----------
try:
    import scanpy as sc, anndata as ad

    X = np.random.poisson(1.0, size=(300, 200)).astype(np.float32)
    adata = ad.AnnData(X=X)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    # skmisc 없이 동작하는 flavor 사용
    sc.pp.highly_variable_genes(adata, n_top_genes=100, flavor="cell_ranger")
    adata = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, n_comps=20, svd_solver="arpack")
    sc.pp.neighbors(adata, n_neighbors=10, n_pcs=15)
    sc.tl.leiden(adata, key_added="leiden", flavor="igraph", n_iterations=2)
    print("Leiden cats:", adata.obs["leiden"].unique().tolist())
    ok("scanpy minimal pipeline")
except Exception as e:
    fail("scanpy pipeline", e)

# ---------- 5) SCVI TOOLS (1 epoch) ----------
try:
    import scvi, anndata as ad

    Xc = np.random.poisson(1.0, size=(200, 100)).astype(np.int32)
    adata2 = ad.AnnData(X=Xc)
    scvi.model.SCVI.setup_anndata(adata2)
    model = scvi.model.SCVI(adata2, n_latent=5)
    model.train(max_epochs=1, accelerator="auto", devices=1, enable_progress_bar=False)
    z = model.get_latent_representation()
    print("SCVI latent shape:", z.shape)
    ok("scvi-tools train(1 epoch)")
except Exception as e:
    fail("scvi-tools train", e)

# ---------- 6) SCRUBLET (API 최신) ----------
try:
    import scrublet as scr

    counts = np.random.poisson(1.0, size=(100, 200)).astype(np.int32)
    s = scr.Scrublet(counts, expected_doublet_rate=0.06)
    # 전처리 후 차원 축소를 고려해 보수적으로 15로 설정
    scores, preds = s.scrub_doublets(min_counts=2, min_cells=2, n_prin_comps=15)
    print("Scrublet scores[0:5]:", np.round(scores[:5], 4))
    ok("scrublet basic")
except Exception as e:
    fail("scrublet", e)

# ---------- 7) HNSWLIB ----------
try:
    import hnswlib

    dim = 16
    data = np.random.rand(100, dim).astype("float32")
    index = hnswlib.Index(space="cosine", dim=dim)
    index.init_index(max_elements=100, ef_construction=100, M=16)
    index.add_items(data, np.arange(100))
    lbls, dists = index.knn_query(data[:1], k=5)
    print("hnsw top5 labels:", lbls[0].tolist())
    ok("hnswlib index/query")
except Exception as e:
    fail("hnswlib", e)

# ---------- 8) ANNOY ----------
try:
    from annoy import AnnoyIndex

    f = 16
    t = AnnoyIndex(f, "euclidean")
    vecs = np.random.rand(100, f).tolist()
    for i, v in enumerate(vecs):
        t.add_item(i, v)
    t.build(10)
    res = t.get_nns_by_item(0, 5)
    print("annoy top5:", res)
    ok("annoy build/query")
except Exception as e:
    fail("annoy", e)

# ---------- 9) GSEAPY (오프라인 prerank) ----------
try:
    from gseapy import prerank

    ranks = pd.Series(
        np.random.randn(200), index=[f"Gene{i}" for i in range(200)]
    ).sort_values(ascending=False)
    gs = {
        "dummy_set": [f"Gene{i}" for i in range(10)]
    }  # 인터넷 없이 실행하기 위한 간단 gene set
    outdir = "gseapy_test"
    os.makedirs(outdir, exist_ok=True)
    enr = prerank(
        rnk=ranks,
        gene_sets=gs,
        outdir=outdir,
        min_size=5,
        max_size=500,
        permutation_num=10,
        no_plot=True,
        seed=1,
        format="png",
    )
    print("gseapy results exist:", hasattr(enr, "res2d"))
    ok("gseapy prerank (offline)")
except Exception as e:
    fail("gseapy prerank", e)

# ---------- 10) JAX ----------
try:
    import jax, jax.numpy as jnp

    print("\n[JAX]")
    print("devices:", jax.devices())

    @jax.jit
    def f(x):
        return x * x + 1

    out = f(jnp.arange(5))
    print("jax jit output:", np.array(out))
    ok("jax jit")
except Exception as e:
    fail("jax", e)

print("\n🎉 DONE")
