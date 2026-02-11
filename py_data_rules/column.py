from .data_type import DataType, XSDString


class Column:
    def __init__(
        self,
        label: str,
        data_type: DataType | None = None,
        nullable: bool | None = None,
    ) -> None:
        self.label: str = label
        self.data_type: DataType = data_type or XSDString()
        self.nullable: bool = nullable or False
