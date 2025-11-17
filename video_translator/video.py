"""Video processing module for Video Translator.

This module handles all video-related operations including audio extraction,
audio replacement, and video file manipulation.
"""

from pathlib import Path
from typing import Optional

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip

from video_translator.config import Config
from video_translator.exceptions import AudioExtractionError, VideoProcessingError
from video_translator.logger import get_logger

logger = get_logger(__name__)


class VideoProcessor:
    """Video processing class for handling video file operations.

    This class provides methods for extracting audio from video, replacing
    audio tracks, and creating new video files with translated audio.

    Attributes:
        config: Configuration object
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize VideoProcessor.

        Args:
            config: Configuration object (uses default if not provided)
        """
        self.config = config or Config()
        logger.info("VideoProcessor initialized")

    def extract_audio(self, video_file: Path, output_audio: Path) -> Path:
        """Extract audio from a video file.

        Args:
            video_file: Path to the input video file
            output_audio: Path where the extracted audio will be saved

        Returns:
            Path to the extracted audio file

        Raises:
            AudioExtractionError: If audio extraction fails
            VideoProcessingError: If video file cannot be processed

        Example:
            >>> processor = VideoProcessor()
            >>> audio_path = processor.extract_audio(
            ...     Path("video.mp4"),
            ...     Path("audio.wav")
            ... )
        """
        logger.info(f"Extracting audio from {video_file} to {output_audio}")
        video_clip = None

        try:
            # Load video file
            logger.debug("Loading video file...")
            video_clip = VideoFileClip(str(video_file))

            # Check if video has audio
            if video_clip.audio is None:
                raise AudioExtractionError(
                    "Video file does not contain an audio track",
                    file_path=str(video_file),
                )

            # Create output directory if needed
            output_audio.parent.mkdir(parents=True, exist_ok=True)

            # Extract audio
            logger.debug(f"Writing audio to {output_audio} with codec {self.config.audio_codec}...")
            video_clip.audio.write_audiofile(
                str(output_audio),
                codec=self.config.audio_codec,
                logger=None,  # Suppress moviepy's verbose output
            )

            # Verify audio file was created
            if not output_audio.exists():
                raise AudioExtractionError(
                    f"Audio file was not created: {output_audio}",
                    file_path=str(video_file),
                )

            logger.info(f"Audio extraction completed: {output_audio}")
            return output_audio

        except AudioExtractionError:
            raise
        except Exception as e:
            error_msg = f"Failed to extract audio from video: {str(e)}"
            logger.error(error_msg)
            raise AudioExtractionError(
                error_msg,
                file_path=str(video_file),
                original_error=e,
            )
        finally:
            # Clean up video clip
            if video_clip is not None:
                try:
                    video_clip.close()
                except Exception as e:
                    logger.warning(f"Error closing video clip: {e}")

    def replace_audio(
        self,
        video_file: Path,
        new_audio: Path,
        output_video: Path,
    ) -> Path:
        """Replace the audio track in a video file.

        Args:
            video_file: Path to the original video file
            new_audio: Path to the new audio file
            output_video: Path where the output video will be saved

        Returns:
            Path to the output video file

        Raises:
            VideoProcessingError: If video processing fails

        Example:
            >>> processor = VideoProcessor()
            >>> output = processor.replace_audio(
            ...     Path("original.mp4"),
            ...     Path("translated_audio.wav"),
            ...     Path("translated.mp4")
            ... )
        """
        logger.info(f"Replacing audio in {video_file} with {new_audio}")
        video_clip = None
        audio_clip = None

        try:
            # Load video file
            logger.debug("Loading video file...")
            video_clip = VideoFileClip(str(video_file))

            # Load new audio file
            logger.debug("Loading new audio file...")
            audio_clip = AudioFileClip(str(new_audio))

            # Create composite audio (replace original audio)
            logger.debug("Creating composite audio...")
            new_audio_clip = CompositeAudioClip([audio_clip])
            video_clip.audio = new_audio_clip

            # Create output directory if needed
            output_video.parent.mkdir(parents=True, exist_ok=True)

            # Write output video
            logger.debug(f"Writing output video to {output_video}...")
            video_clip.write_videofile(
                str(output_video),
                codec="libx264",
                audio_codec="aac",
                logger=None,  # Suppress moviepy's verbose output
            )

            # Verify output file was created
            if not output_video.exists():
                raise VideoProcessingError(
                    f"Output video file was not created: {output_video}"
                )

            logger.info(f"Audio replacement completed: {output_video}")
            return output_video

        except VideoProcessingError:
            raise
        except Exception as e:
            error_msg = f"Failed to replace audio in video: {str(e)}"
            logger.error(error_msg)
            raise VideoProcessingError(error_msg, original_error=e)
        finally:
            # Clean up clips
            if audio_clip is not None:
                try:
                    audio_clip.close()
                except Exception as e:
                    logger.warning(f"Error closing audio clip: {e}")
            if video_clip is not None:
                try:
                    video_clip.close()
                except Exception as e:
                    logger.warning(f"Error closing video clip: {e}")

    def get_video_duration(self, video_file: Path) -> float:
        """Get the duration of a video file in seconds.

        Args:
            video_file: Path to the video file

        Returns:
            Duration in seconds

        Raises:
            VideoProcessingError: If video cannot be read

        Example:
            >>> processor = VideoProcessor()
            >>> duration = processor.get_video_duration(Path("video.mp4"))
            >>> print(f"Duration: {duration:.2f} seconds")
        """
        logger.debug(f"Getting duration of {video_file}")
        video_clip = None

        try:
            video_clip = VideoFileClip(str(video_file))
            duration = video_clip.duration
            logger.debug(f"Video duration: {duration:.2f} seconds")
            return duration

        except Exception as e:
            error_msg = f"Failed to get video duration: {str(e)}"
            logger.error(error_msg)
            raise VideoProcessingError(error_msg, original_error=e)
        finally:
            if video_clip is not None:
                try:
                    video_clip.close()
                except Exception as e:
                    logger.warning(f"Error closing video clip: {e}")

    def get_video_info(self, video_file: Path) -> dict:
        """Get information about a video file.

        Args:
            video_file: Path to the video file

        Returns:
            Dictionary with video information (duration, fps, size, has_audio)

        Raises:
            VideoProcessingError: If video cannot be read

        Example:
            >>> processor = VideoProcessor()
            >>> info = processor.get_video_info(Path("video.mp4"))
            >>> print(f"Duration: {info['duration']}s, FPS: {info['fps']}")
        """
        logger.debug(f"Getting info for {video_file}")
        video_clip = None

        try:
            video_clip = VideoFileClip(str(video_file))
            info = {
                "duration": video_clip.duration,
                "fps": video_clip.fps,
                "size": video_clip.size,
                "has_audio": video_clip.audio is not None,
            }
            logger.debug(f"Video info: {info}")
            return info

        except Exception as e:
            error_msg = f"Failed to get video info: {str(e)}"
            logger.error(error_msg)
            raise VideoProcessingError(error_msg, original_error=e)
        finally:
            if video_clip is not None:
                try:
                    video_clip.close()
                except Exception as e:
                    logger.warning(f"Error closing video clip: {e}")
