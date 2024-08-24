from collections import defaultdict

REG_NAMESPACE = defaultdict(dict)


def Register(description: str, tags: list):
    """Register implementation.

    Args:
        description (str): implementation description.
        tags (list, optional): tags to filter.
    """
    def wrapper(cls):
        REG_NAMESPACE[cls.__name__] = dict(instance=(cls),
                                           description=description,
                                           tags=tags)
        return cls
    return wrapper
