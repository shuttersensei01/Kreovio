from datetime import UTC

from app.core.clock import SystemClock


def test_system_clock_returns_utc_datetime() -> None:
    assert SystemClock().now().tzinfo is UTC

