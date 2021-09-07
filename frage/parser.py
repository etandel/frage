from typing import IO

import dhall

from frage.models import Request


class ParsingError(Exception):
    pass


def parse(data: IO) -> Request:
    try:
        return Request.parse_obj(dhall.load(data))
    except Exception as e:
        raise ParsingError() from e
