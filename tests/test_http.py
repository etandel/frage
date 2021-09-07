import pytest
from aioresponses.core import RequestCall
from aiohttp import ClientSession
from yarl import URL

from frage.http import make_request
from frage.models import Method, Request, Response


@pytest.fixture
async def session():
    async with ClientSession() as s:
        yield s


@pytest.fixture
def req() -> Request:
    return Request(
        path="get",
        method=Method.POST,
        headers={
            "Content-type": "xxx/yyy",
            "x-header-1": "value-1",
            "x-header-2": "value-2",
        },
        body="request body",
    )


@pytest.fixture
def response() -> Response:
    return Response(
        status=200,
        headers={
            "x-response-header-1": "value-1",
            "x-response-header-2": "value-2",
            "Content-type": "xxx/yyy",
        },
        body="response body",
    )


class TestMakeRequest:
    async def test__with_base_url(
        self, mockresponse, session: ClientSession, req: Request, response: Response
    ):
        base_url = URL("http://httpbin/")
        expected_url = base_url.join(URL(req.path))

        mockresponse.post(
            expected_url,
            status=response.status,
            body=response.body,
            headers=response.headers,
        )

        response = await make_request(session, req, base_url=base_url)

        assert response == response
        requests = mockresponse.requests[(req.method, expected_url)]

        assert requests == [
            RequestCall(
                args=(),
                kwargs={"headers": req.headers, "data": req.body},
            ),
        ]

    async def test__without_base_url(
        self, mockresponse, session: ClientSession, req: Request, response: Response
    ):
        base_url = None
        expected_url = URL(req.path)

        mockresponse.post(
            expected_url,
            status=response.status,
            body=response.body,
        )
        mockresponse.post(
            expected_url,
            status=response.status,
            body=response.body,
        )

        response = await make_request(session, req)
        response = await make_request(session, req, base_url=base_url)

        assert response == response
        requests = mockresponse.requests[(req.method, expected_url)]

        assert requests == [
            RequestCall(
                args=(),
                kwargs={"headers": req.headers, "data": req.body},
            ),
            RequestCall(
                args=(),
                kwargs={"headers": req.headers, "data": req.body},
            ),
        ]
