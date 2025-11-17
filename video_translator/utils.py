"""Utility functions for Video Translator application.

This module provides helper functions for file validation, path manipulation,
and other common operations used throughout the application.
"""

import os
from pathlib import Path
from typing import Optional

from video_translator.config import Config
from video_translator.exceptions import InvalidInputError
from video_translator.logger import get_logger

logger = get_logger(__name__)


def validate_video_file(file_path: str, config: Optional[Config] = None) -> Path:
    """Validate that a video file exists and has a supported format.

    Args:
        file_path: Path to the video file
        config: Configuration object (uses default if not provided)

    Returns:
        Path object for the validated video file

    Raises:
        InvalidInputError: If file doesn't exist or has unsupported format
        InvalidInputError: If file size exceeds maximum allowed size

    Example:
        >>> video_path = validate_video_file("/path/to/video.mp4")
        >>> print(f"Valid video: {video_path}")
    """
    if config is None:
        config = Config()

    # Convert to Path object
    path = Path(file_path)

    # Check if file exists
    if not path.exists():
        logger.error(f"Video file not found: {file_path}")
        raise InvalidInputError(f"Video file does not exist: {file_path}", parameter="file_path")

    # Check if it's a file (not a directory)
    if not path.is_file():
        logger.error(f"Path is not a file: {file_path}")
        raise InvalidInputError(f"Path is not a file: {file_path}", parameter="file_path")

    # Check file extension
    if path.suffix.lower() not in config.supported_video_formats:
        logger.error(f"Unsupported video format: {path.suffix}")
        raise InvalidInputError(
            f"Unsupported video format: {path.suffix}. "
            f"Supported formats: {', '.join(config.supported_video_formats)}",
            parameter="file_path",
        )

    # Check file size
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > config.max_file_size_mb:
        logger.error(f"File size ({file_size_mb:.2f} MB) exceeds maximum ({config.max_file_size_mb} MB)")
        raise InvalidInputError(
            f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed "
            f"size ({config.max_file_size_mb} MB)",
            parameter="file_path",
        )

    logger.info(f"Video file validated: {path} ({file_size_mb:.2f} MB)")
    return path


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing or replacing invalid characters.

    This function ensures that filenames are safe for use across different
    operating systems by removing or replacing problematic characters.

    Args:
        filename: Original filename to sanitize

    Returns:
        Sanitized filename string

    Example:
        >>> safe_name = sanitize_filename("my video (2024).mp4")
        >>> print(safe_name)  # "my_video_2024.mp4"
    """
    # Characters to remove or replace
    invalid_chars = '<>:"/\\|?*'

    # Replace invalid characters with underscores
    sanitized = "".join(c if c not in invalid_chars else "_" for c in filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")

    # Collapse multiple underscores
    while "__" in sanitized:
        sanitized = sanitized.replace("__", "_")

    logger.debug(f"Sanitized filename: '{filename}' -> '{sanitized}'")
    return sanitized


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2m 30s", "1h 5m 20s")

    Example:
        >>> duration = format_duration(150.5)
        >>> print(duration)  # "2m 30s"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def get_file_size_mb(file_path: Path) -> float:
    """Get the size of a file in megabytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in megabytes

    Raises:
        FileNotFoundError: If the file doesn't exist

    Example:
        >>> size = get_file_size_mb(Path("video.mp4"))
        >>> print(f"File size: {size:.2f} MB")
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    size_bytes = file_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    return size_mb


def ensure_directory(directory: Path) -> None:
    """Ensure that a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory

    Example:
        >>> ensure_directory(Path("output/videos"))
    """
    directory.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory}")


def cleanup_file(file_path: Path, ignore_errors: bool = True) -> bool:
    """Remove a file if it exists.

    Args:
        file_path: Path to the file to remove
        ignore_errors: If True, suppress exceptions and return False on error

    Returns:
        True if file was removed successfully, False otherwise

    Example:
        >>> cleanup_file(Path("temp_audio.wav"))
    """
    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            logger.debug(f"Removed file: {file_path}")
            return True
        return False
    except Exception as e:
        if ignore_errors:
            logger.warning(f"Failed to remove file {file_path}: {e}")
            return False
        raise
