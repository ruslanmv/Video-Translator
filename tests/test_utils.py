"""Unit tests for video_translator.utils module."""

import pytest
from pathlib import Path
from video_translator.utils import (
    sanitize_filename,
    format_duration,
    validate_video_file,
)
from video_translator.exceptions import InvalidInputError


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_removes_invalid_characters(self) -> None:
        """Test that invalid characters are replaced."""
        assert sanitize_filename("file<>name.mp4") == "file__name.mp4"
        assert sanitize_filename('file:name|test.mp4') == "file_name_test.mp4"

    def test_removes_leading_trailing_spaces(self) -> None:
        """Test that leading and trailing spaces are removed."""
        assert sanitize_filename("  filename.mp4  ") == "filename.mp4"

    def test_collapses_multiple_underscores(self) -> None:
        """Test that multiple underscores are collapsed."""
        assert sanitize_filename("file___name.mp4") == "file_name.mp4"

    def test_normal_filename_unchanged(self) -> None:
        """Test that normal filenames are unchanged."""
        assert sanitize_filename("normal_filename.mp4") == "normal_filename.mp4"


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_seconds_only(self) -> None:
        """Test formatting seconds only."""
        assert format_duration(30) == "30s"
        assert format_duration(59) == "59s"

    def test_minutes_and_seconds(self) -> None:
        """Test formatting minutes and seconds."""
        assert format_duration(90) == "1m 30s"
        assert format_duration(150) == "2m 30s"

    def test_hours_minutes_seconds(self) -> None:
        """Test formatting hours, minutes, and seconds."""
        assert format_duration(3661) == "1h 1m 1s"
        assert format_duration(7265) == "2h 1m 5s"

    def test_zero_duration(self) -> None:
        """Test zero duration."""
        assert format_duration(0) == "0s"


class TestValidateVideoFile:
    """Tests for validate_video_file function."""

    def test_nonexistent_file_raises_error(self) -> None:
        """Test that nonexistent file raises error."""
        with pytest.raises(InvalidInputError, match="does not exist"):
            validate_video_file("/nonexistent/file.mp4")

    def test_unsupported_format_raises_error(self, tmp_path: Path) -> None:
        """Test that unsupported format raises error."""
        unsupported_file = tmp_path / "test.txt"
        unsupported_file.write_text("test")

        with pytest.raises(InvalidInputError, match="Unsupported video format"):
            validate_video_file(str(unsupported_file))
