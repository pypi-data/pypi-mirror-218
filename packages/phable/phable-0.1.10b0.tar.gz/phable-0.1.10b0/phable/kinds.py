from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, Optional

# Note: Bool, Str, List, and Dict Haystack kinds are assumed to just be their Python
# type equivalents.  We may reevaluate this decision in the future.


@dataclass(frozen=True, slots=True)
class Grid:
    meta: dict[str, Any]
    cols: list[dict[str, Any]]
    rows: list[dict[str, Any]]

    @property
    def col_rename_map(self) -> dict[str, str]:
        rename_map: dict[str, str] = {}
        for col in self.cols:
            ori_col_name = col["name"]

            # refer cols named "ts" to "Timestamp"
            if ori_col_name == "ts":
                new_col_name = "Timestamp"

            # use Ref id for name of cols representing points
            elif "meta" in col.keys() and "id" in col["meta"].keys():
                new_col_name = col["meta"]["id"].val

            else:
                new_col_name = ori_col_name

            rename_map[ori_col_name] = new_col_name
        return rename_map

    @staticmethod
    def to_grid(rows: dict[str, Any] | list[dict[str, Any]]) -> Grid:
        if isinstance(rows, dict):
            rows = [rows]

        # might be able to find a nicer way to do this
        col_names: list[str] = []
        for row in rows:
            for col_name in row.keys():
                if col_name not in col_names:
                    col_names.append(col_name)

        cols = [{"name": name} for name in col_names]
        meta = {"ver": "3.0"}

        return Grid(meta=meta, cols=cols, rows=rows)

    def __str__(self):
        return "Grid"


@dataclass(frozen=True, slots=True)
class Number:
    val: int | float
    unit: str | None = None

    def __str__(self):
        return f"{self.val}{self.unit}"


# Marker() is a singleton
class Marker:
    __instance = None

    def __new__(cls):
        if Marker.__instance is None:
            Marker.__instance = object.__new__(cls)
        return Marker.__instance

    def __str__(self):
        return "\u2713"


# Remove() is a singleton
class Remove:
    __instance = None

    def __new__(cls):
        if Remove.__instance is None:
            Remove.__instance = object.__new__(cls)
        return Remove.__instance

    def __str__(self):
        return "remove"


# NA() is a singleton
class NA:
    __instance = None

    def __new__(cls):
        if NA.__instance is None:
            NA.__instance = object.__new__(cls)
        return NA.__instance

    def __str__(self):
        return "NA"


# TODO: Determine if I need make_handle func on Ref()
# TODO:  Should dis in Ref be mandatory?
# TODO:  Improve human readability
@dataclass(frozen=True, slots=True)
class Ref:
    val: str
    dis: str | None = None

    def __str__(self) -> str:
        return self.dis


@dataclass(frozen=True, slots=True)
class Date:
    val: date

    def __str__(self):
        return self.val.isoformat()


@dataclass(frozen=True, slots=True)
class Time:
    val: time

    # def __str__(self):
    #     return time.strftime(self.val, "%H:%M:%S%p")

    def __str__(self):
        return self.val.isoformat()


# TODO:
# - See if we can expose a nicer time zone display to end user
# - Map Haystack tz to IANA time zone database tz
# https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo.key
@dataclass(frozen=True, slots=True)
class DateTime:
    """
    Note:  tz attribute is the just the city name from the IANA database according to
    Haystack.
    """

    val: datetime
    tz: Optional[str] = None

    # def __str__(self):
    #     return datetime.strftime(self.val, "%d-%b-%Y %a %H:%M:%S%p %Z")

    def __str__(self):
        return self.val.isoformat()


@dataclass(frozen=True, slots=True)
class Uri:
    val: str

    def __str__(self):
        return self.val


@dataclass(frozen=True, slots=True)
class Coordinate:
    lat: float
    lng: float

    def __str__(self):
        return f"C({self.lat}, {self.lng})"


@dataclass(frozen=True, slots=True)
class XStr:
    type: str
    val: str

    def __str__(self):
        return f"({self.type}, {self.val})"


@dataclass(frozen=True, slots=True)
class Symbol:
    val: str

    def __str__(self):
        return f"^{self.val}"
