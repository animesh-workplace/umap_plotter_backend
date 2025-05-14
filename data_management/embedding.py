from sqlalchemy import func
from database import UMAP2DEmbeddingTable, UMAP3DEmbeddingTable

def get_umap_embeddings_2d(db):
    embeddings = db.query(UMAP2DEmbeddingTable).order_by(UMAP2DEmbeddingTable.cell_id).all()
    return embeddings

def get_unique_cell_type_2d(db):
    cell_name = db.query(func.split_part(UMAP2DEmbeddingTable.cell_id, '_', 1)).distinct().all()
    return [expr[0] for expr in cell_name]

def get_umap_embeddings_3d(db):
    embeddings = db.query(UMAP3DEmbeddingTable).order_by(UMAP3DEmbeddingTable.cell_id).all()
    return embeddings