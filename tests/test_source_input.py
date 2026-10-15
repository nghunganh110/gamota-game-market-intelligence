import pytest
from gmi.source_input import parse_source_urls


def test_reviewer_urls_are_bounded_before_any_billable_call():
    assert parse_source_urls('https://example.org/a\nhttps://example.org/b') == [
        'https://example.org/a', 'https://example.org/b']
    for raw in ['', 'https://example.org/a\nhttps://example.org/a',
                '\n'.join(f'https://example.org/{n}' for n in range(7)),
                'https://user:password@example.org/report',
                'file:///etc/passwd', 'https://example.org:9999/report']:
        with pytest.raises(ValueError):
            parse_source_urls(raw)
