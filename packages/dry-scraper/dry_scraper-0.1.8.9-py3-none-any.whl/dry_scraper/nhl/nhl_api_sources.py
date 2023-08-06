import json
import pandas as pd
import pydantic
import re
import requests
from abc import ABC
from datetime import datetime
from typing import ClassVar, TypeVar, Self, Any
from sqlalchemy import Select, select, Engine
from sqlalchemy.orm import Session


from dry_scraper.nhl.pydantic_models import (
    nhl_schedule_api_source,
    nhl_teams_api_source,
    nhl_divisions_api_source,
    nhl_conferences_api_source,
    nhl_game_live_feed_api_source,
)
from dry_scraper.data_source import DataSource, CachedDataSource

DataModel = TypeVar("DataModel", bound=pydantic.BaseModel)


class NhlApiSource(DataSource, ABC):
    """
    Abstract subclass of DataSource that represents a request and result from NHL API.
    API fully documented here: https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

    ...

    Attributes
    ----------
    _url_stub : ClassVar[str]
        partial URL location of data source
    _extension : ClassVar[str]
        file extension to be used when writing the raw data source to disk e.g. json, HTM
    _db_engine : Engine
        SQLAlchemy database engine object for caching data fetch results
    _pyd_model : DataModel
        pydantic model class describing the response
    _url : str
        fully qualified URL location of data source, completed on instantiation
    _query : dict
        dict representation of API query
    _content : str
        string representation of raw data retrieved by fetch_content()
    _content_pyd : DataModel
        pydantic model representation of the requested data created on call to parse_to_pyd()

    """

    _url_stub: ClassVar[str] = "https://statsapi.web.nhl.com/api/v1"
    _extension: ClassVar[str] = "json"
    _content_pyd: DataModel = None
    _pyd_model: DataModel
    _db_engine: Engine
    _url: str
    _query: dict
    _content: str

    @property
    def query(self) -> dict | None:
        return getattr(self, "_query", None)

    @query.setter
    def query(self, value: dict) -> None:
        self._query = value

    @property
    def pyd_model(self) -> DataModel:
        return self._pyd_model

    @property
    def content_pyd(self) -> DataModel:
        return self._content_pyd

    def parse_to_pyd(self) -> Self:
        """
        Parse content into a Pydantic model and store result in self.content_pyd
        """
        self._content_pyd = self.pyd_model.parse_raw(self.content)
        return self

    def cache_content(self) -> Self:
        """
        If a SQLAlchemy database engine is present, store the fetched content for later re-use
        """
        cache_record = CachedDataSource(
            url=self.url, query=str(self.query), content=self.content
        )
        with Session(self.db_engine) as session:
            session.add(cache_record)
            session.commit()
        return self

    def retrieve_cached_content(self) -> Self:
        """
        If a SQLAlchemy database engine is present, attempt to retrieve the cached content and store it in self.content
        instead of querying the API
        """
        with Session(self.db_engine) as session:
            select_statement: Select = select(CachedDataSource).where(
                CachedDataSource.url == self.url,
                CachedDataSource.query == str(self.query),
            )
            result: CachedDataSource = session.scalars(select_statement).first()
        if result:
            self.content = result.content
        return self

    def fetch_content(self) -> Self:
        """
        If SQLAlchemy engine is present, attempt to retrieve a cached version of the content.
        Otherwise, query NHL API endpoint at self.url and store response in self.content
        """
        if self.db_engine:
            self.retrieve_cached_content()
            if self.content:
                return self
        try:
            response = requests.get(self.url, self.query)
            response.raise_for_status()
            self.content = response.text
            if self.db_engine:
                self.cache_content()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return self


