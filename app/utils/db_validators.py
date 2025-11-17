def valid_enum(enum_class):
    def decorator(func):
        def wrapper(self, value):
            if value not in enum_class:
                raise ValueError(f"Invalid value '{value}'. Must be one of: {list(enum_class)}.")
            return func(self, value)
        return wrapper
    return decorator