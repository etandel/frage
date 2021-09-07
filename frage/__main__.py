import sys
import argparse
import asyncio
from pathlib import Path
from typing import IO, Optional, Sequence

from aiohttp import ClientSession
from yarl import URL

from frage.http import make_request
from frage.models import Response
from frage.parser import open_file, parse


def parse_args(raw_args: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(description="Make configurable HTTP requests")
    parser.add_argument("request_file", help="Dhall file with request definition")
    parser.add_argument(
        "-u", "--base-url", type=URL, help="Base URL to be joined with request path"
    )
    parser.add_argument(
        "-d", "--dir", type=Path, help="Directory where request files will be searched"
    )

    return parser.parse_args(raw_args)


def output(response: Response, stream: IO):
    stream.write(response.body)


async def main():
    args = parse_args()

    with open_file(args.dir, args.request_file) as f:
        request = parse(f)

    async with ClientSession() as s:
        response = await make_request(s, request, base_url=args.base_url)

    output(response, sys.stdout)


def run():
    asyncio.run(main())


if __name__ == "__main__":  # pragma: nocover
    run()
