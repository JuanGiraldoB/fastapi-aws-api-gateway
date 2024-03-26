from models import (
    Circuit,
    Team,
    Driver,
    Race,
    RaceResult,
    FastestLap,
    Base
)
from classes.f1 import (
    TeamsParser
)
from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


# Create a Circuit object
# monza_circuit = Circuit(name="Monza")

# Create a Team object
# red_bull_team = Team(name="Red Bull", points=140)

# Create a Driver object (assuming Red Bull driver)
# max_verstappen = Driver(name="Max Verstappen",
# nationality="Dutch", team=red_bull_team)

# Create a Race object (assuming year 2024)
# italian_gp_2024 = Race(
# year=2024, date="2024-09-08", circuit=monza_circuit)

# Create a Result object for Max Verstappen in the Italian GP (assuming 1st position)
# italian_gp_result = RaceResult(
# position=1, driver=max_verstappen, race=italian_gp_2024)

# Create a FastestLap object for Max Verstappen in the Italian GP (assuming fastest lap time)
# italian_gp_fastest_lap = FastestLap(driver=max_verstappen, time="1:19.000")

# Print the objects (optional)
# print(f"Circuit: {monza_circuit.name}")
# print(f"Team: {red_bull_team.name} - Points: {red_bull_team.points}")
# print(
#     f"Driver: {max_verstappen.name} - Nationality: {max_verstappen.nationality}")
# print(f"Race: {italian_gp_2024.year} - {italian_gp_2024.date} - Circuit: {italian_gp_2024.circuit.name}")
# print(
#     f"Result: {italian_gp_result.position} - Driver: {italian_gp_result.driver.name}")
# print(
#     f"Fastest Lap: Driver: {italian_gp_fastest_lap.driver.name} - Time: {italian_gp_fastest_lap.time}")

teamParser = TeamsParser(
    url="https://www.formula1.com/en/results.html/2024/team.html")

teamParser.fetch_data()
teams = teamParser.get_teams_data()

db = next(get_db())

for team in teams:
    db.add(team)

# Add the objects to the session
# db.add(monza_circuit)
# db.add(red_bull_team)
# db.add(max_verstappen)
# db.add(italian_gp_2024)
# db.add(italian_gp_result)
# db.add(italian_gp_fastest_lap)

# Commit the changes to the database
db.commit()
