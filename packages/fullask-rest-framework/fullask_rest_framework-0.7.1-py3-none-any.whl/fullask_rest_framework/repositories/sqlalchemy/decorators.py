from functools import wraps


def read_by_fields(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        field_name = func.__name__[len("read_by_") :]
        if field_name in kwargs:
            field_value = kwargs[field_name]
        else:
            if len(args) < 1:
                raise ValueError(f"{field_name} argument is missing")
            field_value = args[0]
        query_result = (
            self.get_model().query.filter_by(**{field_name: field_value}).first()
        )
        return query_result if query_result else None

    return wrapper
