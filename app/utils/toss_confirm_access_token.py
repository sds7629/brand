import asyncio
from typing import Any

import aiohttp

from app.config import TOSS_CONFIRM_CLIENT_KEY, TOSS_CONFIRM_SECRET_KEY

confirm_access_token_url = "https://oauth2.cert.toss.im/token"


async def get_access_token(client_id: str, client_secret: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as client:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "ca",
        }
        async with client.post(url=confirm_access_token_url, headers=headers, data=data) as res:
            print(await res.json())
            if res.status != 200:
                raise Exception(res.status)
            response = await res.json()
            access_token = response["access_token"]
            expires_in = response["expires_in"]

            return {"access_token": access_token, "expires_in": expires_in}


asyncio.run(get_access_token(TOSS_CONFIRM_CLIENT_KEY, TOSS_CONFIRM_SECRET_KEY))
