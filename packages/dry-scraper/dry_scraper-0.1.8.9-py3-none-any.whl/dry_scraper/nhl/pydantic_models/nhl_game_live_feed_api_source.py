from datetime import datetime
from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import Field, constr
from typing import List, Dict, Optional, Union


from dry_scraper.nhl.pydantic_models.nhl_people_api_source import (
    PersonIdString,
    PersonLink,
    Position,
    Player,
    Person,
)
from dry_scraper.nhl.pydantic_models.nhl_teams_api_source import (
    Team,
    ShortTeam,
    ShortVenue,
)

LiveFeedLink = constr(regex=r"^/api/v1/game/\d{10}/feed/live$")


class Metadata(BaseModelNoException):
    wait: Optional[int]
    timestamp: Optional[str] = Field(alias="timeStamp")


class Game(BaseModelNoException):
    pk: Optional[int]
    season: Optional[str]
    type: Optional[str]


class GameDateTime(BaseModelNoException):
    date_time: Optional[datetime] = Field(alias="dateTime")
    end_date_time: Optional[Optional[datetime]] = Field(alias="endDateTime")


class Status(BaseModelNoException):
    abstract_game_state: Optional[str] = Field(alias="abstractGameState")
    coded_game_state: Optional[str] = Field(alias="codedGameState")
    detailed_state: Optional[str] = Field(alias="detailedState")
    status_code: Optional[str] = Field(alias="statusCode")
    start_time_tbd: Optional[bool] = Field(alias="startTimeTBD")


class Teams(BaseModelNoException):
    away: Optional[Team]
    home: Optional[Team]


class GameData(BaseModelNoException):
    game: Optional[Game]
    date_time: Optional[GameDateTime] = Field(alias="datetime")
    status: Optional[Status]
    teams: Optional[Teams]
    players: Optional[Dict[PersonIdString, Player]]
    venue: Optional[ShortVenue]


class PlaysByPeriod(BaseModelNoException):
    start_index: Optional[int] = Field(alias="startIndex")
    plays: Optional[List[int]]
    end_index: Optional[int] = Field(alias="endIndex")


class Strength(BaseModelNoException):
    code: Optional[str]
    name: Optional[str]


class Result(BaseModelNoException):
    event: Optional[str]
    event_code: Optional[str] = Field(alias="eventCode")
    event_type_id: Optional[str] = Field(alias="eventTypeId")
    description: Optional[str]
    secondary_type: Optional[str] = Field(alias="secondaryType")
    strength: Optional[Strength]
    game_winning_goal: Optional[bool] = Field(alias="gameWinningGoal")
    empty_net: Optional[bool] = Field(alias="emptyNet")


class Goals(BaseModelNoException):
    away: Optional[int]
    home: Optional[int]


class About(BaseModelNoException):
    event_idx: Optional[int] = Field(alias="eventIdx")
    event_id: Optional[int] = Field(alias="eventId")
    period: Optional[int]
    period_type: Optional[str] = Field(alias="periodType")
    ordinal_num: Optional[str] = Field(alias="ordinalNum")
    period_time: Optional[str] = Field(alias="periodTime")
    period_time_remaining: Optional[str] = Field(alias="periodTimeRemaining")
    date_time: Optional[datetime] = Field(alias="dateTime")
    goals: Optional[Goals]


class Coordinates(BaseModelNoException):
    x: Optional[int]
    y: Optional[int]


class PlayPlayer(BaseModelNoException):
    player: Optional[Person]
    player_type: Optional[str] = Field(alias="playerType")
    season_total: Optional[str] = Field(alias="seasonTotal")


class Play(BaseModelNoException):
    result: Optional[Result]
    about: Optional[About]
    coordinates: Optional[Coordinates]
    players: Optional[List[PlayPlayer]]
    team: Optional[ShortTeam]


class Plays(BaseModelNoException):
    all_plays: Optional[List[Play]] = Field(alias="allPlays")
    scoring_plays: Optional[List[int]] = Field(alias="scoringPlays")
    penalty_plays: Optional[List[int]] = Field(alias="penaltyPlays")
    plays_by_period: Optional[List[PlaysByPeriod]] = Field(alias="playsByPeriod")
    current_play: Optional[Play] = Field(alias="currentPlay")


