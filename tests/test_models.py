import pytest
from pydantic import ValidationError

from frage.models import Method, RawRequest, Var


class TestVar:
    def test__name_validation(self):
        assert Var(n="x").n == "x"
        assert Var(n="xx").n == "xx"
        assert Var(n="x12").n == "x12"
        assert Var(n="x-x").n == "x-x"
        assert Var(n="x_x").n == "x_x"
        assert Var(n="x-x12").n == "x-x12"
        assert Var(n="x_x12").n == "x_x12"
        assert Var(n="x_1234").n == "x_1234"
        assert Var(n="_1234").n == "_1234"

        assert Var(n="X").n == "X"
        assert Var(n="Xx").n == "Xx"
        assert Var(n="X12").n == "X12"
        assert Var(n="X-x").n == "X-x"
        assert Var(n="X_x").n == "X_x"
        assert Var(n="X-x12").n == "X-x12"
        assert Var(n="X_x12").n == "X_x12"
        assert Var(n="X_1234").n == "X_1234"
        assert Var(n="_1234").n == "_1234"
        assert Var(n="xY").n == "xY"

        # fail
        with pytest.raises(ValidationError):
            assert Var(n="1")
            assert Var(n="12")
            assert Var(n="-")
            assert Var(n="-1234")
            assert Var(n="-xxx")


class TestRawRequest:
    def test__parse_vars(self):
        base_data = {"path": "", "method": Method.GET, "headers": {}, "body": ""}

        assert RawRequest(variables=[], **base_data).variables == []

        r = RawRequest(variables=["x", "y"], **base_data)
        assert r.variables == [Var(n="x"), Var(n="y")]

        r = RawRequest(variables=[Var(n="x"), Var(n="y")], **base_data)
        assert r.variables == [Var(n="x"), Var(n="y")]
