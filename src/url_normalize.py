import re
from urllib.parse import urlparse


def normalize_url(url):
    """
    Return a string safe for urlparse feature extraction, or None if invalid.
    Prepends http:// when no scheme is present so the host lands in netloc.
    """
    if url is None or not isinstance(url, str):
        return None
    url = url.strip()
    if not url or len(url) > 8192:
        return None
    lower = url.lower()
    if lower.startswith(("javascript:", "data:", "vbscript:")):
        return None
    if not re.match(r"^[a-zA-Z][\w+.-]*:", url):
        url = "http://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        return None
    return url