from bs4 import BeautifulSoup
import requests
from models import (
    Circuit,
    Driver,
    FastestLap,
    Race,
    RaceResult,
    Team
)
from sqlalchemy.orm import Session


class DriversParser:
    def __init__(self, url: str, db: Session):
        self.url = url
        self.driver_data = {}
        self.db = db

    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        table_rows = soup.select("tr")

        for row in table_rows:
            name_td = row.select_one("a.dark.bold")
            nationality_td = row.select_one("td.dark.semi-bold.uppercase")
            team_td = row.select_one("a.grey.semi-bold.uppercase")
            points_td = row.select_one("td.dark.bold")

            if name_td and nationality_td and team_td and points_td:
                driver_name_parts = name_td.text.strip().replace("\n", " ").split()
                driver_name = " ".join(driver_name_parts[:-1])
                driver_prefix = driver_name_parts[-1]
                driver_pos = name_td.find_previous(
                    "td", class_="dark").text.strip()
                nationality = nationality_td.text.strip()
                team = team_td.text.strip()
                points = int(points_td.text)

                driver = Driver(
                    name=driver_name,
                    nationality=nationality,
                    points=points,
                    position=driver_pos,

                )

                self.driver_data[driver_prefix] = {
                    "name": driver_name,
                    "position": driver_pos,
                    "nationality": nationality,
                    "car": team,
                    "points": points
                }

    def get_driver_data(self):
        return self.driver_data


class RacesParser:
    def __init__(self, url: str):
        self.url = url
        self.races_data = {}

    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        table_rows = soup.select("tr")

        for row in table_rows:
            grand_prix_td = row.select_one("a.dark.bold")
            date_td = row.select_one("td.dark.hide-for-mobile")
            winner_td = row.select("td.dark.bold")
            car_td = row.select_one("td.semi-bold")
            laps_td = row.select_one("td.bold.hide-for-mobile")
            duration_td = row.select_one("td.dark.bold.hide-for-tablet")

            if grand_prix_td:
                winner_name_parts = winner_td[1].text.split()
                winer_name = " ".join(winner_name_parts[:-1])
                grand_prix = grand_prix_td.text.strip()
                date = date_td.text.strip()
                car = car_td.text.strip()
                laps = laps_td.text.strip()
                duration = duration_td.text.strip()

                self.races_data[grand_prix] = {
                    "date": date,
                    "winner": winer_name,
                    "car": car,
                    "laps": laps,
                    "duration": duration
                }

    def get_races_data(self):
        return self.races_data


class TeamsParser:
    def __init__(self, url: str):
        self.url = url
        self.teams_data = []

    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        table_rows = soup.select("tr")

        for row in table_rows:
            position_td = row.select_one("td.dark")
            team_td = row.select_one("a.dark.bold.uppercase")
            points_td = row.select_one("td.dark.bold")

            if team_td:
                position = position_td.text
                name = team_td.text
                points = points_td.text

                db_team = Team(name=name, position=position, points=points)

                self.teams_data.append(db_team)

    def get_teams_data(self):
        return self.teams_data


class FastestLapsParser:
    def __init__(self, url: str):
        self.url = url
        self.fastest_laps_data = {}

    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        table_rows = soup.select("tr")

        for row in table_rows:
            grand_prix_td = row.select_one("td.width30.dark")
            driver_td = row.select_one("td.width25.dark.bold")
            car_td = row.select_one("td.width25.semi-bold")
            lap_time_td = row.select("td.dark.bold")

            if driver_td:
                driver_name_parts = driver_td.text.strip().replace("\n", " ").split()
                driver_name = " ".join(driver_name_parts[:-1])
                driver_prefix = driver_name_parts[-1]
                grand_prix = grand_prix_td.text
                car = car_td.text
                lap_time = lap_time_td[1].text

                self.fastest_laps_data[grand_prix] = {
                    "driver": driver_name,
                    "driver_prefix": driver_prefix,
                    "car": car,
                    "lap_time": lap_time
                }

    def get_fastest_laps_data(self):
        return self.fastest_laps_data
