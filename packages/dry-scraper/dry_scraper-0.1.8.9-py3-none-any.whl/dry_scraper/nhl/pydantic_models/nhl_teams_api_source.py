from typing import Optional, List

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import constr, Field, HttpUrl

from dry_scraper.nhl.pydantic_models.nhl_conferences_api_source import (
    ShortConference,
)
from dry_scraper.nhl.pydantic_models.nhl_divisions_api_source import (
    NullDivision,
    ShortDivision,
)

VenueLink = constr(regex=r"^/api/v1/venues/(\d+|null)$")

FranchiseLink = constr(regex=r"^/api/v1/franchises/(\d+|null)$")
TeamLink = constr(regex=r"^/api/v1/teams/(\d+|null)$")


class ShortTeam(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: Optional[TeamLink]
    abbreviation: Optional[str]
    tricode: Optional[str] = Field(alias="triCode")


class TimeZone(BaseModelNoException):
    id: Optional[str]
    offset: Optional[int]
    tz: Optional[str]


class Venue(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: Optional[VenueLink]
    city: Optional[str]
    time_zone: Optional[TimeZone] = Field(alias="timeZone")


class ShortVenue(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: Optional[VenueLink]


class Franchise(BaseModelNoException):
    franchise_id: Optional[int] = Field(alias="franchiseId")
    team_name: Optional[str] = Field(alias="teamName")
    link: Optional[FranchiseLink]


class Team(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: Optional[TeamLink]
    venue: Optional[Venue]
    abbreviation: Optional[str]
    tricode: Optional[str] = Field(alias="triCode")
    team_name: Optional[str] = Field(alias="teamName")
    location_name: Optional[str] = Field(alias="locationName")
    first_year_of_play: Optional[str] = Field(alias="firstYearOfPlay")
    division: Optional[ShortDivision | NullDivision]
    conference: Optional[ShortConference]
    franchise: Optional[Franchise]
    short_name: Optional[str] = Field(alias="shortName")
    official_site_url: Optional[HttpUrl] = Field(alias="officialSiteUrl")
    franchise_id: Optional[int] = Field(alias="franchiseId")
    active: Optional[bool]


class Teams(BaseModelNoException):
    teams: Optional[List[Team]]
