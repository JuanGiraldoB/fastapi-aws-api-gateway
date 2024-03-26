from fastapi import APIRouter, HTTPException, status
from api.classes.formula1 import StandingsParser
from api.routers.responses.driver_responses import GET_DRIVERS_200_RESPONSE

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
    responses=GET_DRIVERS_200_RESPONSE
)


@router.get("/{year}")
async def get_drivers(year: int):
    url = f"https://www.formula1.com/en/results.html/{year}/drivers.html"
    standingsParser = StandingsParser(url)
    await standingsParser.fetch_data()
    data = standingsParser.get_driver_data()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Race data not found for the specified year ({year})")

    return data
