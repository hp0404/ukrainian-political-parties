import json

import requests
from bs4 import BeautifulSoup

import pandas as pd 


def fetch():
    r = requests.get("https://minjust.gov.ua/m/4561")
    return BeautifulSoup(r.content, "html.parser")


def create_table(soup):
    table = soup.find("table")
    records = [
        [
            each.text.replace("\n", "").replace("*", "").strip()
            for each in tr.find_all("td")
        ]
        for tr in table.find_all("tr")
    ]
    
    df = pd.DataFrame(records)
    df.columns = df.iloc[0, :]
    return df.iloc[2:,]


def save_data(df):
    df.to_csv("parties.csv", index=False)
    with open("parties.json", "w", encoding="utf-8") as json_file:
        json.dump(df.to_dict(orient="records"), json_file, ensure_ascii=False, indent=4)


def main():
    soup = fetch()
    df = create_table(soup)
    save_data(df)
    
    
if __name__ == "__main__":
    main()
    