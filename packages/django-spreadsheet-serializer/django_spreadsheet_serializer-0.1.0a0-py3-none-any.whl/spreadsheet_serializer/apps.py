from django import apps


class SpreadsheetSerializerConfig(apps.AppConfig):
    """
    Configuration of the 'spreadsheet_serializer' app.
    """

    name = "spreadsheet_serializer"

    def ready(self):
        self._register_serializers()

    def _register_serializers(self):
        from django.core.serializers import register_serializer

        from .core import ENGINES

        for spreadsheet_fmt in ENGINES:
            register_serializer(
                spreadsheet_fmt,
                f"spreadsheet_serializer.serializers.{spreadsheet_fmt}_serializer",
            )
