import sys
import argparse
import asyncio
from typing import IO, Optional, Sequence

from aiohttp import ClientSession

from frage.http import make_request
from frage.models import Response
from frage.parser import parse


def parse_args(raw_args: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(description="Make configurable HTTP requests")
    parser.add_argument("request_file", help="Dhall file with request definition")

    return parser.parse_args(raw_args)


def output(response: Response, stream: IO):
    stream.write(response.body)


async def main(raw_args: Optional[Sequence[str]] = None):
    args = parse_args(raw_args)

    with open(args.request_file) as f:
        request = parse(f)

    async with ClientSession() as s:
        response = await make_request(s, request)

    output(response, sys.stdout)


if __name__ == "__main__":  # pragma: nocover
    asyncio.run(main())
