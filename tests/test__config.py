import sys
from argparse import Namespace
from pathlib import Path

import pytest
from yarl import URL

from frage.config import Config, get_config, parse_args


@pytest.fixture
def expected_config() -> Config:
    return Config(
        request_name="/path/",
        dir=None,
        base_url=None,
    )


@pytest.fixture
def expected_args(expected_config: Config) -> Namespace:
    return Namespace(
        name=expected_config.request_name,
        dir=expected_config.dir,
        base_url=expected_config.base_url,
    )


@pytest.fixture
def base_args(expected_args: Namespace) -> list[str]:
    return [expected_args.name]


class TestParseArgs:
    def test__base_url(self, base_args: list[str], expected_args: Namespace):
        # without
        got = parse_args(base_args)
        assert got == expected_args

        base_url = "https://foo"
        expected_args.base_url = URL(base_url)

        # with long
        got = parse_args(base_args + ["--base-url", base_url])
        assert got == expected_args

        # with short
        got = parse_args(base_args + ["-u", base_url])
        assert got == expected_args

    def test__request_dir(self, base_args: list[str], expected_args: Namespace):
        # without
        got = parse_args(base_args)
        assert got == expected_args

        dir_ = "/path/to/dir"
        expected_args.dir = Path(dir_)

        # with long
        got = parse_args(base_args + ["--dir", dir_])
        assert got == expected_args

        # with short
        got = parse_args(base_args + ["-d", dir_])
        assert got == expected_args


class TestGetConfig:
    def test__with_raw_args(self, base_args: list[str], expected_config: Config):
        assert get_config(base_args) == expected_config

    def test__without_raw_args(
        self, base_args: list[str], expected_config: Config, monkeypatch
    ):
        monkeypatch.setattr(sys, "argv", ["frage"] + base_args)
        assert get_config() == expected_config
