import sys
import asyncio
from typing import IO

from aiohttp import ClientSession

from frage.config import get_config
from frage.http import make_request
from frage.models import Response
from frage.parser import open_file, parse


def output(response: Response, stream: IO):
    stream.write(response.body)


async def main():
    config = get_config()

    with open_file(config.dir, config.request_name) as f:
        request = parse(f)

    async with ClientSession() as s:
        response = await make_request(s, request, base_url=config.base_url)

    output(response, sys.stdout)


def run():
    asyncio.run(main())


if __name__ == "__main__":  # pragma: nocover
    run()
