from decimal import Decimal


def float_to_decimal(value):
    """
    Walk the given data structure and turn all instances of float into double.
    """
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, list):
        return [float_to_decimal(child) for child in value]
    if isinstance(value, dict):
        return {k: float_to_decimal(v) for k, v in value.items()}
    return value
