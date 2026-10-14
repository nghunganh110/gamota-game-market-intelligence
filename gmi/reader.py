"""Bounded public-document reader. No browser, OCR, paywall bypass or JS rendering."""
import hashlib
import ipaddress
import socket
import time
from datetime import date, datetime, timezone
from io import BytesIO
from urllib.parse import urlsplit, urljoin
import httpx
from .models import Source

MAX_BYTES = 4_000_000
MAX_CHARS = 30_000


def assert_public_url(url: str):
    p = urlsplit(url)
    if p.scheme not in {'https', 'http'} or not p.hostname or p.username or p.password or p.port not in {None, 80, 443}:
        raise ValueError('Only public HTTP(S) URLs without credentials are allowed')
    addresses = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Private/reserved address blocked')


def parse_document(data: bytes, content_type: str, url: str):
    if 'pdf' in content_type or data.startswith(b'%PDF'):
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        if len(reader.pages) > 50:
            raise ValueError('PDF exceeds 50-page limit')
        text = '\n'.join(p.extract_text() or '' for p in reader.pages)
        title = str((reader.metadata or {}).get('/Title') or urlsplit(url).hostname)
        published = None  # PDF creation time is not a reliable publication date.
    elif 'html' in content_type:
        from trafilatura import extract
        from trafilatura.metadata import extract_metadata
        html = data.decode('utf-8', errors='replace')
        text = extract(html, include_comments=False, include_tables=True) or ''
        meta = extract_metadata(html, default_url=url)
        title = meta.title if meta and meta.title else urlsplit(url).hostname
        try:
            published = date.fromisoformat(meta.date[:10]) if meta and meta.date else None
        except ValueError:
            published = None
    else:
        raise ValueError('Unsupported content type')
    if len(text.strip()) < 100:
        raise ValueError('No readable full text (scan, paywall or JS page possible)')
    return text[:MAX_CHARS], title, published


class DocumentReader:
    def read(self, url: str, source_id: str) -> Source:
        accessed = datetime.now(timezone.utc)
        try:
            current = url
            started = time.monotonic()
            with httpx.Client(timeout=15, follow_redirects=False, trust_env=False) as client:
                for _ in range(5):
                    assert_public_url(current)
                    with client.stream('GET', current, headers={'User-Agent': 'GamotaResearchMVP/0.1'}) as response:
                        if response.is_redirect:
                            current = urljoin(current, response.headers['location'])
                            continue
                        response.raise_for_status()
                        chunks, size = [], 0
                        for chunk in response.iter_bytes():
                            size += len(chunk)
                            if size > MAX_BYTES or time.monotonic() - started > 30:
                                raise ValueError('Document exceeded size/time limit')
                            chunks.append(chunk)
                        text, title, published = parse_document(b''.join(chunks), response.headers.get('content-type',''), current)
                        return Source(id=source_id, url=current, title=title, text=text, published=published,
                                      accessed=accessed, sha256=hashlib.sha256(text.encode()).hexdigest())
                raise ValueError('Too many redirects')
        except Exception as exc:
            # Never persist arbitrary exception bodies/headers that might include credentials.
            return Source(id=source_id, url=url, title=urlsplit(url).hostname or 'Unreadable source',
                          text='', accessed=accessed, read_status='failed', error=f'Document read failed ({type(exc).__name__})')
