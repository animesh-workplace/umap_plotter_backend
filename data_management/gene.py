from database import GeneTable

def get_unique_gene_names(gene, db):
    query = gene.strip()
    gene_query = (
        db.query(GeneTable.name).filter(GeneTable.name.ilike(f"%{query}%")).limit(50)
        if query else 
        db.query(GeneTable.name).limit(50)
    )
    return [name for (name,) in gene_query.all()]