class NhlScheduleApiSource(NhlApiSource):
    """
    Subclass of NhlGameApiSource that represents a request from the NHL schedule API
    If no attributes are specified, the API will return today's games

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response
    _db_engine : Engine
        SQLAlchemy database engine object for caching data fetch results
    _date : str
        single date for the season_query (e.g. 2021-03-17)
    _start_date : str
        start date for a date range season_query
    _end_date : str
        end date for  date range season_query
    _season : str
        8 character representation of an NHL season (e.g. 20202021)
    _team_id : str
        one or more 2 character ID numbers representing NHL teams separated by commas
        or one or more tricodes representing NHL teams separated by commas
        e.g. '1,2,3' or 'NJD,NYI,NYR'
    _game_type : str
        one or more character codes for different game types separated by commas
        (e.g. PR for preseason, R for regular, A for all-star, P for playoffs)
        all options listed here: https://statsapi.web.nhl.com/api/v1/gameTypes
    _expand : str
        descriptor that provides additional information with the response
        'broadcasts' shows broadcast information, 'linescore' shows the line score,
        'tickets' shows ticketing information
        all options listed here: https://statsapi.web.nhl.com/api/v1/expands

    """

    _pyd_model: DataModel = nhl_schedule_api_source.Schedule
    _db_engine: Engine
    _date: str
    _start_date: str
    _end_date: str
    _season: str
    _team_id: str
    _game_type: str
    _expand: str

    def __init__(
        self,
        date=None,
        start_date=None,
        end_date=None,
        season=None,
        team_id=None,
        game_type=None,
        expand=None,
        db_engine=None,
    ):
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.season = season
        self.team_id = team_id
        self.game_type = game_type
        self.expand = expand
        self.db_engine = db_engine
        self.url = f"{self.url_stub}/schedule"
        query = {}
        if date:
            query["date"] = self.date
        if start_date:
            query["startDate"] = self.start_date
        if end_date:
            query["endDate"] = self.end_date
        if season:
            query["season"] = self.season
        if team_id:
            query["teamId"] = self.team_id
        if game_type:
            query["gameType"] = self.game_type
        if expand:
            query["expand"] = self.expand
        self.query = query

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._date = value.strftime("%Y-%m-%d")
        else:
            self._date = value

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._start_date = value.strftime("%Y-%m-%d")
        else:
            self._start_date = value

    @property
    def end_date(self) -> str:
        return self._end_date

    @end_date.setter
    def end_date(self, value: str | datetime) -> None:
        if isinstance(value, datetime):
            self._end_date = value.strftime("%Y-%m-%d")
        else:
            self._end_date = value

    @property
    def season(self) -> str:
        return self._season

    @season.setter
    def season(self, value: int | str) -> None:
        if len(str(value)) == 4:
            value = str(value) + str(int(value) + 1)
        self._season = str(value)

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, value: int | str) -> None:
        """
        Set value of team_id by coercing the user input into the acceptable form of one or more team ID numbers
        Parameters
        ----------
        value : int | str
            an int representing one team ID, or a str representing multiple.
            str can be a comma delimited list of team ID numbers or tricodes.
        """
        num_pattern = re.compile(r"^(\d|\d\d)$|^(\d,|\d\d,)+(\d|\d\d)$")
        tri_pattern = re.compile(r"^[a-zA-Z]{3}$|^([a-zA-Z]{3},)+[a-zA-Z]{3}$")

        if isinstance(value, int) or num_pattern.match(str(value)):
            self._team_id = str(value)
        elif isinstance(value, str) and tri_pattern.match(value):
            tricode_list: list[str] = value.split(",")
            team_dict: dict[str, int] = NhlTeamsApiSource().create_team_dict()
            id_list: list[str] = []
            for team in tricode_list:
                team_id: int = team_dict.get(team)
                if team_id is not None:
                    id_list.append(str(team_id))
            self._team_id = ",".join(id_list)
        else:
            self._team_id = ""

    @property
    def game_type(self) -> str:
        return self._game_type

    @game_type.setter
    def game_type(self, value: str) -> None:
        self._game_type = value

    @property
    def expand(self) -> str:
        return self._expand

    @expand.setter
    def expand(self, value: str) -> None:
        self._expand = value

    def yield_schedule_df(self) -> pd.DataFrame:
        """
            Return a pandas DataFrame representation of the schedule response

        Returns
        -------
            schedule_df (DataFrame): schedule dataframe
        """
        if self.content_pyd is None:
            self.fetch_content().parse_to_pyd()
        schedule_pyd = self.content_pyd.dates
        schedule_df = pd.DataFrame(
            {
                col: pd.Series(dtype=typ)
                for col, typ in nhl_schedule_api_source.schedule_df_model.items()
            }
        )
        for date in schedule_pyd:
            date_str = date.date
            for game in date.games:
                game_dict = {
                    "date": str(date_str),
                    "season": int(game.season),
                    "gamePk": int(game.gamePk),
                    "game_type": str(game.game_type),
                    "game_date": str(game.game_date),
                    "abstract_game_state": str(game.status.abstract_game_state),
                    "coded_game_state": str(game.status.coded_game_state),
                    "detailed_state": str(game.status.detailed_state),
                    "status_code": str(game.status.status_code),
                    "start_time_tbd": game.status.start_time_tbd,
                    "away_team_id": int(game.teams.away.team.id),
                    "away_team_name": str(game.teams.away.team.name),
                    "away_record_wins": int(game.teams.away.league_record.wins),
                    "away_record_losses": int(game.teams.away.league_record.losses),
                    "away_record_ot": (
                        int(game.teams.away.league_record.ot)
                        if game.teams.away.league_record.ot is not None
                        else None
                    ),
                    "away_record_type": str(game.teams.away.league_record.type),
                    "away_score": int(game.teams.away.score),
                    "home_team_id": int(game.teams.home.team.id),
                    "home_team_name": str(game.teams.home.team.name),
                    "home_record_wins": int(game.teams.home.league_record.wins),
                    "home_record_losses": int(game.teams.home.league_record.losses),
                    "home_record_ot": (
                        int(game.teams.home.league_record.ot)
                        if game.teams.home.league_record.ot is not None
                        else None
                    ),
                    "home_record_type": str(game.teams.home.league_record.type),
                    "home_score": int(game.teams.home.score),
                    "venue_id": (
                        int(game.venue.id) if game.venue.id is not None else None
                    ),
                    "venue_name": str(game.venue.name),
                }
                schedule_df.loc[game_dict["gamePk"]] = game_dict
        return schedule_df


class NhlTeamsApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL teams API

    ...

    Attributes
    ----------
    _team_id : int
        team id number for the NHL API query
    """

    _pyd_model: DataModel = nhl_teams_api_source.Teams
    _db_engine: Engine
    _team_id: str

    def __init__(self, team_id="", db_engine=None) -> None:
        self.team_id = team_id
        self.db_engine = db_engine
        self.url = f"{self.url_stub}" "/teams/" f"{self.team_id}"

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, value: str | int) -> None:
        self._team_id = str(value)

    @staticmethod
    def create_team_dict() -> dict[str, int]:
        """
        Request the full list of NHL teams and return a dictionary associating tricodes
        to team ID numbers.

        For now, use hardcoded version

        Returns
        -------
        team_dict (dict[str:int]) : dictionary associating tricodes to team ID numbers
        """
        from dry_scraper.teams import TEAMS

        team_dict = {}

        for team in TEAMS:
            tricode = TEAMS[team]["abbreviation"]
            id_number = TEAMS[team]["id"]
            team_dict[tricode] = id_number

        return team_dict


class NhlDivisionApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL divisions API

    ...

    Attributes
    ----------
    _division_id : int
        division id number for the NHL API query
    """

    _pyd_model: DataModel = nhl_divisions_api_source.Divisions
    _division_id: str

    def __init__(self, division_id="", db_engine=None) -> None:
        self.division_id = division_id
        self.url = f"{self.url_stub}" "/divisions/" f"{self.division_id}"
        self.db_engine = db_engine

    @property
    def division_id(self) -> str:
        return self._division_id

    @division_id.setter
    def division_id(self, value: str | int) -> None:
        self._division_id = str(value)


class NhlConferenceApiSource(NhlApiSource):
    """
    Subclass of NhlApiSource that represents a request to the NHL conferences API

    ...

    Attributes
    ----------
    _conference_id : int
        conference id number for the NHL API query
    """

    _pyd_model: DataModel = nhl_conferences_api_source.Conferences
    _conference_id: str

    def __init__(self, conference_id="", db_engine=None):  # -> Self:
        self.conference_id = conference_id
        self.url = f"{self.url_stub}" "/conferences/" f"{self.conference_id}"
        self.db_engine = db_engine

    @property
    def conference_id(self) -> str:
        return self._conference_id

    @conference_id.setter
    def conference_id(self, value: str | int) -> None:
        self._conference_id = str(value)


