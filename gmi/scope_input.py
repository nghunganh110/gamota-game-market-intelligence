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
                       today: date | None = None, criteria: str = '') -> list[str]:
    """Reject internally contradictory scope before Gemini search/extraction."""
    today = today or datetime.now(timezone.utc).date()
    errors = []
    if subject.strip() and _search_text(subject) not in _search_text(question):
        errors.append('Đối tượng nghiên cứu phải xuất hiện trong câu hỏi. Nếu hỏi Liên Quân Mobile, nhập chính tên game thay vì MOBA.')
    evaluative = re.search(r'\b(successful|success|promising)\b|thành công|tiềm năng|hấp dẫn', question, re.IGNORECASE)
    specified = re.search(r'xét theo|dựa trên|theo chỉ số|về (doanh thu|người chơi|lượt tải)|measured by|in terms of', question, re.IGNORECASE)
    if evaluative and not (criteria.strip() or specified):
        errors.append('Câu hỏi đánh giá cần tiêu chí cụ thể, ví dụ người chơi, doanh thu hoặc tăng trưởng. Điền ô Tiêu chí đánh giá trước khi nghiên cứu.')
    expected = quarter_bounds(period)
    if bounded and start > end:
        errors.append('Bắt đầu kỳ đo phải trước hoặc bằng kết thúc kỳ đo.')
    if bounded and expected and (start, end) != expected:
        errors.append(f'{period.strip().upper()} tương ứng {expected[0]} đến {expected[1]}; khoảng ngày đang nhập không khớp.')
    effective_end = end if bounded else expected[1] if expected else None
    if effective_end and cutoff < effective_end:
        errors.append('Ngày chốt thông tin phải sau hoặc bằng ngày kết thúc kỳ đo.')
    if cutoff > today:
        errors.append('Ngày chốt thông tin không được ở tương lai.')
    if strict and cutoff < today:
        errors.append('Nếu chọn ngày chốt trong quá khứ và yêu cầu chỉ dùng thông tin có trước ngày đó, cần bản lưu tài liệu từ thời điểm ấy. Ứng dụng hiện chưa tự tìm bản lưu lịch sử. Hãy dùng ngày chốt hôm nay để xem nguồn hiện có, hoặc chuẩn bị bản lưu phù hợp.')
    return errors


def scope_bounds(period: str, bounded: bool, start: date, end: date) -> tuple[date | None, date | None]:
    """A named calendar quarter has unambiguous inclusive bounds."""
    return (start, end) if bounded else (quarter_bounds(period) or (None, None))
