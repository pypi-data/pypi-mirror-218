from numpy import random

from scanpy.datasets import pbmc68k_reduced

def get_toy_adata():
    adata = pbmc68k_reduced()
    sample_key = 'sample'
    
    rng = random.default_rng(0)
    
    # create fake samples
    adata.obs[sample_key] = rng.choice(['A', 'B', 'C', 'D'], size=len(adata.obs))
    
    # group samples into conditions
    adata.obs['case'] = adata.obs[sample_key].map({'A': 'yes', 'B': 'yes', 'C': 'no', 'D': 'no'})
    
    return adata
    