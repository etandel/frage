from contextlib import contextmanager
from pathlib import Path
from typing import TextIO, Iterator

import dhall

from frage.models import RawRequest


class ParsingError(Exception):
    pass


@contextmanager
def open_file(dir_: Path, name: str) -> Iterator[TextIO]:
    with (dir_ / Path(name + ".dhall")).open() as f:
        yield f


def parse(data: TextIO) -> RawRequest:
    try:
        return RawRequest.parse_obj(dhall.load(data))
    except Exception as e:
        raise ParsingError() from e
