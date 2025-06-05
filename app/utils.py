def get_bbox_id(x1, y1, x2, y2, tolerance=10):
    x1 = (x1 // tolerance) * tolerance
    y1 = (y1 // tolerance) * tolerance
    x2 = (x2 // tolerance) * tolerance
    y2 = (y2 // tolerance) * tolerance
    return f"{x1}-{y1}-{x2}-{y2}"
