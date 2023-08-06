import pathlib

import pytest

import mantik.unicore.config.read as read
import mantik.unicore.exceptions


def test_read_config(unicore_config_yaml):
    backend_config = read.read_config(unicore_config_yaml)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2
    assert backend_config["Environment"]["Singularity"] == {
        "Path": "mantik-test.sif",
        "Type": "lOcAl",
    }


def test_read_config_unsupported_type():
    unsupported_format = ".yamml"
    with pytest.raises(mantik.unicore.exceptions.ConfigValidationError) as e:
        read.read_config(pathlib.Path(f"backend-config{unsupported_format}"))
    assert (
        "The given file type '.yamml' is not supported for the config, "
        "the supported ones are: '.json', '.yml', '.yaml'."
    ) == str(e.value)


def test_read_yaml_config(unicore_config_yaml):
    backend_config = read._read_yaml_config(unicore_config_yaml)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2
    assert backend_config["Environment"]["Singularity"] == {
        "Path": "mantik-test.sif",
        "Type": "lOcAl",
    }


def test_read_json_config(unicore_config_json):
    backend_config = read._read_yaml_config(unicore_config_json)
    assert (
        backend_config["UnicoreApiUrl"]
        == "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core"
    )
    assert backend_config["Resources"]["Queue"] == "devel"
    assert backend_config["Resources"]["Nodes"] == 2
    assert backend_config["Environment"]["Singularity"] == {
        "Path": "mantik-test.sif",
        "Type": "lOcAl",
    }
