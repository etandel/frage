from typing import Optional

from aiohttp import ClientSession
from yarl import URL

from frage.models import Request, Response


async def make_request(
    session: ClientSession,
    request: Request,
    *,
    base_url: Optional[URL] = None,
) -> Response:
    request_url = URL(request.path)
    url = base_url.join(request_url) if base_url else request_url

    req = session.request(
        request.method,
        url,
        headers=request.headers,
        data=request.body,
    )
    async with req as resp:
        response = Response(
            status=resp.status,
            headers=resp.headers,
            body=await resp.read(),
        )

    return response
