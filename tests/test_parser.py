from io import StringIO
from pathlib import Path
from typing import IO

import pytest

from frage.models import Method, Request
from frage.parser import parse, ParsingError


def get_definition(filename: str) -> IO:
    path = Path(__file__).parent / "data" / filename
    return path.open()


class TestParse:
    def test__ok(self):
        expected = Request(
            method=Method.POST,
            path="/x/foo/bar",
            headers={},
            body=b"a request body",
        )

        with get_definition("valid_request.dhall") as f:
            got = parse(f)

        assert got == expected

    def test__dhall_parse_error(self):
        with pytest.raises(ParsingError):
            parse(StringIO("invalid dhall content"))

    def test__pydantic_error(self):
        with pytest.raises(ParsingError):
            parse(StringIO("{=}"))