class TeamPeriodLineScore(BaseModelNoException):
    goals: Optional[int]
    shots_on_goal: Optional[int] = Field(alias="shotsOnGoal")
    rink_side: Optional[str] = Field(alias="rinkSide")


class Period(BaseModelNoException):
    period_type: Optional[str] = Field(alias="periodType")
    start_time: Optional[datetime] = Field(alias="startTime")
    end_time: Optional[datetime] = Field(alias="endTime")
    num: Optional[int]
    ordinal_num: Optional[str] = Field(alias="ordinalNum")
    home: Optional[TeamPeriodLineScore]
    away: Optional[TeamPeriodLineScore]


class TeamShootoutInfo(BaseModelNoException):
    scores: Optional[int]
    attempts: Optional[int]


class ShootoutInfo(BaseModelNoException):
    away: Optional[TeamShootoutInfo]
    home: Optional[TeamShootoutInfo]
    start_time: Optional[datetime] = Field(alias="startTime")


class TeamLineScore(BaseModelNoException):
    team: Optional[ShortTeam]
    goals: Optional[int]
    shots_on_goal: Optional[int] = Field(alias="shotsOnGoal")
    goalie_pulled: Optional[bool] = Field(alias="goaliePulled")
    num_skaters: Optional[int] = Field(alias="numSkaters")
    power_play: Optional[bool] = Field(alias="powerPlay")


class TeamsLineScore(BaseModelNoException):
    away: Optional[TeamLineScore]
    home: Optional[TeamLineScore]


class IntermissionInfo(BaseModelNoException):
    intermission_time_remaining: Optional[int] = Field(
        alias="intermissionTimeRemaining"
    )
    intermission_time_elapsed: Optional[int] = Field(alias="intermissionTimeElapsed")
    in_intermission: Optional[bool] = Field(alias="inIntermission")


class PowerPlayInfo(BaseModelNoException):
    situation_time_remaining: Optional[int] = Field(alias="situationTimeRemaining")
    situation_time_elapsed: Optional[int] = Field(alias="situationTimeElapsed")
    in_situation: Optional[bool] = Field(alias="inSituation")


class LineScore(BaseModelNoException):
    current_period: Optional[str] = Field(alias="currentPeriod")
    current_period_ordinal: Optional[str] = Field(alias="currentPeriodOrdinal")
    current_period_time_remaining: Optional[str] = Field(
        alias="currentPeriodTimeRemaining"
    )
    periods: Optional[List[Period]]
    shootout_info: Optional[ShootoutInfo] = Field(alias="shootoutInfo")
    teams: Optional[TeamsLineScore]
    power_play_strength: Optional[str] = Field(alias="powerPlayStrength")
    has_shootout: Optional[bool] = Field(alias="hasShootout")
    intermission_info: Optional[IntermissionInfo] = Field(alias="intermissionInfo")
    power_play_info: Optional[PowerPlayInfo] = Field(alias="powerPlayInfo")


class Official(BaseModelNoException):
    official: Optional[Person]
    official_type: Optional[str] = Field(alias="officialType")


class TeamSkaterStats(BaseModelNoException):
    goals: Optional[int]
    pim: Optional[int]
    shots: Optional[int]
    power_play_percentage: Optional[float] = Field(alias="powerPlayPercentage")
    power_play_goals: Optional[int] = Field(alias="powerPlayGoals")
    power_play_opportunities: Optional[int] = Field(alias="powerPlayOpportunities")
    face_off_win_percentage: Optional[float] = Field(alias="faceOffWinPercentage")
    blocked: Optional[int]
    takeaways: Optional[int]
    giveaways: Optional[int]
    hits: Optional[int]


class TeamStats(BaseModelNoException):
    team_skater_stats: Optional[TeamSkaterStats] = Field(alias="teamSkaterStats")


class PlayerStatsPerson(BaseModelNoException):
    id: Optional[PersonIdString]
    full_name: Optional[str] = Field(alias="fullName")
    link: Optional[constr(regex=r"^/api/v1/people/\d+$")]
    shoots_catches: Optional[str] = Field(alias="shootsCatches")
    roster_status: Optional[str] = Field(alias="rosterStatus")


