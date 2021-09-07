from aiohttp import ClientSession

from frage.models import Request, Response


async def make_request(session: ClientSession, request: Request) -> Response:
    req = session.request(
        request.method,
        request.path,
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
