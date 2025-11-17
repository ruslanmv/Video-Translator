"""Custom exceptions for Video Translator application.

This module defines all custom exception classes used throughout the application
for better error handling and debugging.
"""


class VideoTranslatorError(Exception):
    """Base exception class for all Video Translator errors.

    All custom exceptions in this application inherit from this base class,
    allowing for easy catching of all application-specific errors.
    """

    pass


class VideoProcessingError(VideoTranslatorError):
    """Exception raised for errors during video processing.

    This exception is raised when there are issues with video file operations
    such as reading, writing, or format conversions.

    Attributes:
        message: Explanation of the error
        original_error: The original exception that caused this error (optional)
    """

    def __init__(self, message: str, original_error: Exception = None) -> None:
        """Initialize VideoProcessingError.

        Args:
            message: Human-readable error description
            original_error: The underlying exception that caused this error
        """
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class AudioExtractionError(VideoTranslatorError):
    """Exception raised for errors during audio extraction from video.

    This exception is raised when the application fails to extract audio
    from a video file, which may be due to codec issues, corrupted files,
    or missing dependencies.

    Attributes:
        message: Explanation of the error
        file_path: Path to the video file that failed
        original_error: The original exception that caused this error (optional)
    """

    def __init__(self, message: str, file_path: str = None, original_error: Exception = None) -> None:
        """Initialize AudioExtractionError.

        Args:
            message: Human-readable error description
            file_path: Path to the problematic video file
            original_error: The underlying exception that caused this error
        """
        self.message = message
        self.file_path = file_path
        self.original_error = original_error
        full_message = f"{message}"
        if file_path:
            full_message += f" (File: {file_path})"
        super().__init__(full_message)


class SpeechRecognitionError(VideoTranslatorError):
    """Exception raised for errors during speech-to-text recognition.

    This exception is raised when the speech recognition service fails to
    transcribe audio, which may be due to poor audio quality, unsupported
    languages, or API failures.

    Attributes:
        message: Explanation of the error
        language: Language code that was being recognized
        original_error: The original exception that caused this error (optional)
    """

    def __init__(self, message: str, language: str = None, original_error: Exception = None) -> None:
        """Initialize SpeechRecognitionError.

        Args:
            message: Human-readable error description
            language: Language code that was being processed
            original_error: The underlying exception that caused this error
        """
        self.message = message
        self.language = language
        self.original_error = original_error
        full_message = f"{message}"
        if language:
            full_message += f" (Language: {language})"
        super().__init__(full_message)


class TranslationError(VideoTranslatorError):
    """Exception raised for errors during text translation.

    This exception is raised when the translation service fails to translate
    text from the source language to the target language.

    Attributes:
        message: Explanation of the error
        source_lang: Source language code
        target_lang: Target language code
        original_error: The original exception that caused this error (optional)
    """

    def __init__(
        self,
        message: str,
        source_lang: str = None,
        target_lang: str = None,
        original_error: Exception = None,
    ) -> None:
        """Initialize TranslationError.

        Args:
            message: Human-readable error description
            source_lang: Source language code
            target_lang: Target language code
            original_error: The underlying exception that caused this error
        """
        self.message = message
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.original_error = original_error
        full_message = f"{message}"
        if source_lang and target_lang:
            full_message += f" ({source_lang} → {target_lang})"
        super().__init__(full_message)


class TextToSpeechError(VideoTranslatorError):
    """Exception raised for errors during text-to-speech synthesis.

    This exception is raised when the text-to-speech service fails to generate
    audio from the translated text.

    Attributes:
        message: Explanation of the error
        language: Target language code
        original_error: The original exception that caused this error (optional)
    """

    def __init__(self, message: str, language: str = None, original_error: Exception = None) -> None:
        """Initialize TextToSpeechError.

        Args:
            message: Human-readable error description
            language: Language code for speech synthesis
            original_error: The underlying exception that caused this error
        """
        self.message = message
        self.language = language
        self.original_error = original_error
        full_message = f"{message}"
        if language:
            full_message += f" (Language: {language})"
        super().__init__(full_message)


class InvalidInputError(VideoTranslatorError):
    """Exception raised for invalid input parameters.

    This exception is raised when the application receives invalid input
    such as unsupported file formats, invalid language codes, or malformed data.

    Attributes:
        message: Explanation of the error
        parameter: Name of the invalid parameter
    """

    def __init__(self, message: str, parameter: str = None) -> None:
        """Initialize InvalidInputError.

        Args:
            message: Human-readable error description
            parameter: Name of the parameter that was invalid
        """
        self.message = message
        self.parameter = parameter
        full_message = f"{message}"
        if parameter:
            full_message += f" (Parameter: {parameter})"
        super().__init__(full_message)
