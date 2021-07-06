import os
import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from typing import Dict
from functools import cache

@cache
def get_county_code_map() -> Dict[str, str]:
    html = requests.get("https://www.teoalida.ro/lista-judete/").text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("tbody")
    
    prefixes = {}
    for row in table.find_all("tr"):
        if row.contents[1].string is not None:
            prefixes[row.contents[1].string] = row.contents[3].string

    return prefixes


def get_county_data(county_code: str, year: int) -> pd.DataFrame:
    # mev: -2 = absent
    # ri/mi/lmi: NaN = absent

    if year >= 2021:
        URL = f"http://evaluare.edu.ro/rezultate/{county_code}/data/candidate.json"
    elif year >= 2019:
        URL = f"http://static.evaluare.edu.ro/{year}/rezultate/{county_code}/data/candidate.json"
    else:
        raise ValueError("Data from before 2019 is no logner available.")
    
    county_map = get_county_code_map()
    print(f"Getting data from {county_map[county_code]}.")

    # TODO: implement progress bar

    with open("temp/temp.json", "w", encoding="utf-8") as temp_write:
        print("\tRequesting data.")
        json_response = requests.get(URL).json()
        print("\tReceived response.")
        json.dump(json_response, temp_write)
    
    with open("temp/temp.json", "r", encoding="utf-8") as temp_read:
        print("\tGenerating dataframe.")
        df = pd.read_json(temp_read, encoding="utf-8")
        df = df.drop(columns=["index"])
        print("\tGenerated dataframe.")
        return df

if __name__ == "__main__":
    county_code_map = get_county_code_map()
    
    YEAR = 2019

    dataframes = []
    for i, county_code in enumerate(county_code_map.keys()):
        dataframes.append(get_county_data(county_code, YEAR))
        time.sleep(5) # because of course they have a spam prevention mechanism bruh

    data = pd.concat(dataframes)
    data = data.reset_index()
    data = data.drop(columns=["index"])
    data.to_csv(f"data/csv/note_en_{YEAR}.csv")
    data.to_excel(f"data/xlsx/note_en_{YEAR}.xlsx")
