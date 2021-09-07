import sys
from argparse import Namespace
from pathlib import Path
from io import StringIO

import pytest
from yarl import URL

from frage.__main__ import main, output, parse_args, run
from frage.models import Response


class TestParseArgs:
    @pytest.fixture
    def expected_args(self) -> Namespace:
        return Namespace(
            request_file="/path/",
            dir=None,
            base_url=None,
        )

    @pytest.fixture
    def base_args(self, expected_args: Namespace) -> list[str]:
        return [expected_args.request_file]

    def test__base_url(self, base_args: list[str], expected_args: Namespace):
        # without
        got = parse_args(base_args)
        assert got == expected_args

        base_url = "https://foo"
        expected_args.base_url = URL(base_url)

        # with long
        got = parse_args(base_args + ["--base-url", base_url])
        assert got == expected_args

        # with short
        got = parse_args(base_args + ["-u", base_url])
        assert got == expected_args

    def test__request_dir(self, base_args: list[str], expected_args: Namespace):
        # without
        got = parse_args(base_args)
        assert got == expected_args

        dir_ = "/path/to/dir"
        expected_args.dir = Path(dir_)

        # with long
        got = parse_args(base_args + ["--dir", dir_])
        assert got == expected_args

        # with short
        got = parse_args(base_args + ["-d", dir_])
        assert got == expected_args


class TestOutput:
    async def test__ok(self):
        stream = StringIO()
        response = Response(
            status=200,
            headers={},
            body="a body",
        )
        output(response, stream)
        stream.seek(0)
        assert stream.read() == response.body


class TestMain:
    async def test__ok(self, capsys, tmp_path, monkeypatch, mockresponse):
        request_definition = """
        { method = "GET", path = "/foo", headers = {=}, body = ""}
        """
        request_filepath = tmp_path / "request.dhall"
        request_filepath.write_text(request_definition)

        mockresponse.get("/foo", body="response body")
        monkeypatch.setattr(sys, "argv", ["frage", str(request_filepath)])

        await main()

        assert capsys.readouterr().out == "response body"


class TestRun:
    def test__ok(self, capsys, tmp_path, monkeypatch, mockresponse):
        request_definition = """
        { method = "GET", path = "/foo", headers = {=}, body = ""}
        """
        request_filepath = tmp_path / "request.dhall"
        request_filepath.write_text(request_definition)

        mockresponse.get("/foo", body="response body")
        monkeypatch.setattr(sys, "argv", ["frage", str(request_filepath)])

        run()

        assert capsys.readouterr().out == "response body"
