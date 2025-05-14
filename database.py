import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Load your DB credentials from environment variables or hardcode for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://animesh:@localhost:5432/GeneEchelon")

# Create the engine and local session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session in FastAPI routes
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for declarative models
Base = declarative_base()

class UMAP2DEmbeddingTable(Base):
    __tablename__ = "data_management_umapembedding"
    id = Column(Integer, primary_key=True, index=True)
    cell_id = Column(String, index=True)
    x = Column(Float)
    y = Column(Float)

class UMAP3DEmbeddingTable(Base):
    __tablename__ = "data_management_3dumapembedding"
    id = Column(Integer, primary_key=True, index=True)
    cell_id = Column(String, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

class GeneTable(Base):
    __tablename__ = "data_management_gene"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class GeneExpressionTable(Base):
    __tablename__ = "data_management_geneexpression"
    id = Column(Integer, primary_key=True, index=True)
    cell_id = Column(String)
    gene_name = Column(String)
    expression_value = Column(Float)