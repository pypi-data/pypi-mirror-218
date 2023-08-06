from datetime import date
from typing import List, Optional

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import constr, Field

from dry_scraper.nhl.pydantic_models.nhl_teams_api_source import ShortTeam

PersonIdString = constr(regex=r"^(ID)?\d{4,7}$")


PersonLink = constr(regex=r"^/api/v1/people/(\d+|null)$")


class Position(BaseModelNoException):
    code: Optional[str]
    name: Optional[str]
    type: Optional[str]
    abbreviation: Optional[str]


class Player(BaseModelNoException):
    id: Optional[int]
    full_name: Optional[str] = Field(alias="fullName")
    link: Optional[PersonLink]
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    primary_number: Optional[int] = Field(alias="primaryNumber")
    birth_date: Optional[date] = Field(alias="birthDate")
    current_age: Optional[int] = Field(alias="currentAge")
    birth_city: Optional[str] = Field(alias="birthCity")
    birth_state_province: Optional[str] = Field(alias="birthStateProvince")
    birth_country: Optional[str] = Field(alias="birthCountry")
    nationality: Optional[str]
    height: Optional[str]
    weight: Optional[int]
    active: Optional[bool]
    alternate_captain: Optional[bool] = Field(alias="alternateCaptain")
    captain: Optional[bool]
    rookie: Optional[bool]
    shoots_catches: Optional[str] = Field(alias="shootsCatches")
    roster_status: Optional[str] = Field(alias="rosterStatus")
    current_team: Optional[ShortTeam] = Field(alias="currentTeam")
    primary_position: Optional[Position] = Field(alias="primaryPosition")


class Person(BaseModelNoException):
    id: Optional[PersonIdString]
    full_name: Optional[str] = Field(alias="fullName")
    link: Optional[PersonLink]


class People(BaseModelNoException):
    people: Optional[List[Player]]
