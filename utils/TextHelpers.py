def pronoun_3p_subject(obj) -> str:
    if not hasattr(obj, "gender"):
        return "they"
    elif obj.gender == "male":
        return "he"
    elif obj.gender == "female":
        return "she"
    else:
        return "they"


def pronoun_3p_object(obj) -> str:
    if not hasattr(obj, "gender"):
        return "them"
    elif obj.gender == "male":
        return "him"
    elif obj.gender == "female":
        return "her"
    else:
        return "them"


def pronoun_3p_possessive(obj) -> str:
    if not hasattr(obj, "gender"):
        return "their"
    elif obj.gender == "male":
        return "his"
    elif obj.gender == "female":
        return "her"
    else:
        return "their"


def enumerate_objects(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    if len(items) > 2:
        return (", ".join(items[:-1]))+f", and {items[-1]}"
    raise Exception("Call to TextHelpers.enumerate_objects contained less than 1 item.")


def pluralize(item: str, count: int) -> str:
    if count == 1:
        return item
    if count == 0 or count > 1:
        return f"{item}s"
    raise Exception("Call to TextHelpers.pluralize had less than 0 count")
