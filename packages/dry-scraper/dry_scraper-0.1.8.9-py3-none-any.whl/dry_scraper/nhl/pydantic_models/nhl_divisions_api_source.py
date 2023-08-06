from typing import List, Optional, Literal

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import Field, constr

from dry_scraper.nhl.pydantic_models.nhl_conferences_api_source import (
    ShortConference,
)

DivisionLink = constr(regex=r"^/api/v1/divisions/(\d+|null)$")


class ShortDivision(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    name_short: Optional[str] = Field(alias="nameShort")
    link: Optional[DivisionLink]
    abbreviation: Optional[str]


class Division(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    name_short: Optional[str] = Field(alias="nameShort")
    link: Optional[DivisionLink]
    abbreviation: Optional[str]
    conference: Optional[ShortConference]
    active: Optional[bool]


class NullDivision(BaseModelNoException):
    link: Optional[Literal["/api/v1/divisions/null"]]

    class Config:
        extra = "forbid"


class Divisions(BaseModelNoException):
    divisions: Optional[List[NullDivision | Division]]
