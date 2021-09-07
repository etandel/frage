import inspect

import pytest


def pytest_collection_modifyitems(session, config, items):
    """
    This is a pytest hook that automatically marks all async test cases
    to be collected and run.
    """
    for item in items:
        if isinstance(item, pytest.Function) and inspect.iscoroutinefunction(
            item.function
        ):
            item.add_marker(pytest.mark.asyncio)

