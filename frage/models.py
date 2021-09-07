from enum import Enum
from typing import List

from pydantic import BaseModel, Field, validator


class Method(str, Enum):
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    TRACE = "TRACE"
    CONNECT = "CONNECT"


Headers = dict[str, str]
Body = str


class BaseRequest(BaseModel):
    path: str
    method: Method
    headers: Headers
    body: Body


class Request(BaseRequest):
    pass


class Var(BaseModel):
    n: str = Field(regex=r"^[_\w][\-_\w\d]*")


class RawRequest(BaseRequest):
    variables: List[Var]

    @validator("variables", pre=True)
    def parse_vars(cls, v):
        return [x if isinstance(x, Var) else Var(n=x) for x in v]


class Response(BaseModel):
    status: int
    headers: Headers
    body: Body
