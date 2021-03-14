def get_by_index(source_list, idx, default=None):
    try:
        return source_list[idx]
    except IndexError:
        return default
