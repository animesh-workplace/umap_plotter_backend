from database import GeneExpressionTable

def get_single_gene_expression(gene, db):
    query = gene.strip()

    expressions = (
        db.query(GeneExpressionTable)
        .filter(GeneExpressionTable.gene_name == query)
        .order_by(GeneExpressionTable.cell_id)
        .all()
    )

    # print(expressions)
    # result = [{expr[1]: expr} for expr in expressions]
    return expressions