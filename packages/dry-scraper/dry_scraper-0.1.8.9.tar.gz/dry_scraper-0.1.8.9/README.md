# dry_scraper

`dry_scraper` is a framework for retrieving and parsing hockey data into useful forms.

In its current form, it supports only NHL data sources, but its object-oriented structure is intended to enable
extensibility to other leagues with comparable data sources.

It's simple to get started. Here's how you can retrieve a pandas dataframe of the team stats for a given game:

```
   from dry_scraper.nhl.nhl_api_sources import NhlGameLiveFeedApiSource
   team_stats = NhlGameLiveFeedApiSource(season=2022, gamePk=20720)
                  .fetch_content()
                  .parse_to_pyd()
                  .yield_team_stats_df()
```