from io import StringIO

from frage.__main__ import main, output, parse_args
from frage.models import Response


class TestParseArgs:
    def test__ok(self):
        got = parse_args(["/path/"])
        assert got.request_file == "/path/"


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
    async def test__ok(self, capsys, tmp_path, mockresponse):
        request_definition = """
        { method = "GET", path = "/foo", headers = {=}, body = ""}
        """
        request_filepath = tmp_path / "request.dhall"
        request_filepath.write_text(request_definition)

        mockresponse.get("/foo", body="response body")

        await main([str(request_filepath)])

        assert capsys.readouterr().out == "response body"
