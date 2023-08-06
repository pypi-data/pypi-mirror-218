import dataclasses
import typing as t

import pytest

import mantik.testing as testing
import mantik.unicore.config._base as _base
import mantik.unicore.config._utils as _utils
import mantik.unicore.exceptions as exceptions


@pytest.mark.parametrize(
    ("name", "value_type", "config", "expected"),
    [
        ("given", str, {"given": "value"}, "value"),
        (
            "given_with_incorrect_type",
            int,
            {"given_with_incorrect_type": "value"},
            exceptions.ConfigValidationError(),
        ),
        (
            "not_given",
            str,
            {"given": "value"},
            exceptions.ConfigValidationError(),
        ),
    ],
)
def test_get_required_config_value(name, value_type, config, expected):
    with testing.contexts.expect_raise_if_exception(expected):
        result = _utils.get_required_config_value(
            name=name,
            value_type=value_type,
            config=config,
        )

        assert result == expected


@pytest.mark.parametrize(
    ("name", "value_type", "default", "config", "expected"),
    [
        ("given", str, None, {"given": "value"}, "value"),
        (
            "given_with_incorrect_type",
            int,
            None,
            {"given_with_incorrect_type": "value"},
            exceptions.ConfigValidationError(),
        ),
        ("not_given", str, None, {"given": "value"}, None),
        ("not_given", str, None, {"given": "value"}, None),
        ("not_given", str, "default", {"given": "value"}, "default"),
    ],
)
def test_get_optional_config_value(
    name, value_type, default, config, expected, caplog
):
    with testing.contexts.expect_raise_if_exception(expected):
        _utils.logger.setLevel("DEBUG")
        result = _utils.get_optional_config_value(
            name=name,
            value_type=value_type,
            config=config,
            default=default,
        )

        assert result == expected
        if expected is None:
            assert "DEBUG" in caplog.text


@dataclasses.dataclass
class AnyConfigObject(_base.ConfigObject):
    test: str = "test"

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "AnyConfigObject":
        pass

    def _to_dict(self) -> t.Dict:
        return dataclasses.asdict(self)


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        (
            {"any": "value"},
            {"any": "value"},
        ),
        (
            {"any": None},
            {},
        ),
        (
            {"any": AnyConfigObject()},
            {"any": {"test": "test"}},
        ),
        # bool needs to be converted to lower-case string
        (
            {"any": True},
            {"any": "true"},
        ),
        (
            {"any": False},
            {"any": "false"},
        ),
    ],
)
def test_create_dict_with_not_none_values(kwargs, expected):
    result = _utils.create_dict_with_not_none_values(**kwargs)

    assert result == expected
