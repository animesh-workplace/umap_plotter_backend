from typing import List
from database import get_db
from sqlalchemy.orm import  Session
from schema import UMAPEmbeddingSchema
from data_management.gene import get_unique_gene_names
from data_management.embedding import get_umap_embeddings
from fastapi import FastAPI, Depends, Query, HTTPException
from data_management.expression import get_single_gene_expression

# FastAPI app
app = FastAPI()

@app.get("/api/genes/autocomplete", response_model=List[str])
def API_GET_GENE_LIST(gene: str = Query(default="", alias="gene"), database: Session = Depends(get_db)):
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

@app.get("/api/umap/", response_model=List[UMAPEmbeddingSchema])
def API_GET_UMAP_EMBEDDING(database: Session = Depends(get_db)):
    """
    Retrieve all UMAP embeddings stored in the database.

    Returns:
    --------
    List of UMAP embeddings ordered by `cell_id`.
    """
    return get_umap_embeddings(database)

@app.get("/api/genes/single-expr/", response_model=List[float])
def API_GET_SINGLE_GENE_EXPRESSION(
    gene_name: str = Query(..., description="Gene name to filter by"),
    database: Session = Depends(get_db)
):
    """
    Get expression values for a specific gene across all cells
    
    Parameters:
    - gene_name: Required query parameter specifying the gene to filter by
    
    Returns:
    - List of expression values ordered by cell_id
    """
    if not gene_name:
        raise HTTPException(
            status_code=400,
            detail="gene_name parameter is required"
        )
    
    return get_single_gene_expression(gene_name, database)