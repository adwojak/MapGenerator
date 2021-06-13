def round_value(value):
    integer = int(value)
    if value - integer > 0.99999999:
        return integer + 1
    return value
