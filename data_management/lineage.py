from database import CAF_LineagesTable


def get_single_lineage_expression(lineage, db):
    lineage = lineage.strip().lower().replace(" ", "_")

    # Define the valid lineage columns
    valid_lineages = {
        "lineage_1": CAF_LineagesTable.lineage_1,
        "lineage_2": CAF_LineagesTable.lineage_2,
        "lineage_3": CAF_LineagesTable.lineage_3,
        "lineage_4": CAF_LineagesTable.lineage_4,
    }

    # Check if the lineage input is valid
    if lineage not in valid_lineages:
        raise ValueError(
            f"Invalid lineage name: {lineage}. Must be one of {list(valid_lineages.keys())}"
        )

    # Dynamically select the chosen column
    selected_column = valid_lineages[lineage]

    # Query only that specific column
    expressions = db.query(CAF_LineagesTable.cell_id, selected_column).all()

    return expressions
