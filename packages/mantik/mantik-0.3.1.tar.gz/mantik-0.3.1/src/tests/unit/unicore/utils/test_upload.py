import pathlib

import pytest

import mantik.unicore.config.environment as environment
import mantik.unicore.config.executable as executable
import mantik.unicore.utils.upload as upload_files


@pytest.mark.parametrize(
    ("singularity_image", "expect_image_is_included"),
    [
        # Test case: upload local image
        (
            environment.Environment(
                execution=executable.Singularity(
                    path=pathlib.Path("mantik-test.sif"),
                    type="local",
                ),
            ),
            True,
        ),
        # Test case: use remote image, don't upload a local image
        (
            environment.Environment(
                execution=executable.Singularity(
                    path=pathlib.Path("/absolute/path/to/remote/image.sif"),
                    type="remote",
                ),
            ),
            False,
        ),
    ],
)
def test_get_files_to_upload(
    example_project_path,
    example_config,
    singularity_image,
    expect_image_is_included,
):
    example_config.environment = singularity_image
    files = upload_files.get_files_to_upload(
        project_dir=example_project_path, config=example_config
    )
    if expect_image_is_included:
        assert example_project_path / "mantik-test.sif" in files
    else:
        assert example_project_path / "mantik-test.sif" not in files


@pytest.mark.parametrize(
    ("project_path", "exclude", "expected"),
    [
        ("example_project_path", ["*"], []),
        (
            "example_project_path",
            ["*.py"],
            [
                "Dockerfile",
                "MLproject",
                "recipe.def",
                "unicore-config.json",
                "unicore-config.yaml",
                "mantik-test.sif",
                "config-with-errors.yaml",
            ],
        ),
        (
            "example_project_path",
            [
                "Dockerfile",
                "MLproject",
                "recipe.def",
                "unicore-config.json",
                "unicore-config.yaml",
                "mantik-test.sif",
                "config-with-errors.yaml",
            ],
            ["main.py", "test_subfolder/test.py"],
        ),
        (
            "example_project_path",
            [
                "Dockerfile",
                "MLproject",
                "recipe.def",
                "unicore-config.json",
                "unicore-config.yaml",
                "mantik-test.sif",
                "test_subfolder/",
                "config-with-errors.yaml",
            ],
            ["main.py"],
        ),
    ],
)
def test_exclude_files(project_path, exclude, expected, request):
    for i, element in enumerate(expected):
        expected[i] = request.getfixturevalue(project_path) / element
    included_list = upload_files._recursively_list_files_in_directory(
        request.getfixturevalue(project_path), exclude
    )
    for element in included_list:
        assert element in expected
    assert len(expected) == len(included_list)


@pytest.mark.parametrize(
    ("file_name", "exclude", "expected"),
    [
        ("main.py", ["*.py"], True),
        ("main.py", ["*.yaml"], False),
    ],
)
def test_file_matches_exclude_entry(
    file_name, example_project_path, exclude, expected, request
):
    filepath = example_project_path / file_name
    assert expected == upload_files._file_matches_exclude_entry(
        filepath, exclude
    )


@pytest.mark.parametrize(
    ("file_path", "pattern", "expected"),
    [
        ("example_project_path", "*.py", ["main.py"]),
        ("example_project_path", "**/*.py", ["main.py", "test.py"]),
    ],
)
def test_files_matching_pattern(file_path, pattern, expected, request):  #
    assert expected == upload_files._files_matching_pattern(
        request.getfixturevalue(file_path), pattern
    )


@pytest.mark.parametrize(
    ("element_relative_path", "exclude", "expected"),
    [
        (pathlib.Path("subfolder/test.py"), ["subfolder/"], True),
    ],
)
def test_excluded_subdirectory(element_relative_path, exclude, expected):
    assert expected == upload_files._excluded_subdirectory(
        element_relative_path, exclude
    )
