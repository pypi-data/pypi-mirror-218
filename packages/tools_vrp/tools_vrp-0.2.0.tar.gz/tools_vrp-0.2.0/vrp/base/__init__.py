

from typing import Any


class ValuationReportData:
    def __init__(self) -> None:
        self.details: list[CaseDict] = []
        self.product: CaseDict = None


TABLE_NAME = "__tablename__"
DATASOUCE = "__datasource__"

ENV_FILE_NAME = "$FILE_NAME"
ENV_PROCESS_TIME = "$PROCESS_TIME"
ENV_DB_SINK = "__DB_SINK"
ENV_DEBUG = "__DEBUG"


class CaseDict(dict[str, Any]):
    def __contains__(self, __o: object) -> bool:
        if super().__contains__(__o):
            return True
        return self.__find_key__(__o) is not None

    def __find_key__(self, __o: str) -> str:
        for k in self.keys():
            if k.lower() == __o.lower():
                return k
        return None

    def __getitem__(self, __key: str) -> Any:
        if super().__contains__(__key):
            return super().__getitem__(__key)
        key = self.__find_key__(__key)
        if key:
            return super().__getitem__(key)
        raise KeyError(__key)

    def to_lower_dict(self):
        return {k.lower(): v for k, v in self.items()}
