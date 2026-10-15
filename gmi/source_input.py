"""Validate optional reviewer-supplied public document URLs before a live run."""
from urllib.parse import urlsplit


def parse_source_urls(raw: str) -> list[str]:
    urls = [line.strip() for line in raw.splitlines() if line.strip()]
    if not urls or len(urls) > 6:
        raise ValueError('Nhập từ 1 đến 6 URL nguồn, mỗi dòng một URL.')
    if len(set(urls)) != len(urls):
        raise ValueError('Danh sách nguồn có URL trùng nhau.')
    for url in urls:
        parts = urlsplit(url)
        try:
            port = parts.port
        except ValueError as exc:
            raise ValueError('URL nguồn có cổng không hợp lệ.') from exc
        if (parts.scheme not in {'https', 'http'} or not parts.hostname
                or parts.username or parts.password or port not in {None, 80, 443}
                or any(char.isspace() for char in url)):
            raise ValueError('Chỉ nhận URL HTTP(S) công khai, không có thông tin đăng nhập.')
    return urls