class NhlGameApiSource(NhlApiSource, ABC):
    """
    Abstract subclass of NhlApiSource that represents a request from an NHL Game API

    ...

    Attributes
    ----------
    _season : str
        8 character representation of an NHL season (e.g. 20202021)
    _gamePk : str
        6 character representation of NHL game in a season (e.g. 020462)
    """

    _season: str
    _gamePk: str

    def __init__(
        self, season: str | int, gamePk: str | int, db_engine: Engine | None = None
    ) -> None:
        self.season = season
        self.gamePk = gamePk
        self.db_engine = db_engine

    @property
    def season(self) -> str:
        return self._season

    @season.setter
    def season(self, value: int | str) -> None:
        self._season = str(value)

    @property
    def gamePk(self) -> str:
        return self._gamePk

    @gamePk.setter
    def gamePk(self, value: int | str) -> None:
        self._gamePk = str(value)


class NhlGameBoxScoreApiSource(NhlGameApiSource):
    """
    Subclass of NhlGameApiSource that represents a request from the NHL box score API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response
    """

    _pyd_model: DataModel = nhl_game_live_feed_api_source.BoxScore

    def __init__(
        self, season: str | int, gamePk: str | int, db_engine: Engine | None = None
    ) -> None:
        super().__init__(season, gamePk, db_engine)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/boxscore"
        )


