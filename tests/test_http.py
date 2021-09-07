import pytest
from aioresponses import aioresponses
from aioresponses.core import RequestCall
from aiohttp import ClientSession
from yarl import URL

from frage.http import make_request
from frage.models import Method, Request, Response


@pytest.fixture
def mockresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
async def session():
    async with ClientSession() as s:
        yield s


class TestMakeRequest:
    async def test__ok(self, mockresponse, session: ClientSession):
        request = Request(
            path="http://httpbin/get",
            method=Method.POST,
            headers={
                "Content-type": "xxx/yyy",
                "x-header-1": "value-1",
                "x-header-2": "value-2",
            },
            body="request body",
        )

        expected_response = Response(
            status=200,
            headers={
                "x-response-header-1": "value-1",
                "x-response-header-2": "value-2",
                "Content-type": "xxx/yyy",
            },
            body="response body",
        )

        mockresponse.post(
            request.path,
            status=expected_response.status,
            body=expected_response.body,
            headers=expected_response.headers,
        )

        response = await make_request(session, request)

        assert response == expected_response
        requests = mockresponse.requests[(request.method, URL(request.path))]

        assert requests == [
            RequestCall(
                args=(),
                kwargs={"headers": request.headers, "data": request.body},
            ),
        ]
