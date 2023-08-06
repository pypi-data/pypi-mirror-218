import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import classproperty


class CharFieldModel(models.Model):
    char_field = models.CharField(max_length=255)

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "char_field"],
                rows=[
                    (1, "char-a"),
                    (2, "char-b"),
                    (3, "char-c"),
                ],
            ),
        ]


class TextFieldModel(models.Model):
    text_field = models.TextField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "text_field"],
                rows=[
                    (1, "text-a"),
                    (2, "text-b"),
                    (3, "text-c"),
                ],
            ),
        ]


class SlugFieldModel(models.Model):
    slug_field = models.SlugField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "slug_field"],
                rows=[
                    (1, "slug-a"),
                    (2, "slug-b"),
                    (3, "slug-c"),
                ],
            ),
        ]


class IntegerFieldModel(models.Model):
    integer_field = models.IntegerField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "integer_field"],
                rows=[
                    (1, 1),
                    (2, 10),
                    (3, 100),
                ],
            ),
        ]


class DecimalFieldModel(models.Model):
    decimal_field = models.DecimalField(decimal_places=2, max_digits=3)

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "decimal_field"],
                rows=[
                    (1, Decimal("3.14")),
                    (2, Decimal("2.73")),
                    (3, Decimal("1.41")),
                ],
            ),
        ]


class BooleanFieldModel(models.Model):
    boolean_field = models.BooleanField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "boolean_field"],
                rows=[
                    (1, True),
                    (2, False),
                ],
            ),
        ]


class DateFieldModel(models.Model):
    date_field = models.DateField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "date_field"],
                rows=[
                    (1, datetime.date(1990, 1, 1)),
                    (2, datetime.date(1991, 1, 1)),
                    (3, datetime.date(1992, 1, 1)),
                ],
            ),
        ]


class DateTimeFieldModel(models.Model):
    date_time_field = models.DateTimeField()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "date_time_field"],
                rows=[
                    (1, datetime.datetime(1990, 1, 1, 12, 0, 0)),
                    (2, datetime.datetime(1991, 1, 1, 13, 0, 0)),
                    (3, datetime.datetime(1992, 1, 1, 14, 0, 0)),
                ],
            ),
        ]


class RelatedModel(models.Model):
    pass


class RelatedModelMixin:
    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                model="tests.RelatedModel",
                columns=["id"],
                rows=[
                    (1,),
                    (2,),
                    (3,),
                ],
            ),
        ]


class ForeignKeyModel(RelatedModelMixin, models.Model):
    foreign_key_field = models.ForeignKey(
        RelatedModel, on_delete=models.CASCADE, blank=True, null=True
    )

    @classproperty
    def test_spreadsheet_datasets(cls):
        return super().test_spreadsheet_datasets + [
            dict(
                columns=["id", "foreign_key_field"],
                rows=[
                    (1, 1),
                    (2, 1),
                    (3, 1),
                    (4, None),
                ],
            ),
        ]


class OneToOneFieldModel(RelatedModelMixin, models.Model):
    one_to_one_field = models.OneToOneField(
        RelatedModel, on_delete=models.CASCADE, blank=True, null=True
    )

    @classproperty
    def test_spreadsheet_datasets(cls):
        return super().test_spreadsheet_datasets + [
            dict(
                columns=["id", "one_to_one_field"],
                rows=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, None),
                ],
            ),
        ]


class ManyToManyFieldModel(RelatedModelMixin, models.Model):
    many_to_many_field = models.ManyToManyField(RelatedModel, blank=True)

    @classproperty
    def test_spreadsheet_datasets(cls):
        return super().test_spreadsheet_datasets + [
            dict(
                columns=["id", "many_to_many_field"],
                rows=[
                    (1, "1, 2, 3"),
                    (2, "1, 3"),
                    (3, "1, 2"),
                    (4, ""),
                ],
            ),
        ]


class ContentTypeFieldModel(RelatedModelMixin, models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @classproperty
    def test_spreadsheet_datasets(cls):
        return super().test_spreadsheet_datasets + [
            dict(
                columns=["id", "content_type", "object_id"],
                rows=[
                    (1, "tests.RelatedModel", 1),
                    (2, "tests.RelatedModel", 2),
                    (3, "tests.RelatedModel", 3),
                ],
            ),
        ]


class BlankFieldModel(models.Model):
    blank_field = models.CharField(max_length=255, blank=True)

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "blank_field"],
                rows=[
                    (1, ""),
                    (2, "char-b"),
                    (3, ""),
                ],
            ),
        ]


class NullFieldModel(models.Model):
    null_field = models.IntegerField(blank=True, null=True)

    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "null_field"],
                rows=[
                    (1, None),
                    (2, 10),
                    (3, None),
                ],
            ),
        ]


class User(AbstractUser):
    @classproperty
    def test_spreadsheet_datasets(cls):
        return [
            dict(
                columns=["id", "username", "password"],
                rows=[
                    (1, "user-1", "password-1"),
                    (2, "user-2", "password-2"),
                    (3, "user-3", "password-3"),
                ],
            )
        ]
