from fastapi import APIRouter, HTTPException, status
from api.classes.formula1 import TeamsParser
from api.routers.responses.team_responses import GET_TEAMS_200_RESPONSE

router = APIRouter(
    prefix="/teams",
    tags=["Teams"],
    responses=GET_TEAMS_200_RESPONSE,
)


@router.get("/{year}")
async def get_teams(year: int):
    url = f"https://www.formula1.com/en/results.html/{year}/team.html"
    teamsParser = TeamsParser(url)
    await teamsParser.fetch_data()
    data = teamsParser.get_teams_data()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Team data not found for the specified year ({year})")

    return data
