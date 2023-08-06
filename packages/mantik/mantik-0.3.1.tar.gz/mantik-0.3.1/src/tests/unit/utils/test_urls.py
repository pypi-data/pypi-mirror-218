import mantik.utils.urls as urls


def test_ensure_https_and_remove_double_slashes_from_path():
    url = "http://test-url.com/path//with/double//slashes"
    expected = "https://test-url.com/path/with/double/slashes"

    result = urls.ensure_https_and_remove_double_slashes_from_path(url)

    assert result == expected


def test_ensure_https_and_remove_double_slashes_from_path_also_with_3_slashes():
    url = "http://test-url.com///path//with/double//slashes"
    expected = "https://test-url.com/path/with/double/slashes"

    result = urls.ensure_https_and_remove_double_slashes_from_path(url)

    assert result == expected
