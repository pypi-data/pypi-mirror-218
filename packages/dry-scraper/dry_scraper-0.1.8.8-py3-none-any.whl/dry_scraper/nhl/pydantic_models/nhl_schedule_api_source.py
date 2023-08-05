import datetime
from typing import List, Optional

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import Field

from dry_scraper.nhl.pydantic_models.nhl_game_live_feed_api_source import (
    LiveFeedLink,
    Status,
)
from dry_scraper.nhl.pydantic_models.nhl_teams_api_source import (
    ShortTeam,
    ShortVenue,
)


class LeagueRecord(BaseModelNoException):
    wins: Optional[int]
    losses: Optional[int]
    ot: Optional[int]
    type: Optional[str]


class Team(BaseModelNoException):
    league_record: Optional[LeagueRecord] = Field(alias="leagueRecord")
    score: Optional[int]
    team: Optional[ShortTeam]


class Teams(BaseModelNoException):
    away: Optional[Team]
    home: Optional[Team]


class Game(BaseModelNoException):
    gamePk: Optional[int]
    link: Optional[LiveFeedLink]
    game_type: Optional[str] = Field(alias="gameType")
    season: Optional[str] = Field(alias="season")
    game_date: Optional[datetime.datetime] = Field(alias="gameDate")
    status: Optional[Status]
    teams: Optional[Teams]
    venue: Optional[ShortVenue]


class Date(BaseModelNoException):
    date: Optional[datetime.date]
    total_items: Optional[int] = Field(alias="totalItems")
    total_games: Optional[int] = Field(alias="totalGames")
    games: Optional[List[Game]]


class Schedule(BaseModelNoException):
    total_items: Optional[int] = Field(alias="totalItems")
    total_games: Optional[int] = Field(alias="totalGames")
    dates: Optional[List[Date]]


schedule_df_model = {
    "date": "str",
    "season": "int",
    "gamePk": "int",
    "game_type": "str",
    "game_date": "datetime64[m]",
    "abstract_game_state": "str",
    "coded_game_state": "int",
    "detailed_state": "str",
    "status_code": "int",
    "start_time_tbd": "bool",
    "away_team_id": "int",
    "away_team_name": "str",
    "away_record_wins": "int",
    "away_record_losses": "int",
    "away_record_ot": "int",
    "away_record_type": "str",
    "away_score": "int",
    "home_team_id": "int",
    "home_team_name": "str",
    "home_record_wins": "int",
    "home_record_losses": "int",
    "home_record_ot": "int",
    "home_record_type": "str",
    "home_score": "int",
    "venue_id": "int",
    "venue_name": "str",
}
