import abc
import typing as t


class ConfigObject(abc.ABC):
    """An object contained in the config."""

    @classmethod
    def from_dict(cls, config: t.Dict) -> "ConfigObject":
        """Initialize from dict."""
        return cls._from_dict(config)

    def to_dict(self) -> t.Dict:
        """Return as dict."""
        return self._to_dict()

    @classmethod
    @abc.abstractmethod
    def _from_dict(cls, config: t.Dict) -> "ConfigObject":
        ...

    @abc.abstractmethod
    def _to_dict(self) -> t.Dict:
        ...
