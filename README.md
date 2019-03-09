# Voting Scraper

Scraper for extracting data from the [U.S. Election Assistance Commission](https://www.eac.gov/research-and-data/datasets-codebooks-and-surveys/).

### Installing Dependencies

```sh
pip install -r requirements.txt
```

### Extracting data

For every election from 2008 onwards, this tool will extract the following data into one CSV by year:

- Year
- State
- 2 letter state abbreviation
- Jurisdiction (usually county)
- Active registrations
- Number of precints
- Number of polling places
- Number of poll workers (grouped by age, if data is available)
- Difficulty of finding poll workers
- Number of election participants

This project uses `.env` to load file paths to the source data. In order for the project to work, create a `.env` file and include a line like this for each year:

```sh
DATA_PATH_2016=PATH_TO_SOURCE_DATA_ON_YOUR_COMPUTER
```