import pytest
from gmi.reader import assert_public_url, parse_document

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


def test_owned_mission1_pdf_read_without_inventing_publication_date():
    from pathlib import Path
    text,title,published=parse_document(Path('docs/mission1/Mission_1_Game_Market_Intelligence.pdf').read_bytes(),'application/pdf','https://example.org/mission1.pdf')
    assert 'Publishing' in text and len(text)>100
    assert published is None
