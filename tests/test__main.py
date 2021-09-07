import sys
from io import StringIO

import pytest

from frage.__main__ import main, output, run
from frage.models import Response


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


class TestIntegration:
    @pytest.fixture
    def setup_entry_point(self, tmp_path, monkeypatch, mockresponse) -> str:
        expected_body = "response body"
        name = "request "
        request_definition = """
        { method = "GET", path = "/foo", headers = {=}, body = ""}
        """
        request_filepath = tmp_path / f"{name}.dhall"
        request_filepath.write_text(request_definition)

        mockresponse.get("/foo", body=expected_body)
        monkeypatch.setattr(
            sys,
            "argv",
            ["frage", name, "--dir", str(tmp_path)],
        )

        return expected_body

    async def test__main(self, capsys, setup_entry_point):
        await main()

        assert capsys.readouterr().out == setup_entry_point

    def test__run(self, capsys, setup_entry_point):
        run()

        assert capsys.readouterr().out == setup_entry_point
