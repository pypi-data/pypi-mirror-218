from typing import List, Optional

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import constr, Field

ConferenceLink = constr(regex=r"^/api/v1/conferences/(\d+|null)$")


class Conference(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: Optional[ConferenceLink]
    abbreviation: Optional[str]
    short_name: Optional[str] = Field(alias="shortName")
    active: Optional[bool]


class ShortConference(BaseModelNoException):
    id: Optional[Optional[int]]
    name: Optional[Optional[str]]
    link: Optional[ConferenceLink]


class Conferences(BaseModelNoException):
    conferences: Optional[List[Conference]]
