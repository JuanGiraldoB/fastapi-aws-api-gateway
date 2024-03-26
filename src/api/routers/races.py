from fastapi import APIRouter, HTTPException, status
from api.classes.formula1 import RacesParser, FastestLapsParser
from api.routers.responses.race_responses import GET_RACES_200_RESPONSE, GET_FASTEST_LAPS_200_RESPONSE

router = APIRouter(
    prefix="/races",
    tags=["Races"],
)


@router.get("/{year}", responses=GET_RACES_200_RESPONSE)
async def get_races(year: int):
    url = f"https://www.formula1.com/en/results.html/{year}/races.html"
    racesParcer = RacesParser(url)
    await racesParcer.fetch_data()
    data = racesParcer.get_races_data()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Race data not found for the specified year ({year})")

    return data


@router.get("/fastest-laps/{year}", responses=GET_FASTEST_LAPS_200_RESPONSE)
async def get_fastest_laps(year: int):
    url = f"https://www.formula1.com/en/results.html/{year}/fastest-laps.html"
    racesParcer = FastestLapsParser(url)
    await racesParcer.fetch_data()
    data = racesParcer.get_fastest_laps_data()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Fastest laps data not found for the specified year ({year})")

    return data
