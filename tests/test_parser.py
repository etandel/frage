from io import StringIO
from pathlib import Path
from typing import TextIO

import pytest

from frage.models import Method, Request
from frage.parser import open_file, parse, ParsingError


def get_definition(filename: str) -> TextIO:
    path = Path(__file__).parent / "data" / filename
    return path.open()


class TestFindFile:
    @pytest.fixture
    def content(self) -> str:
        return "{=}"

    def test__root_file_found(self, tmp_path: Path, content: str):
        path = tmp_path / "a_file.dhall"
        path.write_text(content)

        with open_file(tmp_path, "a_file") as got:
            assert got.read() == content

    def test__nested_file_found(self, tmp_path: Path, content: str):
        base_dir = tmp_path / "nested"
        base_dir.mkdir()

        path = base_dir / "a_file.dhall"
        path.write_text(content)

        with open_file(tmp_path, "nested/a_file") as got:
            assert got.read() == content

    def test__file_not_found(self, tmp_path: Path, content: str):
        path = tmp_path / "a_file.dhall"
        path.write_text(content)

        with pytest.raises(FileNotFoundError):
            with open_file(tmp_path, "another_file"):
                pass


class TestParse:
    def test__no_headers(self):
        expected = Request(
            method=Method.POST,
            path="x/foo/bar",
            headers={},
            body=b"a request body",
        )

        with get_definition("valid_request_without_headers.dhall") as f:
            got = parse(f)

        assert got == expected

    def test__with_headers(self):
        expected = Request(
            method=Method.POST,
            path="x/foo/bar",
            headers={
                "x-header-1": "value-1",
                "x-header-2": "value-2",
            },
            body=b"a request body",
        )

        with get_definition("valid_request_with_headers.dhall") as f:
            got = parse(f)

        assert got == expected

    def test__dhall_parse_error(self):
        with pytest.raises(ParsingError):
            parse(StringIO("invalid dhall content"))

    def test__pydantic_error(self):
        with pytest.raises(ParsingError):
            parse(StringIO("{=}"))