class NhlGameLineScoreApiSource(NhlGameApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL line score API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response
    """

    _pyd_model: DataModel = nhl_game_live_feed_api_source.LineScore

    def __init__(
        self, season: str | int, gamePk: str | int, db_engine: Engine | None = None
    ) -> None:
        super().__init__(season, gamePk, db_engine)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/linescore"
        )


def determine_team_decision(team_goal_differential: int, ordinal: str) -> str:
    """
    Determine the decision of the game from the perspective of one team
    e.g., RW, OTL, SOW, etc.

    Parameters
    ----------
    team_goal_differential : int
        goal differential from the perspective of one team
    ordinal : str
        ordinal str describing the most recent period played
        e.g., 3rd, OT, SO

    Returns
    -------
    decision : str
        string describing decision of game from the perspective of one team
        e.g., RW, OTL, SOW, etc.
    """
    if team_goal_differential == 0:
        return "T"
    decision = "R" if ordinal == "3rd" else ordinal
    return decision + "W" if team_goal_differential > 0 else decision + "L"


class NhlGameLiveFeedApiSource(NhlGameApiSource):
    """
    Subclass of NhlApiSource that represents a request from the NHL live feed API

    ...

    Attributes
    ----------
    _pyd_model : DataModel
        pydantic model class describing the response
    """

    _pyd_model: DataModel = nhl_game_live_feed_api_source.LiveFeed

    def __init__(
        self, season: str | int, gamePk: str | int, db_engine: Engine | None = None
    ) -> None:
        super().__init__(season, gamePk, db_engine)
        self.url = (
            f"{self.url_stub}"
            "/game/"
            f"{self.season[:4]}"
            "0"
            f"{self.gamePk}"
            "/feed/live"
        )

    def yield_teams_and_date(self) -> (str, str, str):
        """
            Return home and away tricodes and date string of game from self.content

        Returns:
            home (str): home team tricode
            away (str): away team tricode
            date (str): date string
        """
        game_data = json.loads(self.content)["gameData"]
        try:
            home = game_data["teams"]["home"]["triCode"]
            away = game_data["teams"]["away"]["triCode"]
            date = game_data["datetime"]["dateTime"]
        except KeyError:
            home, away, date = None, None, None
        return home, away, date

    def yield_pbp_df(self) -> pd.DataFrame:
        """
            Return a pandas DataFrame representation of the game play-by-play

        Returns
        -------
            pbp_df (DataFrame): play-by-play dataframe
        """
        if self.content_pyd is None:
            self.fetch_content()
        pbp_pyd = self.content_pyd.live_data.plays.all_plays
        teams = self.content_pyd.game_data.teams
        home_team_id = teams.home.id
        home_team_name = teams.home.name
        home_team_tricode = teams.home.tricode
        away_team_id = teams.away.id
        away_team_name = teams.away.name
        away_team_tricode = teams.away.tricode
        pbp_df = pd.DataFrame(
            {
                col: pd.Series(dtype=typ)
                for col, typ in nhl_game_live_feed_api_source.pbp_df_model.items()
            }
        )
        for play in pbp_pyd:
            play_dict = {
                "season": int(self.season),
                "gamePk": int(self.gamePk),
                "home_team_id": int(home_team_id),
                "home_team_name": str(home_team_name),
                "home_team_tricode": str(home_team_tricode),
                "away_team_id": int(away_team_id),
                "away_team_name": str(away_team_name),
                "away_team_tricode": str(away_team_tricode),
                "event": str(play.result.event),
                "event_code": str(play.result.event_code),
                "event_type_id": str(play.result.event_type_id),
                "description": str(play.result.description),
                "secondary_type": str(play.result.secondary_type),
                "game_winning_goal": str(play.result.game_winning_goal),
                "empty_net": str(play.result.empty_net),
                "event_idx": int(play.about.event_idx),
                "event_id": int(play.about.event_id),
                "period": int(play.about.period),
                "period_type": str(play.about.period_type),
                "ordinal_num": str(play.about.ordinal_num),
                "period_time": str(play.about.period_time),
                "period_time_remaining": str(play.about.period_time_remaining),
                "date_time": str(play.about.date_time),
                "goals_home": int(play.about.goals.home),
                "goals_away": int(play.about.goals.away),
                "coordinates_x": (
                    int(play.coordinates.x) if play.coordinates.x is not None else None
                ),
                "coordinates_y": (
                    int(play.coordinates.y) if play.coordinates.y is not None else None
                ),
                "strength_code": (
                    str(play.result.strength.code)
                    if play.result.strength is not None
                    else None
                ),
                "strength_name": (
                    str(play.result.strength.name)
                    if play.result.strength is not None
                    else None
                ),
                "player0_id": (
                    int(play.players[0].player.id) if play.players is not None else None
                ),
                "player0_full_name": (
                    str(play.players[0].player.full_name)
                    if play.players is not None
                    else None
                ),
                "player0_player_type": (
                    str(play.players[0].player_type)
                    if play.players is not None
                    else None
                ),
                "player0_season_total": (
                    int(play.players[0].season_total)
                    if play.players is not None
                    and play.players[0].season_total is not None
                    else None
                ),
                "player1_id": (
                    int(play.players[1].player.id)
                    if play.players is not None and len(play.players) > 1
                    else None
                ),
                "player1_full_name": (
                    str(play.players[1].player.full_name)
                    if play.players is not None and len(play.players) > 1
                    else None
                ),
                "player1_player_type": (
                    str(play.players[1].player_type)
                    if play.players is not None and len(play.players) > 1
                    else None
                ),
                "player1_season_total": (
                    int(play.players[1].season_total)
                    if play.players is not None
                    and len(play.players) > 1
                    and play.players[1].season_total is not None
                    else None
                ),
                "player2_id": (
                    int(play.players[2].player.id)
                    if play.players is not None and len(play.players) > 2
                    else None
                ),
                "player2_full_name": (
                    str(play.players[2].player.full_name)
                    if play.players is not None and len(play.players) > 2
                    else None
                ),
                "player2_player_type": (
                    str(play.players[2].player_type)
                    if play.players is not None and len(play.players) > 2
                    else None
                ),
                "player2_season_total": (
                    int(play.players[2].season_total)
                    if play.players is not None
                    and len(play.players) > 2
                    and play.players[2].season_total is not None
                    else None
                ),
                "player3_id": (
                    int(play.players[3].player.id)
                    if play.players is not None and len(play.players) > 3
                    else None
                ),
                "player3_full_name": (
                    str(play.players[3].player.full_name)
                    if play.players is not None and len(play.players) > 3
                    else None
                ),
                "player3_player_type": (
                    str(play.players[3].player_type)
                    if play.players is not None and len(play.players) > 3
                    else None
                ),
                "player3_season_total": (
                    int(play.players[3].season_total)
                    if play.players is not None
                    and len(play.players) > 3
                    and play.players[3].season_total is not None
                    else None
                ),
                "team_id": int(play.team.id) if play.team is not None else None,
                "team_name": (str(play.team.name) if play.team is not None else None),
                "team_tricode": (
                    str(play.team.tricode) if play.team is not None else None
                ),
            }
            pbp_df.loc[play_dict["event_idx"]] = play_dict
        return pbp_df

    def yield_team_stats_df(self) -> pd.DataFrame:
        """
            Return a pandas DataFrame representation of the teamStats section of the BoxScore response

        Returns
        -------
            team_stats_df (DataFrame): teamStats dataframe
        """
        if self.content_pyd is None:
            self.fetch_content().parse_to_pyd()
        home_stats = (
            self.content_pyd.live_data.box_score.teams.home.team_stats.team_skater_stats
        )
        home_team_info = self.content_pyd.game_data.teams.home
        away_stats = (
            self.content_pyd.live_data.box_score.teams.away.team_stats.team_skater_stats
        )
        away_team_info = self.content_pyd.game_data.teams.away
        team_stats_df = pd.DataFrame(
            {
                col: pd.Series(dtype=typ)
                for col, typ in nhl_game_live_feed_api_source.team_stats_df_model.items()
            }
        )
        home_line_score_goal_differential = (
            self.content_pyd.live_data.line_score.teams.home.goals
            - self.content_pyd.live_data.line_score.teams.away.goals
        )
        start = self.content_pyd.game_data.date_time.date_time
        end = self.content_pyd.game_data.date_time.end_date_time
        venue = self.content_pyd.game_data.venue
        for home, team_stats, oppo_stats, team_info, oppo_info in [
            (True, home_stats, away_stats, home_team_info, away_team_info),
            (False, away_stats, home_stats, away_team_info, home_team_info),
        ]:
            team_stats_dict = {
                "season": int(self.season),
                "game_pk": int(self.gamePk),
                "game_type": self.content_pyd.game_data.game.type,
                "start_date_time": datetime.min if start is None else start,
                "end_date_time": datetime.min if end is None else end,
                "team_id": int(team_info.id),
                "team_franchise_id": int(team_info.franchise_id),
                "team_name": str(team_info.name),
                "team_tricode": str(team_info.tricode),
                "oppo_id": int(oppo_info.id),
                "oppo_franchise_id": int(oppo_info.franchise_id),
                "oppo_name": str(oppo_info.name),
                "oppo_tricode": str(oppo_info.tricode),
                "team_home": home,
                "team_goals": int(team_stats.goals),
                "team_penalty_minutes": int(team_stats.pim),
                "team_shots_on_goal": not_none(team_stats.shots, int),
                "team_power_play_points": not_none(
                    team_stats.power_play_percentage, float
                ),
                "team_power_play_goals": not_none(team_stats.power_play_goals, int),
                "team_power_play_opportunities": not_none(
                    team_stats.power_play_opportunities, int
                ),
                "team_face_off_win_percentage": not_none(
                    team_stats.power_play_percentage, float
                ),
                "team_blocked_shots": not_none(team_stats.blocked, int),
                "team_takeaways": not_none(team_stats.takeaways, int),
                "team_giveaways": not_none(team_stats.giveaways, int),
                "team_hits": not_none(team_stats.hits, int),
                "oppo_goals": not_none(oppo_stats.goals, int),
                "oppo_penalty_minutes": not_none(oppo_stats.pim, int),
                "oppo_shots_on_goal": not_none(oppo_stats.shots, int),
                "oppo_power_play_percentage": not_none(
                    oppo_stats.power_play_percentage, float
                ),
                "oppo_power_play_goals": not_none(oppo_stats.power_play_goals, int),
                "oppo_power_play_opportunities": not_none(
                    oppo_stats.power_play_opportunities, int
                ),
                "oppo_face_off_win_percentage": not_none(
                    oppo_stats.face_off_win_percentage, float
                ),
                "oppo_blocked_shots": not_none(oppo_stats.blocked, int),
                "oppo_takeaways": not_none(oppo_stats.takeaways, int),
                "oppo_giveaways": not_none(oppo_stats.giveaways, int),
                "oppo_hits": not_none(oppo_stats.hits, int),
                "team_goal_differential": int(team_stats.goals) - int(oppo_stats.goals),
                "team_decision": determine_team_decision(
                    home_line_score_goal_differential
                    if home
                    else -home_line_score_goal_differential,
                    self.content_pyd.live_data.line_score.current_period_ordinal,
                ),
                "venue_id": None if venue is None else not_none(venue.id, int),
                "venue_name": None if venue is None else not_none(venue.name, str),
            }
            team_stats_df.loc[
                f"{self.gamePk} Home" if home else f"{self.gamePk} Away"
            ] = team_stats_dict
        return team_stats_df


def not_none(value: Any, type_function: type) -> Any:
    return type_function(value) if value is not None else None
