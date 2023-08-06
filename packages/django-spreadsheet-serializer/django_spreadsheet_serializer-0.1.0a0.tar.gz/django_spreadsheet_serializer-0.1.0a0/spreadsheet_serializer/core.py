from itertools import chain

import pandas as pd

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.base import (
    DeserializedObject,
    Deserializer,
    Serializer,
    build_instance,
)
from django.db import models

from .utils import is_valid_model_identifier

ENGINES = {
    "ods": "odf",
    "xlsx": "openpyxl",
}

UserModel = get_user_model()


class SpreadsheetSerializer(Serializer):
    """
    Serialization utility to export Django model to Pandas data frame a spreadsheet.
    """

    spreadsheet_fmt = None


class SpreadsheetDeserializer(Deserializer):
    """
    Deserialization utility to create Django model objects from a spreadsheet.
    """

    spreadsheet_fmt = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Stream spreadsheet
        spreadsheet = pd.ExcelFile(self.stream, engine=ENGINES[self.spreadsheet_fmt])

        # Use only the sheets named as the models are labeled in the app registry
        sheet_names = list(filter(is_valid_model_identifier, spreadsheet.sheet_names))

        # Get all the spreadsheet data as a dict of Pandas data frames
        model_dfs = pd.read_excel(spreadsheet, sheet_name=sheet_names, dtype="object")

        # For each data frame remove the columns not associated with any model field
        for model_label, df in model_dfs.items():
            opts = apps.get_model(model_label)._meta
            field_names = [
                field.name
                for field in chain(
                    opts.concrete_fields,
                    opts.many_to_many,
                )
            ]
            cols_to_drop = [col for col in df.columns if col not in field_names]
            model_dfs[model_label] = df.drop(cols_to_drop, axis=1)

        # Transform 'model_dfs' into an iterator of '(model, row)' tuples, where 'row'
        # is a dict representation of model instance to be deserialized, whereas 'model'
        # is the model class
        self.fixtures = chain(
            *(
                [
                    (apps.get_model(model_label), row)
                    for row in df.to_dict(orient="records")
                ]
                for model_label, df in model_dfs.items()
            )
        )

        # Get the database connection name
        self.using = self.options.get("using", "default")

    def __next__(self):
        # Get the fixture model, data, and fields
        _model, _row = next(self.fixtures)

        # Many-to-many relationship data
        m2m_data = {}

        # List of the fixtures keys corresponding to many-to-many relations
        m2m_fields = []

        # Update fixture data in some special types of fields
        row = {}
        for field_name, field_value in _row.items():
            field = _model._meta.get_field(field_name)

            # Handle Pandas 'nan' values of nullable and blank fields
            if field.null and pd.isnull(field_value):
                field_value = None
            elif field.blank and pd.isnull(field_value):
                field_value = ""
            if not field_value:
                field_value = field.to_python(field_value)

            # ForeignKey or OneToOneField field to ContentType
            # (ContentType objects can be referred to as full model labels)
            if (
                isinstance(field, (models.ForeignKey, models.OneToOneField))
                and field_value
                and field.related_model == ContentType
            ):
                # ContentType objects are referred to using model labels
                app_label, model_name = field_value.split(".")
                field_value = (
                    ContentType._default_manager.using(self.using)
                    .get(app_label=app_label, model=model_name.lower())
                    .id
                )

            # ManyToManyField field
            # (related objects can be referred to a list of comma-separated IDs)
            if isinstance(field, models.ManyToManyField):
                m2m_fields.append(field_name)
                if field_value:
                    manager = field.related_model._default_manager.using(self.using)
                    related_objs = [
                        manager.get(pk=related_pk)
                        for related_pk in [
                            int(value) for value in str(field_value).split(",")
                        ]
                    ]
                    m2m_data.update({field.name: related_objs})

            # Update FK field name to column name, therefore let Django build related
            # instance on its own
            field_id = (
                f"{field_name}_id"
                if isinstance(field, (models.ForeignKey, models.OneToOneField))
                else field_name
            )

            # Save the updated value to the fixture's data
            row[field_id] = field_value

        # Exclude many-to-many relations from the data
        # (the data on those fields are in 'm2m_data' dict)
        for m2m_field in m2m_fields:
            row.pop(m2m_field)

        # Build the model instance
        obj = build_instance(_model, row, db=self.using)

        # Perform an extra step of password hashing in the case of the user model
        if isinstance(obj, UserModel):
            obj.set_password(obj.password)

        return DeserializedObject(obj, m2m_data=m2m_data)
