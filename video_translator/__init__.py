"""Video Translator - A production-ready video translation application.

This package provides functionality to translate video content across multiple
languages using speech recognition, machine translation, and text-to-speech synthesis.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
__license__ = "Apache-2.0"

from video_translator.config import SUPPORTED_LANGUAGES, Config
from video_translator.exceptions import (
    AudioExtractionError,
    SpeechRecognitionError,
    TranslationError,
    VideoProcessingError,
)
from video_translator.translator import VideoTranslator

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "VideoTranslator",
    "Config",
    "SUPPORTED_LANGUAGES",
    "VideoProcessingError",
    "AudioExtractionError",
    "SpeechRecognitionError",
    "TranslationError",
]
