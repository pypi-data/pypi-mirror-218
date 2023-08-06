import requests
from typing import Dict


async def get_login_token(login_url: str, user: str, password: str) -> str:
    data = {"username": user, "password": password}

    res = await _make_request(login_url=login_url, payload=data)
    token = res["token"]

    return token


async def _make_request(login_url: str, payload: Dict[str, str]) -> Dict[str, str]:
    # TODO change this to use https://github.com/aio-libs/aiohttp
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url=login_url, data=payload, headers=headers)
    if not response.status_code == 200:
        raise Exception(
            f"Error logging in to GraphQL server , error code {response.status_code}, error {response.text}"
        )
    results = response.json()
    return results
