import requests

from app.config import settings


ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"


def fetch_jobs(
    country: str = "in",
    page: int = 1,
    what: str = "software engineer intern",
    where: str = "Bangalore",
    results_per_page: int = 10,
) -> list[dict]:
    url = f"{ADZUNA_BASE_URL}/jobs/{country}/search/{page}"

    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": what,
        "where": where,
        "content-type": "application/json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])