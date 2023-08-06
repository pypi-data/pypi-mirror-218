import os

import pandas as pd
import pytest

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from spreadsheet_serializer.core import ENGINES


def get_test_spreadsheet_name(model, spreadsheet_fmt, ext=True):
    file_name = model.replace(".", "_").lower()
    if ext:
        return f"{file_name}.{spreadsheet_fmt}"
    return file_name


@pytest.fixture(params=ENGINES.keys())
def spreadsheet_fmt(request):
    return request.param


@pytest.fixture(
    params=[
        model._meta.label
        for model in apps.get_app_config("tests").get_models()
        if hasattr(model, "test_spreadsheet_datasets")
    ]
)
def model(request):
    return request.param


@pytest.fixture(
    params=[True, False],
    ids=[
        "fixture label w/ ext",
        "fixture label w/o ext",
    ],
)
def fixture_label_ext(request):
    return request.param


@pytest.fixture(
    params=[True, False],
    ids=[
        "'format' kwarg passed",
        "'format' kwarg not passed",
    ],
)
def format_kwarg(request):
    return request.param


@pytest.fixture(autouse=True)
def setup_test_data(model, spreadsheet_fmt, fixture_label_ext, format_kwarg):
    """
    Create, load, and remove spreadsheet fixture file.
    """
    # ===================================== Set up =====================================
    test_spreadsheet_datasets = apps.get_model(model).test_spreadsheet_datasets

    # Using the sequence of dicts returned by the models's test data, compose Pandas
    # data frames to be exported to a spreadsheet
    model_dfs = {
        dataset.get("model", model): pd.DataFrame(
            data=dataset["rows"],
            columns=dataset["columns"],
            dtype="object",
        )
        for dataset in test_spreadsheet_datasets
    }

    with pd.ExcelWriter(
        get_test_spreadsheet_name(model, spreadsheet_fmt),
        engine=ENGINES[spreadsheet_fmt],
    ) as writer:
        for model, df in model_dfs.items():
            df.to_excel(writer, sheet_name=model, index=False)

    # Deserialize using built-in 'loaddata' command
    command_kwargs = {"verbosity": 0}
    if format_kwarg:
        command_kwargs["format"] = spreadsheet_fmt
    fixture_label = get_test_spreadsheet_name(
        model, spreadsheet_fmt, ext=fixture_label_ext
    )
    call_command("loaddata", fixture_label, **command_kwargs)

    # ====================================== Test ======================================
    yield

    # =================================== Tear down ====================================
    os.remove(get_test_spreadsheet_name(model, spreadsheet_fmt))


@pytest.mark.django_db
def test_model_deserialization(model):
    """
    Assert that all the data were loaded for the model's datasets given.
    """
    manager = apps.get_model(model)._default_manager
    for dataset in manager.model.test_spreadsheet_datasets:
        rows, columns = dataset["rows"], dataset["columns"]

        # Check each row (object) individually
        for row in rows:
            # Convert a pair to sequences column/field-value to dict
            row_dict = {column: value for column, value in zip(columns, row)}

            # Assert that the object referred to by ID exists
            try:
                obj = manager.get(id=row_dict["id"])
            except manager.model.DoesNotExist:
                pytest.fail()

            # Perform extra checks for some "special" cases using non-standard
            # serialization for some of their fields.
            # ================================================================

            # Get the dataset model
            dataset_model = dataset.get("model", model)

            # Special case 1: ManyToManyField
            if dataset_model == "tests.ManyToManyFieldModel":
                related_ids = obj.many_to_many_field.all().values_list("id", flat=True)
                assert (
                    ", ".join(map(str, related_ids)) == row_dict["many_to_many_field"]
                )
            #
            # Special case 2: ContentType-related ForeignKey
            elif dataset_model == "tests.ContentTypeFieldModel":
                content_type = obj.content_type
                assert content_type == ContentType.objects.get_for_model(
                    apps.get_model(row_dict["content_type"])
                )
            #
            # Special case 3: User model
            elif dataset_model == "tests.User":
                assert obj.check_password(row_dict["password"])
