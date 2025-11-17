"""Configuration module for Video Translator application.

This module contains all configuration settings, constants, and language mappings
used throughout the application.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# Supported languages with their locale codes
LANGUAGE_LOCALE_MAP: Dict[str, str] = {
    "English": "en-US",
    "Italian": "it-IT",
    "Spanish": "es-MX",
    "Russian": "ru-RU",
    "German": "de-DE",
    "Japanese": "ja-JP",
    "Portuguese": "pt-BR",
}

# Language codes for translation (ISO 639-1)
LANGUAGE_CODE_MAP: Dict[str, str] = {
    "English": "en",
    "Italian": "it",
    "Spanish": "es",
    "Russian": "ru",
    "German": "de",
    "Japanese": "ja",
    "Portuguese": "pt",
}

# Supported languages list
SUPPORTED_LANGUAGES: List[str] = list(LANGUAGE_LOCALE_MAP.keys())


@dataclass
class Config:
    """Application configuration class.

    This class holds all configuration parameters for the video translation
    application including paths, file formats, and processing settings.

    Attributes:
        temp_dir: Directory for temporary files
        output_dir: Directory for output files
        audio_format: Audio file format for intermediate processing
        video_format: Video file format for output
        audio_codec: Audio codec for extraction
        max_file_size_mb: Maximum allowed file size in MB
        supported_video_formats: List of supported input video formats
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    temp_dir: Path = field(default_factory=lambda: Path("temp"))
    output_dir: Path = field(default_factory=lambda: Path("output"))
    audio_format: str = "wav"
    video_format: str = "mp4"
    audio_codec: str = "pcm_s16le"
    max_file_size_mb: int = 500
    supported_video_formats: List[str] = field(
        default_factory=lambda: [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"]
    )
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Initialize directories after dataclass initialization."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_temp_audio_path(self, filename: str = "temp_audio") -> Path:
        """Generate a temporary audio file path.

        Args:
            filename: Base filename without extension

        Returns:
            Path object for the temporary audio file
        """
        return self.temp_dir / f"{filename}.{self.audio_format}"

    def get_output_video_path(self, language_code: str, prefix: str = "video_translated") -> Path:
        """Generate an output video file path.

        Args:
            language_code: Target language code (e.g., 'en', 'es')
            prefix: Prefix for the output filename

        Returns:
            Path object for the output video file
        """
        return self.output_dir / f"{prefix}_{language_code}.{self.video_format}"

    def cleanup_temp_files(self) -> None:
        """Remove all temporary files from the temp directory."""
        if self.temp_dir.exists():
            for file in self.temp_dir.glob("*"):
                try:
                    if file.is_file():
                        file.unlink()
                except Exception:
                    pass  # Ignore cleanup errors

    @staticmethod
    def get_language_locale(language: str) -> str:
        """Get the locale code for a given language.

        Args:
            language: Language name (e.g., 'English', 'Spanish')

        Returns:
            Locale code (e.g., 'en-US', 'es-MX')

        Raises:
            ValueError: If language is not supported
        """
        if language not in LANGUAGE_LOCALE_MAP:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported languages: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        return LANGUAGE_LOCALE_MAP[language]

    @staticmethod
    def get_language_code(language: str) -> str:
        """Get the ISO 639-1 language code for a given language.

        Args:
            language: Language name (e.g., 'English', 'Spanish')

        Returns:
            ISO 639-1 language code (e.g., 'en', 'es')

        Raises:
            ValueError: If language is not supported
        """
        if language not in LANGUAGE_CODE_MAP:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported languages: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        return LANGUAGE_CODE_MAP[language]
