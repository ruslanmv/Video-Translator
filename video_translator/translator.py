"""Translation module for Video Translator.

This module provides the main VideoTranslator class that orchestrates the entire
video translation pipeline from speech recognition to translation to synthesis.
"""

from pathlib import Path
from typing import Optional

from deep_translator import GoogleTranslator

from video_translator.audio import AudioProcessor
from video_translator.config import Config
from video_translator.exceptions import TranslationError
from video_translator.logger import get_logger
from video_translator.utils import validate_video_file
from video_translator.video import VideoProcessor

logger = get_logger(__name__)


class VideoTranslator:
    """Main video translation class.

    This class orchestrates the entire video translation pipeline:
    1. Extract audio from video
    2. Convert speech to text (source language)
    3. Translate text to target language
    4. Convert translated text to speech
    5. Replace video audio with translated audio

    Attributes:
        config: Configuration object
        video_processor: VideoProcessor instance
        audio_processor: AudioProcessor instance

    Example:
        >>> translator = VideoTranslator()
        >>> output = translator.translate_video(
        ...     "video.mp4",
        ...     "English",
        ...     "Spanish"
        ... )
        >>> print(f"Translation complete: {output}")
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize VideoTranslator.

        Args:
            config: Configuration object (uses default if not provided)
        """
        self.config = config or Config()
        self.video_processor = VideoProcessor(self.config)
        self.audio_processor = AudioProcessor(self.config)
        logger.info("VideoTranslator initialized")

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language.

        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en', 'es')
            target_lang: Target language code (e.g., 'es', 'ja')

        Returns:
            Translated text string

        Raises:
            TranslationError: If translation fails

        Example:
            >>> translator = VideoTranslator()
            >>> translated = translator.translate_text(
            ...     "Hello world",
            ...     "en",
            ...     "es"
            ... )
            >>> print(translated)  # "Hola mundo"
        """
        logger.info(
            f"Translating text ({source_lang} → {target_lang}), "
            f"length: {len(text)} characters"
        )

        try:
            # Validate input
            if not text or not text.strip():
                raise TranslationError(
                    "Cannot translate empty text",
                    source_lang=source_lang,
                    target_lang=target_lang,
                )

            # Use deep_translator (more stable than googletrans)
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)

            logger.info(
                f"Translation successful. Output length: {len(translated_text)} characters"
            )
            logger.debug(f"Original: {text[:100]}...")
            logger.debug(f"Translated: {translated_text[:100]}...")

            return translated_text

        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            logger.error(error_msg)
            raise TranslationError(
                error_msg,
                source_lang=source_lang,
                target_lang=target_lang,
                original_error=e,
            )

    def translate_video(
        self,
        video_path: str,
        source_language: str,
        target_language: str,
        output_path: Optional[str] = None,
    ) -> str:
        """Translate a video from source language to target language.

        This is the main method that orchestrates the entire translation pipeline.

        Args:
            video_path: Path to the input video file
            source_language: Source language name (e.g., 'English', 'Spanish')
            target_language: Target language name (e.g., 'Spanish', 'Japanese')
            output_path: Optional custom output path (auto-generated if not provided)

        Returns:
            Path to the translated video file

        Raises:
            InvalidInputError: If input parameters are invalid
            AudioExtractionError: If audio extraction fails
            SpeechRecognitionError: If speech recognition fails
            TranslationError: If translation fails
            TextToSpeechError: If text-to-speech fails
            VideoProcessingError: If video processing fails

        Example:
            >>> translator = VideoTranslator()
            >>> output = translator.translate_video(
            ...     "obama.mp4",
            ...     "English",
            ...     "Spanish"
            ... )
            >>> print(f"Translated video saved to: {output}")
        """
        logger.info(
            f"Starting video translation: {video_path} "
            f"({source_language} → {target_language})"
        )

        # Step 1: Validate video file
        logger.info("Step 1/6: Validating video file...")
        video_file = validate_video_file(video_path, self.config)

        # Get language codes
        source_locale = self.config.get_language_locale(source_language)
        target_code = self.config.get_language_code(target_language)
        source_code = self.config.get_language_code(source_language)

        # Generate file paths
        temp_audio = self.config.get_temp_audio_path("extracted_audio")
        translated_audio = self.config.get_temp_audio_path("translated_audio")

        if output_path:
            output_video = Path(output_path)
        else:
            output_video = self.config.get_output_video_path(target_code)

        try:
            # Step 2: Extract audio from video
            logger.info("Step 2/6: Extracting audio from video...")
            self.video_processor.extract_audio(video_file, temp_audio)

            # Step 3: Convert speech to text
            logger.info("Step 3/6: Converting speech to text...")
            recognized_text = self.audio_processor.speech_to_text(temp_audio, source_locale)
            logger.info(f"Recognized text: {recognized_text[:200]}...")

            # Step 4: Translate text
            logger.info("Step 4/6: Translating text...")
            translated_text = self.translate_text(recognized_text, source_code, target_code)
            logger.info(f"Translated text: {translated_text[:200]}...")

            # Step 5: Convert translated text to speech
            logger.info("Step 5/6: Converting translated text to speech...")
            self.audio_processor.text_to_speech(
                translated_text,
                translated_audio,
                target_code,
                slow=False,
            )

            # Step 6: Replace audio in video
            logger.info("Step 6/6: Creating translated video...")
            self.video_processor.replace_audio(video_file, translated_audio, output_video)

            logger.info(f"✓ Translation completed successfully: {output_video}")
            return str(output_video)

        except Exception as e:
            logger.error(f"Translation pipeline failed: {str(e)}")
            raise

        finally:
            # Cleanup temporary files
            logger.debug("Cleaning up temporary files...")
            self.config.cleanup_temp_files()

    def batch_translate(
        self,
        video_path: str,
        source_language: str,
        target_languages: list,
    ) -> dict:
        """Translate a video to multiple target languages.

        Args:
            video_path: Path to the input video file
            source_language: Source language name
            target_languages: List of target language names

        Returns:
            Dictionary mapping language names to output video paths

        Example:
            >>> translator = VideoTranslator()
            >>> results = translator.batch_translate(
            ...     "video.mp4",
            ...     "English",
            ...     ["Spanish", "French", "German"]
            ... )
            >>> for lang, path in results.items():
            ...     print(f"{lang}: {path}")
        """
        logger.info(
            f"Starting batch translation to {len(target_languages)} languages: "
            f"{', '.join(target_languages)}"
        )

        results = {}
        for target_lang in target_languages:
            try:
                logger.info(f"Translating to {target_lang}...")
                output_path = self.translate_video(video_path, source_language, target_lang)
                results[target_lang] = output_path
                logger.info(f"✓ {target_lang} translation completed")
            except Exception as e:
                logger.error(f"✗ {target_lang} translation failed: {e}")
                results[target_lang] = None

        success_count = sum(1 for v in results.values() if v is not None)
        logger.info(
            f"Batch translation completed: {success_count}/{len(target_languages)} successful"
        )

        return results
