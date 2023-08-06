from django.apps import apps


def is_valid_model_identifier(name):
    """
    Check if the name given represents a valid model identifier.

    Identifier is the model label retrieved from 'label' Meta option.
    """
    if not name.count("."):
        return False
    try:
        apps.get_model(name)
    except (ValueError, LookupError):
        return False
    return True
