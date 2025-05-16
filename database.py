import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Load your DB credentials from environment variables or hardcode for local dev
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://animesh:@localhost:5432/GeneEchelon"
)

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
    __tablename__ = "data_management_2dumapembedding"
    x = Column(Float)
    y = Column(Float)
    cluster = Column(String)
    cell_id = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)


class UMAP3DEmbeddingTable(Base):
    __tablename__ = "data_management_3dumapembedding"
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    cluster = Column(String)
    cell_id = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)


class TSNE2DEmbeddingTable(Base):
    __tablename__ = "data_management_2dtsneembedding"
    x = Column(Float)
    y = Column(Float)
    cluster = Column(String)
    cell_id = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)


class TSNE3DEmbeddingTable(Base):
    __tablename__ = "data_management_3dtsneembedding"
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    cluster = Column(String)
    cell_id = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)


class GeneTable(Base):
    __tablename__ = "data_management_gene"
    name = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)


class GeneExpressionTable(Base):
    __tablename__ = "data_management_geneexpression"
    cell_id = Column(String)
    gene_name = Column(String)
    expression_value = Column(Float)
    id = Column(Integer, primary_key=True, index=True)
