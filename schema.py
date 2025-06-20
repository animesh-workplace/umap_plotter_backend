from pydantic import BaseModel


class UMAP2DEmbeddingSchema(BaseModel):
    x: float
    y: float
    cell_id: str
    cluster: str


class UMAP3DEmbeddingSchema(BaseModel):
    x: float
    y: float
    z: float
    cell_id: str
    cluster: str


class SpatialPositionSchema(BaseModel):
    x: int
    y: int
    sample: str
    cell_id: str
    background: int


class SpatialExpressionSchema(BaseModel):
    sample: str
    cell_id: str
    caf_1: float
    caf_2: float
    caf_3: float
    caf_4: float
    caf_5: float
    caf_6: float
    caf_7: float
    caf_8: float
    caf_9: float
