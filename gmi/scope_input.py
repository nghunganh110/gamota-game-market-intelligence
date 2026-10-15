"""Cheap live-scope checks before any billable provider call."""
import re
import unicodedata
from calendar import monthrange
from datetime import date, datetime, timezone


def quarter_bounds(period: str) -> tuple[date, date] | None:
    match = re.fullmatch(r'Q([1-4])\s+(\d{4})', period.strip(), flags=re.IGNORECASE)
    if not match:
        return None
    quarter, year = int(match.group(1)), int(match.group(2))
    if year < 1:
        return None
    first_month = (quarter - 1) * 3 + 1
    last_month = first_month + 2
    return date(year, first_month, 1), date(year, last_month, monthrange(year, last_month)[1])


def _search_text(value: str) -> str:
    normalized = unicodedata.normalize('NFKD', value.casefold().replace('đ', 'd'))
    return ' '.join(''.join(char for char in normalized if not unicodedata.combining(char)).split())


def scope_input_errors(question: str, subject: str, period: str, bounded: bool,
                       start: date, end: date, cutoff: date, strict: bool,
                       today: date | None = None) -> list[str]:
    """Reject internally contradictory scope before Gemini search/extraction."""
    today = today or datetime.now(timezone.utc).date()
    errors = []
    if subject.strip() and _search_text(subject) not in _search_text(question):
        errors.append('Đối tượng nghiên cứu phải xuất hiện trong câu hỏi. Nếu hỏi Liên Quân Mobile, nhập chính tên game thay vì MOBA.')
    expected = quarter_bounds(period)
    if bounded and start > end:
        errors.append('Bắt đầu kỳ đo phải trước hoặc bằng kết thúc kỳ đo.')
    if bounded and expected and (start, end) != expected:
        errors.append(f'{period.strip().upper()} tương ứng {expected[0]} đến {expected[1]}; khoảng ngày đang nhập không khớp.')
    effective_end = end if bounded else expected[1] if expected else None
    if effective_end and cutoff < effective_end:
        errors.append('Cutoff phải sau hoặc bằng ngày kết thúc kỳ đo.')
    if cutoff > today:
        errors.append('Cutoff không được ở tương lai.')
    if strict and cutoff < today:
        errors.append('Cutoff lịch sử + strict cần snapshot lưu trước cutoff; reader live hiện không lấy archive. Dùng cutoff hôm nay để phân tích hồi cứu từ nguồn hiện có, hoặc chuẩn bị snapshot lịch sử.')
    return errors


def scope_bounds(period: str, bounded: bool, start: date, end: date) -> tuple[date | None, date | None]:
    """A named calendar quarter has unambiguous inclusive bounds."""
    return (start, end) if bounded else (quarter_bounds(period) or (None, None))
