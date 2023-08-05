from datetime import datetime
from typing import List, Dict, Optional, Annotated, Literal
from uuid import UUID
from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import constr, Field, HttpUrl

GameContentLink = constr(regex=r"^/api/v1/game/\d{10}/content$")
ResolutionString = constr(regex=r"^\d{2,4}x\d{2,4}$")


class Empty(BaseModelNoException):
    ...

    class Config:
        extra = "forbid"


class ContributorEntry(BaseModelNoException):
    name: Optional[str]
    twitter: Optional[str]


class Contributor(BaseModelNoException):
    contributors: Optional[List[ContributorEntry]]
    source: Optional[str]


class ImageCut(BaseModelNoException):
    aspect_ratio: Optional[str] = Field(alias="aspectRatio")
    width: Optional[int]
    height: Optional[int]
    src: Optional[HttpUrl]
    at2x: Optional[HttpUrl]
    at3x: Optional[HttpUrl]


class Image(BaseModelNoException):
    title: Optional[str]
    alt_text: Optional[str] = Field(alias="altText")
    cuts: Optional[Dict[ResolutionString, ImageCut]]


class Playback(BaseModelNoException):
    name: Optional[str]
    width: Optional[int | str]
    height: Optional[int | str]
    url: Optional[HttpUrl | str]


class Keyword(BaseModelNoException):
    type: Optional[str]
    value: Optional[str]
    display_name: Optional[str] = Field(alias="displayName")


class PhotoMediaItem(BaseModelNoException):
    type: Optional[str]
    image: Optional[Image]


class MediaItem(BaseModelNoException):
    type: Optional[str]
    id: Optional[int]
    date: Optional[datetime]
    title: Optional[str]
    blurb: Optional[str]
    description: Optional[str]
    duration: Optional[str]
    auth_flow: Optional[bool] = Field(alias="authFlow")
    media_playback_id: Optional[int] = Field(alias="mediaPlaybackId")
    media_state: Optional[str] = Field(alias="mediaState")
    keywords: Optional[List[Keyword]]
    image: Optional[Image]
    playbacks: Optional[List[Playback]]


class EditorialItem(BaseModelNoException):
    type: Optional[str]
    state: Optional[str]
    date: Optional[datetime]
    id: Optional[str]
    headline: Optional[str]
    subhead: Optional[str]
    seo_title: Optional[str] = Field(alias="seoTitle")
    seo_description: Optional[str] = Field(alias="seoDescription")
    seo_keywords: Optional[str] = Field(alias="seoKeywords")
    slug: Optional[str]
    commenting: Optional[bool]
    tagline: Optional[str]
    contributor: Optional[Contributor]
    keywords_display: Optional[List[Keyword]] = Field(alias="keywordsDisplay")
    keywords_all: Optional[List[Keyword]] = Field(alias="keywordsAll")
    approval: Optional[str]
    url: Optional[str]
    data_URI: Optional[str] = Field(alias="dataURI")
    media: Optional[MediaItem | PhotoMediaItem | Empty]
    preview: Optional[str]


class NhlTvItem(BaseModelNoException):
    guid: Optional[UUID]
    media_state: Optional[str] = Field(alias="mediaState")
    media_playback_id: Optional[int] = Field(alias="mediaPlaybackId")
    media_feed_type: Optional[str] = Field(alias="mediaFeedType")
    call_letters: Optional[str] = Field(alias="callLetters")
    event_id: Optional[str] = Field(alias="eventId")
    language: Optional[str]
    free_game: Optional[bool] = Field(alias="freeGame")
    feed_name: Optional[str] = Field(alias="feedName")
    game_plus: Optional[bool] = Field(alias="gamePlus")


class AudioItem(BaseModelNoException):
    media_state: Optional[str] = Field(alias="mediaState")
    media_playback_id: Optional[int] = Field(alias="mediaPlaybackId")
    media_feed_type: Optional[str] = Field(alias="mediaFeedType")
    call_letters: Optional[str] = Field(alias="callLetters")
    event_id: Optional[str] = Field(alias="eventId")
    language: Optional[str]
    free_game: Optional[bool] = Field(alias="freeGame")
    feed_name: Optional[str] = Field(alias="feedName")
    game_plus: Optional[bool] = Field(alias="gamePlus")


class EditorialCategory(BaseModelNoException):
    title: Optional[str]
    topic_list: Optional[str] = Field(alias="topicList")
    items: Optional[List[EditorialItem]]


class NhlTvEntry(BaseModelNoException):
    title: Optional[Literal["NHLTV"]]
    platform: Optional[str]
    items: Optional[List[NhlTvItem]]


class AudioEpgEntry(BaseModelNoException):
    title: Optional[Literal["Audio"]]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: Optional[List[AudioItem]]


class ExtendedHighlightsEpgEntry(BaseModelNoException):
    title: Optional[Literal["Extended Highlights"]]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: Optional[List[MediaItem]]


class RecapEpgEntry(BaseModelNoException):
    title: Optional[Literal["Recap"]]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: Optional[List[MediaItem]]


class PowerPlayEpgEntry(BaseModelNoException):
    title: Optional[Literal["Power Play"]]
    topic_list: Optional[int | str] = Field(alias="topicList")
    items: Optional[List[MediaItem]]


EpgEntry = Annotated[
    NhlTvEntry
    | AudioEpgEntry
    | ExtendedHighlightsEpgEntry
    | RecapEpgEntry
    | PowerPlayEpgEntry,
    Field(discriminator="title"),
]


class Editorial(BaseModelNoException):
    preview: Optional[EditorialCategory]
    articles: Optional[EditorialCategory]
    recap: Optional[EditorialCategory]


class Milestone(BaseModelNoException):
    title: Optional[str]
    description: Optional[str]
    type: Optional[str]
    type: Optional[str]
    time_absolute: Optional[datetime] = Field(alias="timeAbsolute")
    time_offset: Optional[datetime] = Field(alias="timeOffset")
    period: Optional[int | str]
    stats_event_id: Optional[int | str] = Field(alias="statsEventId")
    team_id: Optional[int | str] = Field(alias="teamId")
    player_id: Optional[int | str] = Field(alias="playerId")
    period_time: Optional[str] = Field(alias="periodTime")
    ordinal_num: Optional[str] = Field(alias="ordinalNum")
    highlight: Optional[MediaItem | Empty]


class Milestones(BaseModelNoException):
    title: Optional[Literal["Milestones"]]
    steam_start: Optional[datetime] = Field(alias="streamStart")
    items: Optional[List[Milestone]]


class Media(BaseModelNoException):
    epg: Optional[List[EpgEntry]]
    milestones: Optional[Milestones | Empty]


class HighlightEntries(BaseModelNoException):
    title: Optional[str]
    topic_list: Optional[str] = Field(alias="topicList")
    items: Optional[List[MediaItem]]


class Highlights(BaseModelNoException):
    scoreboard: Optional[HighlightEntries]
    gamecenter: Optional[HighlightEntries] = Field(alias="gameCenter")


class GameContent(BaseModelNoException):
    link: Optional[GameContentLink]
    editorial: Optional[Editorial]
    media: Optional[Media]
    highlights: Optional[Highlights]
