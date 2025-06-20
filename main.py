from database import get_db
from typing import List, Dict
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from data_management.gene import get_unique_gene_names
from fastapi import FastAPI, Depends, Query, HTTPException
from data_management.expression import get_single_gene_expression
from data_management.embedding import (
    get_umap_embeddings_2d,
    get_umap_embeddings_3d,
    get_tsne_embeddings_2d,
    get_tsne_embeddings_3d,
    get_unique_cell_type_2d,
)
from schema import (
    UMAP2DEmbeddingSchema,
    UMAP3DEmbeddingSchema,
    SpatialPositionSchema,
    SpatialExpressionSchema,
)
from data_management.spatial import (
    get_spatial_position_for_image,
    get_spatial_expression_for_image,
)

# FastAPI app
app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
)


@app.get("/api/genes/autocomplete", response_model=List[str])
def API_GET_GENE_LIST(
    gene: str = Query(default="", alias="gene"), database: Session = Depends(get_db)
):
    """
    Retrieve a list of unique gene names for autocomplete suggestions.

    This endpoint performs a case-insensitive search on the `data_management_gene` table
    using the provided `gene` query string. It returns up to 50 distinct gene names
    that contain the input substring, ordered alphabetically.

    Parameters:
    ----------
    gene : str
        A partial or full gene name to search for. Defaults to an empty string, which returns the first 50 genes.

    database : Session
        A SQLAlchemy database session injected via dependency.

    Returns:
    -------
    List[str]
        A list of up to 50 matching gene names.
    """
    return get_unique_gene_names(gene, database)


@app.get("/api/umap/2d/", response_model=List[UMAP2DEmbeddingSchema])
def API_GET_UMAP_EMBEDDING(database: Session = Depends(get_db)):
    """
    Retrieve all UMAP embeddings stored in the database.

    Returns:
    --------
    List of UMAP embeddings ordered by `cell_id`.
    """
    return get_umap_embeddings_2d(database)


@app.get("/api/umap/3d/", response_model=List[UMAP3DEmbeddingSchema])
def API_GET_UMAP_3DEMBEDDING(database: Session = Depends(get_db)):
    """
    Retrieve all UMAP embeddings stored in the database.

    Returns:
    --------
    List of UMAP embeddings ordered by `cell_id`.
    """
    return get_umap_embeddings_3d(database)


@app.get("/api/umap/2d/celltype", response_model=List[str])
def API_GET_UMAP_CELL_TYPE(database: Session = Depends(get_db)):
    return get_unique_cell_type_2d(database)


@app.get("/api/genes/single-expr/", response_model=Dict[str, float])
def API_GET_SINGLE_GENE_EXPRESSION(
    gene_name: str = Query(..., description="Gene name to filter by"),
    database: Session = Depends(get_db),
):
    """
    Get expression values for a specific gene across all cells

    Parameters:
    - gene_name: Required query parameter specifying the gene to filter by

    Returns:
    - List of expression values ordered by cell_id
    """
    if not gene_name:
        raise HTTPException(status_code=400, detail="gene_name parameter is required")

    return {
        item.cell_id: item.expression_value
        for item in get_single_gene_expression(gene_name, database)
    }


@app.get("/api/tsne/2d/", response_model=List[UMAP2DEmbeddingSchema])
def API_GET_TSNE_EMBEDDING(database: Session = Depends(get_db)):
    """
    Retrieve all TSNE embeddings stored in the database.

    Returns:
    --------
    List of TSNE embeddings ordered by `cell_id`.
    """
    return get_tsne_embeddings_2d(database)


@app.get("/api/tsne/3d/", response_model=List[UMAP3DEmbeddingSchema])
def API_GET_TSNE_3DEMBEDDING(database: Session = Depends(get_db)):
    """
    Retrieve all TSNE embeddings stored in the database.

    Returns:
    --------
    List of TSNE embeddings ordered by `cell_id`.
    """
    return get_tsne_embeddings_3d(database)


@app.get("/api/spatial/position/", response_model=List[SpatialPositionSchema])
def API_GET_SPATIAL_POSITION(
    sample_name: str = Query(
        ..., description="Sample name to get the positions for the image"
    ),
    database: Session = Depends(get_db),
):
    """
    Retrieve spatial coordinates for a given sample image.

    This endpoint returns a list of spatial positions (e.g., x, y coordinates)
    of cells or spots associated with a specified sample. It can be used to
    reconstruct the spatial layout of gene expression or other spatial features.

    Parameters:
    - sample_name (str): The name of the sample for which spatial positions are requested.

    Returns:
    - List[SpatialPositionSchema]: A list of spatial position objects including cell ID,
      coordinates, and background flag.
    """
    return get_spatial_position_for_image(sample_name, database)


@app.get("/api/spatial/expression/", response_model=List[SpatialExpressionSchema])
def API_GET_SPATIAL_EXPRESSION(
    sample_name: str = Query(
        ..., description="Sample name to get the expression for the image"
    ),
    database: Session = Depends(get_db),
):
    """
    Retrieve spatial gene expression data for a given sample image.

    This endpoint returns gene expression levels mapped to spatial coordinates
    for a specific sample. The data can be used for visualizing or analyzing
    spatial transcriptomics data in tissue sections.

    Parameters:
    - sample_name (str): The name of the sample for which gene expression data is requested.

    Returns:
    - List[SpatialExpressionSchema]: A list of expression entries including gene ID,
      expression value, and corresponding spatial location.
    """
    return get_spatial_expression_for_image(sample_name, database)
