import sys
from io import StringIO

from yarl import URL

from frage.__main__ import main, output, parse_args, run
from frage.models import Response


class TestParseArgs:
    def test__with_base_url(self):
        expected_request_file = "/path/"
        expected_base_url = "https://foo"
        got = parse_args([expected_request_file, "--base-url", expected_base_url])
        assert got.request_file == expected_request_file
        assert got.base_url == URL(expected_base_url)

    def test__without_base_url(self):
        expected_request_file = "/path/"
        got = parse_args([expected_request_file])
        assert got.request_file == expected_request_file
        assert got.base_url is None


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
