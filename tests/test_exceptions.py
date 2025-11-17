"""Unit tests for video_translator.exceptions module."""

import pytest
from video_translator.exceptions import (
    VideoTranslatorError,
    VideoProcessingError,
    AudioExtractionError,
    SpeechRecognitionError,
    TranslationError,
    TextToSpeechError,
    InvalidInputError,
)


class TestExceptions:
    """Tests for custom exception classes."""

    def test_base_exception(self) -> None:
        """Test base exception."""
        exc = VideoTranslatorError("Base error")
        assert str(exc) == "Base error"
        assert isinstance(exc, Exception)

    def test_video_processing_error(self) -> None:
        """Test VideoProcessingError."""
        original = ValueError("Original error")
        exc = VideoProcessingError("Processing failed", original_error=original)
        assert str(exc) == "Processing failed"
        assert exc.original_error == original

    def test_audio_extraction_error(self) -> None:
        """Test AudioExtractionError with file path."""
        exc = AudioExtractionError("Extraction failed", file_path="/path/to/video.mp4")
        assert "/path/to/video.mp4" in str(exc)

    def test_speech_recognition_error(self) -> None:
        """Test SpeechRecognitionError with language."""
        exc = SpeechRecognitionError("Recognition failed", language="en-US")
        assert "en-US" in str(exc)

    def test_translation_error(self) -> None:
        """Test TranslationError with languages."""
        exc = TranslationError("Translation failed", source_lang="en", target_lang="es")
        assert "en" in str(exc)
        assert "es" in str(exc)

    def test_text_to_speech_error(self) -> None:
        """Test TextToSpeechError."""
        exc = TextToSpeechError("TTS failed", language="ja")
        assert "ja" in str(exc)

    def test_invalid_input_error(self) -> None:
        """Test InvalidInputError with parameter."""
        exc = InvalidInputError("Invalid input", parameter="video_path")
        assert "video_path" in str(exc)
