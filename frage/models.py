from enum import Enum

from pydantic import BaseModel, AnyHttpUrl


class Method(str, Enum):
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


Headers = dict[str, str]
Body = bytes


class Request(BaseModel):
    path: AnyHttpUrl
    method: Method
    headers: Headers
    body: Body


class Response(BaseModel):
    status: int
    headers: Headers
    body: Body