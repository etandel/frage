from frage.models import RawRequest, Request


def interpolate(s: str, v: dict[str, str]) -> str:
    return s.format(**v)


def noop(s: str, v: dict[str, str]) -> str:
    return s


def compile_request(raw_request: RawRequest, vars_: dict[str, str]) -> Request:
    interp = interpolate if raw_request.variables else noop

    return Request(
        method=raw_request.method,
        path=interp(raw_request.path, vars_),
        headers={
            interp(k, vars_): interp(v, vars_) for k, v in raw_request.headers.items()
        },
        body=interp(raw_request.body, vars_),
    )
