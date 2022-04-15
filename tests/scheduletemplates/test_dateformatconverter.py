import pytest

from scheduletemplates.admin import translate_date_format


@pytest.mark.parametrize(
    "date_format,expected",
    [
        ("%Y-%m-%d", "yy-mm-dd"),
        ("%m/%d/%Y", "mm/dd/yy"),
        ("%m/%d/%y", "mm/dd/y"),
        ("%b %d %Y", "M dd yy"),
        ("%b %d, %Y", "M dd, yy"),
        ("%d %b %Y", "dd M yy"),
        ("%d %b, %Y", "dd M, yy"),
        ("%B %d %Y", "MM dd yy"),
        ("%B %d, %Y", "MM dd, yy"),
        ("%d %B %Y", "dd MM yy"),
        ("%d %B, %Y", "dd MM, yy"),
    ],
)
def test_translate_date_format(date_format, expected):
    assert translate_date_format(date_format) == expected