class GoalieStats(BaseModelNoException):
    time_on_ice: Optional[str] = Field(alias="timeOnIce")
    assists: Optional[int]
    goals: Optional[int]
    pim: Optional[int]
    shots: Optional[int]
    saves: Optional[int]
    power_play_saves: Optional[int] = Field(alias="powerPlaySaves")
    shorthanded_saves: Optional[int] = Field(alias="shortHandedSaves")
    even_saves: Optional[int] = Field(alias="evenSaves")
    shorthanded_shots_against: Optional[int] = Field(alias="shortHandedShotsAgainst")
    even_shots_against: Optional[int] = Field(alias="evenShotsAgainst")
    power_play_shots_against: Optional[int] = Field(alias="powerPlayShotsAgainst")
    decision: Optional[str]
    save_percentage: Optional[float] = Field(alias="savePercentage")
    power_play_save_percentage: Optional[float] = Field(alias="powerPlaySavePercentage")
    even_strength_save_percentage: Optional[float] = Field(
        alias="evenStrengthSavePercentage"
    )


class SkaterStats(BaseModelNoException):
    time_on_ice: Optional[str] = Field(alias="timeOnIce")
    assists: Optional[int]
    goals: Optional[int]
    shots: Optional[int]
    hits: Optional[int]
    power_play_goals: Optional[int] = Field(alias="powerPlayGoals")
    power_play_assists: Optional[int] = Field(alias="powerPlayAssists")
    penalty_minutes: Optional[int] = Field(alias="penaltyMinutes")
    face_off_wins: Optional[int] = Field(alias="faceOffWins")
    face_offs_taken: Optional[int] = Field(alias="faceoffTaken")
    takeaways: Optional[int]
    giveaways: Optional[int]
    shorthanded_goals: Optional[int] = Field(alias="shortHandedGoals")
    shorthanded_assists: Optional[int] = Field(alias="shortHandedAssists")
    blocked_shots: Optional[int] = Field(alias="blocked")
    plus_minus: Optional[int] = Field(alias="plusMinus")
    even_time_on_ice: Optional[str] = Field(alias="evenTimeOnIce")
    power_play_time_on_ice: Optional[str] = Field(alias="powerPlayTimeOnIce")
    shorthanded_time_on_ice: Optional[str] = Field(alias="shortHandedTimeOnIce")


class PlayerStats(BaseModelNoException):
    skater_stats: Optional[SkaterStats] = Field(alias="skaterStats")
    goalie_stats: Optional[GoalieStats] = Field(alias="goalieStats")


class PlayerStatsEntry(BaseModelNoException):
    person: Optional[PlayerStatsPerson]
    jersey_number: Optional[int] = Field(alias="jerseyNumber")
    position: Optional[Position]
    stats: Optional[Union[PlayerStats, None, Dict]]


class ShortPerson(BaseModelNoException):
    full_name: Optional[str] = Field(alias="fullName")
    link: Optional[PersonLink]


class Coach(BaseModelNoException):
    person: Optional[Person]
    position: Optional[Position]


class OnIcePlusPlayer(BaseModelNoException):
    player_id: Optional[PersonIdString] = Field(alias="playerId")
    shift_duration: Optional[int] = Field(alias="shiftDuration")
    stamina: Optional[int]


class PenaltyBox(BaseModelNoException):
    id: Optional[PersonIdString]
    time_remaining: Optional[str] = Field(alias="timeRemaining")
    active: Optional[bool]


class TeamBoxScore(BaseModelNoException):
    team: Optional[ShortTeam]
    team_stats: Optional[TeamStats] = Field(alias="teamStats")
    players: Optional[Dict[PersonIdString, PlayerStatsEntry]]
    goalies: Optional[List[PersonIdString]]
    skaters: Optional[List[PersonIdString]]
    on_ice: Optional[List[PersonIdString]] = Field(alias="onIce")
    on_ice_plus: Optional[List[OnIcePlusPlayer]] = Field(alias="onIcePlus")
    scratches: Optional[List[PersonIdString]]
    penalty_box: Optional[List[PenaltyBox]] = Field(alias="penaltyBox")
    coaches: Optional[List[Coach]]


