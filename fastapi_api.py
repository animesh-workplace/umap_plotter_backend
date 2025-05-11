from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import time

# Replace with your actual PostgreSQL connection URI
DATABASE_URL = "postgresql://animesh:@localhost:5432/GeneEchelon"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to get expression values
@app.get("/expression_values")
def get_expression_values(
    gene_name: str = Query(..., description="Gene name to query"),
    db: Session = Depends(get_db)
):
    if not gene_name:
        raise HTTPException(status_code=400, detail="gene_name is required")

    # Raw SQL query using safe parameterization
    query = text("""
        SELECT expression_value
        FROM data_management_geneexpression
        WHERE gene_name = :gname
        ORDER BY cell_id
    """)

    start = time.time()
    result = db.execute(query, {"gname": gene_name}).fetchall()
    end = time.time()

    print('DB execution time', end-start )

    # Flatten the result
    values = [row[0] for row in result]

    return JSONResponse(content=values)
