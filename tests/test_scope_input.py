from datetime import date

from gmi.scope_input import quarter_bounds, scope_bounds, scope_input_errors


def test_calendar_quarter_uses_correct_inclusive_bounds_without_manual_dates():
    expected = (date(2025, 1, 1), date(2025, 3, 31))
    assert quarter_bounds('q1 2025') == expected
    assert scope_bounds('Q1 2025', False, date(2025, 10, 1), date(2025, 12, 31)) == expected
    assert quarter_bounds('launch window') is None
    assert quarter_bounds('Q1 0000') is None


def test_online_user_scope_errors_are_caught_before_api_calls():
    errors = scope_input_errors(
        question='Liên Quân Mobile có phải 1 game thành công',
        subject='MOBA', period='Q1 2025', bounded=True,
        start=date(2025, 10, 1), end=date(2025, 12, 31),
        cutoff=date(2025, 12, 31), strict=True,
        today=date(2026, 10, 15),
    )
    assert len(errors) == 3
    assert any('Đối tượng' in error for error in errors)
    assert any('2025-01-01 đến 2025-03-31' in error for error in errors)
    assert any('snapshot lịch sử' in error for error in errors)


def test_current_retrospective_scope_is_allowed_with_auto_quarter_bounds():
    assert scope_input_errors(
        question='Liên Quân Mobile có thành công tại Việt Nam trong Q1 2025?',
        subject='Liên Quân Mobile', period='Q1 2025', bounded=False,
        start=date(2025, 10, 1), end=date(2025, 12, 31),
        cutoff=date(2026, 10, 15), strict=True,
        today=date(2026, 10, 15),
    ) == []


def test_cutoff_before_end_of_period_is_rejected():
    errors = scope_input_errors(
        question='Liên Quân Mobile tại Việt Nam trong Q1 2025 có thành công?',
        subject='Liên Quân Mobile', period='Q1 2025', bounded=False,
        start=date(2025, 10, 1), end=date(2025, 12, 31),
        cutoff=date(2025, 1, 31), strict=False,
        today=date(2026, 10, 15),
    )
    assert any('ngày kết thúc kỳ đo' in error for error in errors)
