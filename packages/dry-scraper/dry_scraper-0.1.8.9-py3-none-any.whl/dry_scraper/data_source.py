import os

from sqlalchemy import Engine, Select, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import JSONB
import requests
from abc import ABC
from typing import ClassVar, Self


class DataSource(ABC):
    """
    Abstract class that represents an online data source.

    ...

    Attributes
    ----------
    _content : str
        string representation of raw data retrieved by fetch_content()
    _db_engine : Engine
        SQLAlchemy database engine object for caching data fetch results
    _url : str
        fully qualified URL location of data source, completed on instantiation
    _url_stub : ClassVar[str]
        partial URL location of data source
    _extension : ClassVar[str]
        file extension to be used when writing the raw data source to disk e.g. json, HTM

    """

    _content: str
    _db_engine: Engine
    _url: str
    _url_stub: ClassVar[str]
    _extension: ClassVar[str]

    @property
    def content(self) -> str | None:
        return getattr(self, "_content", None)

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

    @property
    def db_engine(self) -> Engine | None:
        return getattr(self, "_db_engine", None)

    @db_engine.setter
    def db_engine(self, value: Engine) -> None:
        self._db_engine = value

    @property
    def url(self) -> str | None:
        return getattr(self, "_url", None)

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def url_stub(self) -> str:
        return self._url_stub

    @property
    def extension(self) -> str:
        return self._extension

    def fetch_content(self) -> Self:
        """
        Use requests.get to retrieve file at self.url and store response in self.content
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.content = response.text
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return self

    def cache_content(self) -> Self:
        """
        If a SQLAlchemy database engine is present, store the fetched content for later re-use
        """
        cache_record = CachedDataSource(url=self.url, content=self.content)
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
                CachedDataSource.url == self.url
            )
            result: CachedDataSource = session.scalars(select_statement).first()
        if result:
            self.content = result.content
        return self

    def write_content(self, path: str, filename: str) -> Self:
        """Write content to {path}/{filename}.{self.extension}

        Args:
            filename (str): desired filename
            path (str): path to save location
        """
        full_path = os.path.join(path, f"{filename}.{self.extension}")
        try:
            with open(full_path, "w") as f:
                f.write(self.content)
        except OSError as e:
            print(f"Failed to write to {full_path}.")
            print(e)
        except Exception as e:
            print(e)
        return self


class Base(DeclarativeBase):
    pass


class CachedDataSource(Base):
    __tablename__ = "cached_data_source"

    url: Mapped[str] = mapped_column(Text, primary_key=True)
    query: Mapped[str] = mapped_column(Text, primary_key=True)
    content: Mapped[dict] = mapped_column(JSONB)
