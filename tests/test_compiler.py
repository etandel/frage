import pytest

from frage.models import Method, RawRequest, Request, Var
from frage.compiler import compile_request


class TestCompile:
    def test__no_vars(self):
        rr = RawRequest(
            variables=[],
            method=Method.GET,
            path="",
            headers={},
            body="",
        )

        expected = Request(
            method=Method.GET,
            path="",
            headers={},
            body="",
        )

        got = compile_request(rr, vars_={})
        assert got == expected

    def test__var_in_path(self):
        rr = RawRequest(
            variables=["var1", "var2"],
            method=Method.GET,
            path="/foo/{var1}?q={var2}",
            headers={},
            body="",
        )

        expected = Request(
            method=Method.GET,
            path="/foo/value1?q=value2",
            headers={},
            body="",
        )

        got = compile_request(rr, vars_={"var1": "value1", "var2": "value2"})
        assert got == expected

    def test__var_in_header(self):
        rr = RawRequest(
            variables=["var1", "var2"],
            method=Method.GET,
            path="",
            headers={"{var1}": "{var2}"},
            body="",
        )

        expected = Request(
            method=Method.GET,
            path="",
            headers={"value1": "value2"},
            body="",
        )

        got = compile_request(rr, vars_={"var1": "value1", "var2": "value2"})
        assert got == expected

    def test__var_in_body(self):
        rr = RawRequest(
            variables=["var1", "var2"],
            method=Method.GET,
            path="",
            headers={},
            body="body with var1 = {var1} and var2 = {var2}",
        )

        expected = Request(
            method=Method.GET,
            path="",
            headers={},
            body="body with var1 = value1 and var2 = value2",
        )

        got = compile_request(rr, vars_={"var1": "value1", "var2": "value2"})
        assert got == expected
