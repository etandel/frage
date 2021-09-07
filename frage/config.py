import argparse
from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel
from yarl import URL


class Config(BaseModel):
    request_name: str
    base_url: Optional[URL]
    dir: Optional[Path]

    class Config:
        arbitrary_types_allowed = True


def get_config(raw_args: Optional[Sequence[str]] = None) -> Config:
    args = parse_args(raw_args)
    return Config(
        request_name=args.name,
        base_url=args.base_url,
        dir=args.dir,
    )


def parse_args(raw_args: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(description="Make configurable HTTP requests")
    parser.add_argument(
        "name", help="Name of Dhall file with request definition, without extension"
    )
    parser.add_argument(
        "-u", "--base-url", type=URL, help="Base URL to be joined with request path"
    )
    parser.add_argument(
        "-d", "--dir", type=Path, help="Directory where request files will be searched"
    )

    return parser.parse_args(raw_args)
