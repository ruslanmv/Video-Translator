"""Unit tests for video_translator.config module."""

import pytest
from pathlib import Path
from video_translator.config import Config, SUPPORTED_LANGUAGES


class TestConfig:
    """Tests for Config class."""

    def test_default_initialization(self) -> None:
        """Test that Config initializes with default values."""
        config = Config()
        assert config.audio_format == "wav"
        assert config.video_format == "mp4"
        assert config.audio_codec == "pcm_s16le"
        assert config.max_file_size_mb == 500

    def test_directories_created(self, tmp_path: Path) -> None:
        """Test that directories are created on initialization."""
        temp_dir = tmp_path / "temp"
        output_dir = tmp_path / "output"

        config = Config(temp_dir=temp_dir, output_dir=output_dir)

        assert temp_dir.exists()
        assert output_dir.exists()

    def test_get_language_locale(self) -> None:
        """Test language locale retrieval."""
        assert Config.get_language_locale("English") == "en-US"
        assert Config.get_language_locale("Spanish") == "es-MX"
        assert Config.get_language_locale("Japanese") == "ja-JP"

    def test_get_language_locale_invalid(self) -> None:
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language"):
            Config.get_language_locale("Klingon")

    def test_get_language_code(self) -> None:
        """Test language code retrieval."""
        assert Config.get_language_code("English") == "en"
        assert Config.get_language_code("Spanish") == "es"
        assert Config.get_language_code("Japanese") == "ja"

    def test_get_language_code_invalid(self) -> None:
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language"):
            Config.get_language_code("Elvish")

    def test_supported_languages(self) -> None:
        """Test that all expected languages are supported."""
        expected = ["English", "Italian", "Spanish", "Russian", "German", "Japanese", "Portuguese"]
        assert all(lang in SUPPORTED_LANGUAGES for lang in expected)
