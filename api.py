"""api.py - API access to vaalitulos.hyy.fi"""

import urllib.request
import json
# import csv

import pandas as pd
from io import StringIO

BASE_URL = "http://vaalitulos.hyy.fi"

def _fetch_csv(year: int, endpoint: str) -> pd.DataFrame:
    """Load csv data from year/endpoint and return it as a
    pandas DataFrame"""

    url = f"{BASE_URL}/{year}/{endpoint}"

    with urllib.request.urlopen(url) as response:
        # TODO: There is really no need to use pandas here,
        # and I would like the data just as a dict, but
        # I just couldn't get csv.DictReader working for now
        data = response.read().decode("utf-8")
        return pd.read_csv(StringIO(data), sep=",")

def _fetch(year: int, endpoint: str) -> dict:
    """Load json data from year/endpoint and return it as a dict"""

    url = f"{BASE_URL}/{year}/{endpoint}"

    with urllib.request.urlopen(url) as response:
        return json.load(response)

def result(year: int) -> dict:
    """Fetch vaalitulos.hyy.fi/<year>/result.json"""

    return _fetch(year, "result.json")

def candidates(year: int) -> dict:
    """Fetch vaalitulos.hyy.fi/<year>/candidates.json"""

    return _fetch(year, "candidates.json")

def votes(year: int) -> pd.DataFrame:
    """Fetch vaalitulos.hyy.fi/<year>/votes.csv"""

    return _fetch_csv(year, "votes.csv", dataformat="csv")

def votes_by_faculty(year: int) -> dict:
    """Fetch vaalitulos.hyy.fi/<year>/votes_by_faculty.json"""

    return _fetch(year, "votes_by_faculty.json")

def votes_by_hour(year: int) -> dict:
    """Fetch vaalitulos.hyy.fi/<year>/votes_by_hour.json"""

    return _fetch(year, "votes_by_hour.json")

