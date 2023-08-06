from urllib.parse import urljoin

POSBUS_PATH = "/posbus"
GUEST_AUTH_PATH = "/api/v4/auth/guest-token"
CHALLENGE_PATH = "/api/v4/auth/challenge"
TOKEN_PATH = "/api/v4/auth/token"


def auth_guest_url(base_url):
    return urljoin(base_url, GUEST_AUTH_PATH)


def auth_challenge_url(base_url):
    return urljoin(base_url, CHALLENGE_PATH)


def auth_token_url(base_url):
    return urljoin(base_url, TOKEN_PATH)


def posbus_websocket_url(base_url):
    # wss doesn't work with websocket lib currently.
    # url_split = urlsplit(base_url)
    # ws_scheme = "ws" if url_split.scheme == "http" else "wss"
    # ws_base_url = url_split._replace(scheme=ws_scheme).geturl()
    return urljoin(base_url, POSBUS_PATH)