class TeamsBoxScore(BaseModelNoException):
    away: Optional[TeamBoxScore]
    home: Optional[TeamBoxScore]


class BoxScore(BaseModelNoException):
    teams: Optional[TeamsBoxScore]
    officials: Optional[List[Official]]


class Decisions(BaseModelNoException):
    winner: Optional[Person]
    loser: Optional[Person]
    first_star: Optional[Person] = Field(alias="firstStar")
    second_star: Optional[Person] = Field(alias="secondStar")
    third_star: Optional[Person] = Field(alias="thirdStar")


class LiveData(BaseModelNoException):
    plays: Optional[Plays]
    line_score: Optional[LineScore] = Field(alias="linescore")
    box_score: Optional[BoxScore] = Field(alias="boxscore")
    decisions: Optional[Decisions]


class LiveFeed(BaseModelNoException):
    game_pk: Optional[int] = Field(alias="gamePk")
    link: Optional[LiveFeedLink]
    metadata: Optional[Metadata] = Field(alias="metaData")
    game_data: Optional[GameData] = Field(alias="gameData")
    live_data: Optional[LiveData] = Field(alias="liveData")


pbp_df_model = {
    "season": "int",
    "gamePk": "int",
    "home_team_id": "int",
    "home_franchise_id": "int",
    "home_team_name": "str",
    "home_team_tricode": "str",
    "away_team_id": "int",
    "away_franchise_id": "int",
    "away_team_name": "str",
    "away_team_tricode": "str",
    "event_idx": "int",
    "event_id": "int",
    "event": "str",
    "event_code": "str",
    "event_type_id": "str",
    "description": "str",
    "secondary_type": "str",
    "game_winning_goal": "str",
    "empty_net": "str",
    "period": "int",
    "period_type": "str",
    "ordinal_num": "str",
    "period_time": "str",
    "period_time_remaining": "str",
    "date_time": "str",
    "goals_home": "int",
    "goals_away": "int",
    "coordinates_x": "int",
    "coordinates_y": "int",
    "strength_code": "str",
    "strength_name": "str",
    "player0_id": "int",
    "player0_full_name": "str",
    "player0_player_type": "str",
    "player0_season_total": "int",
    "player1_id": "int",
    "player1_full_name": "str",
    "player1_player_type": "str",
    "player1_season_total": "int",
    "player2_id": "int",
    "player2_full_name": "str",
    "player2_player_type": "str",
    "player2_season_total": "int",
    "player3_id": "int",
    "player3_full_name": "str",
    "player3_player_type": "str",
    "player3_season_total": "int",
    "team_id": "int",
    "team_name": "str",
    "team_tricode": "str",
}

team_stats_df_model = {
    "season": "int",
    "game_pk": "int",
    "game_type": "str",
    "game_date": "datetime64[D]",
    "start_date_time": "datetime64[s]",
    "end_date_time": "datetime64[s]",
    "venue_id": "int",
    "venue_name": "str",
    "team_id": "int",
    "team_franchise_id": "int",
    "team_name": "str",
    "team_tricode": "str",
    "oppo_id": "int",
    "oppo_franchise_id": "int",
    "oppo_name": "str",
    "oppo_tricode": "str",
    "team_home": "bool",
    "team_goals": "int",
    "team_shots_on_goal": "int",
    "team_penalty_minutes": "int",
    "team_power_play_percentage": "float",
    "team_power_play_goals": "int",
    "team_power_play_opportunities": "int",
    "team_face_off_win_percentage": "float",
    "team_blocked_shots": "int",
    "team_takeaways": "int",
    "team_giveaways": "int",
    "team_hits": "int",
    "oppo_goals": "int",
    "oppo_shots_on_goal": "int",
    "oppo_penalty_minutes": "int",
    "oppo_power_play_percentage": "float",
    "oppo_power_play_goals": "int",
    "oppo_power_play_opportunities": "int",
    "oppo_face_off_win_percentage": "float",
    "oppo_blocked_shots": "int",
    "oppo_takeaways": "int",
    "oppo_giveaways": "int",
    "oppo_hits": "int",
    "team_goal_differential": "int",
    "team_decision": "str",
}
