from pydantic import BaseModel

class UMAPEmbeddingSchema(BaseModel):
    x: float
    y: float
    cell_id: str

class UMAP3DEmbeddingSchema(BaseModel):
    x: float
    y: float
    z: float
    cell_id: str