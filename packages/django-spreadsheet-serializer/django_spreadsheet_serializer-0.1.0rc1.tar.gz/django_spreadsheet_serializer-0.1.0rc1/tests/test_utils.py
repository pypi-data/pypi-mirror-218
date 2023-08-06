import pytest

from spreadsheet_serializer.utils import is_valid_model_identifier


@pytest.mark.parametrize(
    "name, valid",
    [
        ("tests.CharFieldModel", True),
        ("tests.charfieldmodel", True),
        ("CharFieldModel", False),
        ("tests.NonExistingModel", False),
    ],
    ids=[
        "full label (Pascal-case)",
        "full label (lowercase)",
        "name only",
        "non-existing model",
    ],
)
def test_is_valid_model_identifier(name, valid):
    assert is_valid_model_identifier(name) == valid
