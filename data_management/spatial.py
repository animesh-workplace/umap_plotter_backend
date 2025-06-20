from database import SpatialExpressionTable, SpatialPositionTable


def get_spatial_position_for_image(sample_name, db):
    query = sample_name.strip()

    positions = (
        db.query(SpatialPositionTable)
        .filter(
            SpatialPositionTable.sample == query, SpatialPositionTable.background == 1
        )
        .all()
    )

    return positions


def get_spatial_expression_for_image(sample_name, db):
    query = sample_name.strip()

    positions = (
        db.query(SpatialExpressionTable)
        .filter(SpatialExpressionTable.sample == query)
        .all()
    )

    return positions
