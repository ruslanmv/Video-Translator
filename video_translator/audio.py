"""Audio processing module for Video Translator.

This module handles all audio-related operations including extraction from video,
speech recognition, and text-to-speech synthesis.
"""

from pathlib import Path
from typing import Optional

import speech_recognition as sr
from gtts import gTTS

from video_translator.config import Config
from video_translator.exceptions import (
    AudioExtractionError,
    SpeechRecognitionError,
    TextToSpeechError,
)
from video_translator.logger import get_logger

logger = get_logger(__name__)


class AudioProcessor:
    """Audio processing class for speech recognition and synthesis.

    This class provides methods for converting speech to text and text to speech
    using Google's cloud services.

    Attributes:
        config: Configuration object
        recognizer: Speech recognition instance
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize AudioProcessor.

        Args:
            config: Configuration object (uses default if not provided)
        """
        self.config = config or Config()
        self.recognizer = sr.Recognizer()
        logger.info("AudioProcessor initialized")

    def speech_to_text(self, audio_file: Path, language_locale: str) -> str:
        """Convert speech in audio file to text.

        This method uses Google Speech Recognition API to transcribe audio
        content into text.

        Args:
            audio_file: Path to the audio file (WAV format)
            language_locale: Language locale code (e.g., 'en-US', 'es-MX')

        Returns:
            Transcribed text string

        Raises:
            SpeechRecognitionError: If speech recognition fails
            AudioExtractionError: If audio file cannot be read

        Example:
            >>> processor = AudioProcessor()
            >>> text = processor.speech_to_text(Path("audio.wav"), "en-US")
            >>> print(text)
        """
        logger.info(f"Starting speech-to-text for {audio_file} (language: {language_locale})")

        try:
            # Verify audio file exists
            if not audio_file.exists():
                raise AudioExtractionError(
                    f"Audio file not found: {audio_file}",
                    file_path=str(audio_file),
                )

            # Load audio file
            with sr.AudioFile(str(audio_file)) as source:
                logger.debug("Loading audio data into memory...")
                audio_data = self.recognizer.record(source)

                logger.debug(f"Recognizing speech (language: {language_locale})...")
                text = self.recognizer.recognize_google(audio_data, language=language_locale)

                logger.info(f"Speech recognition successful. Text length: {len(text)} characters")
                return text

        except sr.UnknownValueError as e:
            error_msg = "Speech recognition could not understand the audio"
            logger.error(f"{error_msg}: {e}")
            raise SpeechRecognitionError(
                error_msg,
                language=language_locale,
                original_error=e,
            )
        except sr.RequestError as e:
            error_msg = "Could not request results from Speech Recognition service"
            logger.error(f"{error_msg}: {e}")
            raise SpeechRecognitionError(
                error_msg,
                language=language_locale,
                original_error=e,
            )
        except Exception as e:
            error_msg = f"Unexpected error during speech recognition: {str(e)}"
            logger.error(error_msg)
            raise SpeechRecognitionError(
                error_msg,
                language=language_locale,
                original_error=e,
            )

    def text_to_speech(
        self,
        text: str,
        output_file: Path,
        language_code: str,
        slow: bool = False,
    ) -> Path:
        """Convert text to speech and save as audio file.

        This method uses Google Text-to-Speech (gTTS) to generate audio
        from text in the specified language.

        Args:
            text: Text to convert to speech
            output_file: Path where the audio file will be saved
            language_code: Language code (e.g., 'en', 'es', 'ja')
            slow: If True, speech will be slower (default: False)

        Returns:
            Path to the generated audio file

        Raises:
            TextToSpeechError: If text-to-speech conversion fails

        Example:
            >>> processor = AudioProcessor()
            >>> audio_path = processor.text_to_speech(
            ...     "Hello world",
            ...     Path("output.wav"),
            ...     "en"
            ... )
        """
        logger.info(
            f"Starting text-to-speech (language: {language_code}, "
            f"text length: {len(text)} characters)"
        )

        try:
            # Validate input
            if not text or not text.strip():
                raise TextToSpeechError(
                    "Cannot convert empty text to speech",
                    language=language_code,
                )

            # Create gTTS object
            logger.debug("Creating gTTS object...")
            tts = gTTS(text=text, lang=language_code, slow=slow)

            # Save to file
            logger.debug(f"Saving audio to {output_file}...")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            tts.save(str(output_file))

            # Verify file was created
            if not output_file.exists():
                raise TextToSpeechError(
                    f"Audio file was not created: {output_file}",
                    language=language_code,
                )

            logger.info(f"Text-to-speech completed successfully: {output_file}")
            return output_file

        except TextToSpeechError:
            raise
        except Exception as e:
            error_msg = f"Failed to convert text to speech: {str(e)}"
            logger.error(error_msg)
            raise TextToSpeechError(
                error_msg,
                language=language_code,
                original_error=e,
            )

    def adjust_audio_speed(self, audio_file: Path, speed: float = 1.0) -> Path:
        """Adjust the playback speed of an audio file.

        Note: This is a placeholder for future implementation using pydub.
        Currently returns the original file unchanged.

        Args:
            audio_file: Path to the audio file
            speed: Speed multiplier (1.0 = normal, 2.0 = 2x speed, 0.5 = half speed)

        Returns:
            Path to the processed audio file

        Example:
            >>> processor = AudioProcessor()
            >>> faster_audio = processor.adjust_audio_speed(Path("audio.wav"), 1.5)
        """
        logger.info(f"Audio speed adjustment requested: {speed}x (not yet implemented)")
        # Future implementation with pydub:
        # from pydub import AudioSegment
        # audio = AudioSegment.from_file(audio_file)
        # adjusted = audio.speedup(playback_speed=speed)
        # adjusted.export(audio_file, format="wav")
        return audio_file
