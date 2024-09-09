def validate_instance(value, expected_type):
    if not isinstance(value, expected_type):
        raise TypeError(f"""Invalid parameter. {value} must be an instance of 
                        {expected_type.__name__}""")