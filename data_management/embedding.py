from database import UMAPEmbeddingTable

def get_umap_embeddings(db):
    embeddings = db.query(UMAPEmbeddingTable).order_by(UMAPEmbeddingTable.cell_id).all()
    return embeddings