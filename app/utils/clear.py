import math

def sanitize_floats(doc):
    """Replace NaN or Infinity float values with None."""
    for key, value in doc.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            doc[key] = None
        elif isinstance(value, dict):
            sanitize_floats(value)
    return doc