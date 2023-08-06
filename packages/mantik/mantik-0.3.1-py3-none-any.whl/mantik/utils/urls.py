import urllib.parse


def ensure_https_and_remove_double_slashes_from_path(url: str) -> str:
    """Ensure that a URL uses HTTPS and does not contain `//` in its path."""
    u = urllib.parse.urlparse(url)
    path = u.path.replace("//", "/")
    url = f"{u.netloc}{path}".replace("//", "/")
    return f"https://{url}"
