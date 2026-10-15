import pytest
from gmi.reader import assert_public_url, parse_document, safe_read_error

@pytest.mark.parametrize('url',['http://127.0.0.1/private','http://169.254.169.254/latest','file:///etc/passwd','https://user:pass@example.org','http://[::1]/','https://example.org:22/'])
def test_private_or_credential_urls_blocked(url):
    with pytest.raises(ValueError): assert_public_url(url)


def test_html_full_text_extraction():
    html=b'<html><head><title>Synthetic source</title><meta property="article:published_time" content="2025-03-01"/></head><body><article><h1>Synthetic research</h1><p>This invented document describes demand research for a fictional mobile game. It contains readable body text so that extraction can be tested without network access or search snippets. All statements are synthetic test data.</p></article></body></html>'
    text,title,published=parse_document(html,'text/html','https://example.org')
    assert 'invented document' in text and title=='Synthetic research'
    assert str(published)=='2025-03-01'


def test_empty_scan_and_unsupported_types_fail():
    with pytest.raises(ValueError): parse_document(b'<html><body>JS app</body></html>','text/html','https://example.org')
    with pytest.raises(ValueError): parse_document(b'not readable','application/octet-stream','https://example.org')


def test_reader_error_detail_is_actionable_but_does_not_leak_arbitrary_text():
    import httpx
    request = httpx.Request('GET', 'https://example.org/private-token')
    response = httpx.Response(403, request=request)
    assert safe_read_error(httpx.HTTPStatusError('secret response', request=request, response=response)) == 'HTTP 403'
    assert safe_read_error(ValueError('No readable full text (scan, paywall or JS page possible)')).startswith('No readable')
    assert safe_read_error(ValueError('secret source text')) == 'ValueError'


def test_navigation_shell_is_not_readable_article():
    menu = ''.join(f'<li><a href="/{i}">{label}</a></li>' for i, label in enumerate([
        'About NEXON', 'Corporate Profile', 'Leadership', 'Location', 'History',
        'Products', 'Popular Games in Service', 'Pipeline', 'Investor Relations',
        'Stock Information', 'Our Business', 'Quarterly Disclosure', 'IR News',
        'Events and Interviews', 'Careers', 'Sustainability', 'News', 'Video Archive']))
    html = f'<html><head><title>News</title></head><body><nav><ul>{menu}</ul></nav><main><h1>NEWS</h1></main><footer>{menu}</footer></body></html>'
    with pytest.raises(ValueError):
        parse_document(html.encode(), 'text/html', 'https://example.org/news')


def test_owned_mission1_pdf_read_without_inventing_publication_date():
    from pathlib import Path
    text,title,published=parse_document(Path('docs/mission1/Mission_1_Game_Market_Intelligence.pdf').read_bytes(),'application/pdf','https://example.org/mission1.pdf')
    assert 'Publishing' in text and len(text)>100
    assert published is None
