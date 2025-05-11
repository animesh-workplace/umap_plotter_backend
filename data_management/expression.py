from database import GeneExpressionTable

def get_single_gene_expression(gene, db):
    query = gene.strip()

    expressions = (
        db.query(GeneExpressionTable.expression_value)
        .filter(GeneExpressionTable.gene_name == query)
        .order_by(GeneExpressionTable.cell_id)
        .all()
    )

    result = [expr[0] for expr in expressions]
    return result