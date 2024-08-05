def parse_float(float_str):
    try:
        return float(float_str)
    except ValueError:
        print(f"Invalid float format: {float_str}")
        return None
