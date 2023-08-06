from ..core import SpreadsheetDeserializer, SpreadsheetSerializer


class OdsSerializationMixin:
    spreadsheet_fmt = "ods"


class Serializer(OdsSerializationMixin, SpreadsheetSerializer):
    pass


class Deserializer(OdsSerializationMixin, SpreadsheetDeserializer):
    pass
