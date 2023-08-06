from ..core import SpreadsheetDeserializer, SpreadsheetSerializer


class XlsxSerializationMixin:
    spreadsheet_fmt = "xlsx"


class Serializer(XlsxSerializationMixin, SpreadsheetSerializer):
    pass


class Deserializer(XlsxSerializationMixin, SpreadsheetDeserializer):
    pass
