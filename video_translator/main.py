"""Main entry point for Video Translator Gradio application.

This module provides the web interface for the Video Translator application
using Gradio for easy user interaction.
"""

import sys
from pathlib import Path
from typing import Optional

import gradio as gr

from video_translator import __version__
from video_translator.config import SUPPORTED_LANGUAGES, Config
from video_translator.logger import get_logger, setup_logger
from video_translator.translator import VideoTranslator

# Setup logging
logger = get_logger(__name__)


def translate_video_wrapper(
    video_file: gr.File,
    source_language: str,
    target_language: str,
    progress: gr.Progress = gr.Progress(),
) -> Optional[str]:
    """Wrapper function for Gradio interface to translate videos.

    This function wraps the VideoTranslator for use with Gradio, providing
    progress updates and error handling for the web interface.

    Args:
        video_file: Uploaded video file from Gradio
        source_language: Source language name
        target_language: Target language name
        progress: Gradio progress tracker

    Returns:
        Path to the translated video file, or None if translation fails
    """
    try:
        logger.info(
            f"Translation request received: {source_language} → {target_language}"
        )

        # Update progress
        progress(0, desc="Initializing...")

        # Validate inputs
        if video_file is None:
            logger.error("No video file provided")
            gr.Warning("Please upload a video file")
            return None

        if source_language == target_language:
            logger.warning("Source and target languages are the same")
            gr.Warning("Source and target languages must be different")
            return None

        # Initialize translator
        config = Config()
        translator = VideoTranslator(config)

        # Extract video path
        video_path = video_file.name if hasattr(video_file, "name") else str(video_file)
        logger.info(f"Processing video: {video_path}")

        # Update progress
        progress(0.1, desc="Extracting audio...")

        # Perform translation
        output_path = translator.translate_video(
            video_path,
            source_language,
            target_language,
        )

        # Update progress
        progress(1.0, desc="Translation complete!")

        logger.info(f"Translation successful: {output_path}")
        gr.Info(f"Translation complete! Video saved to: {output_path}")

        return output_path

    except Exception as e:
        error_msg = f"Translation failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        gr.Error(error_msg)
        return None


def create_gradio_interface() -> gr.Blocks:
    """Create and configure the Gradio web interface.

    Returns:
        Configured Gradio Blocks interface

    Example:
        >>> interface = create_gradio_interface()
        >>> interface.launch()
    """
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .gr-button-primary {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
        border: none !important;
    }
    .footer {
        text-align: center;
        margin-top: 2em;
        color: #666;
    }
    """

    with gr.Blocks(
        title="Video Translator",
        theme=gr.themes.Soft(),
        css=custom_css,
    ) as interface:
        # Header
        gr.Markdown(
            """
            # 🎬 Video Translator
            ### Translate video content across multiple languages using AI

            Transform your videos with automatic speech recognition, translation, and voice synthesis.
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("## 📤 Input")

                video_input = gr.File(
                    label="Upload Video",
                    file_types=["video"],
                    type="filepath",
                )

                source_lang = gr.Dropdown(
                    choices=SUPPORTED_LANGUAGES,
                    label="Source Language",
                    value="English",
                    info="Select the language spoken in the video",
                )

                target_lang = gr.Dropdown(
                    choices=SUPPORTED_LANGUAGES,
                    label="Target Language",
                    value="Spanish",
                    info="Select the language for translation",
                )

                translate_btn = gr.Button(
                    "🚀 Translate Video",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=1):
                # Output section
                gr.Markdown("## 📥 Output")

                video_output = gr.Video(
                    label="Translated Video",
                    autoplay=False,
                )

        # Information section
        with gr.Accordion("ℹ️ How it works", open=False):
            gr.Markdown(
                """
                ### Translation Pipeline:

                1. **Audio Extraction**: Extracts audio track from the uploaded video
                2. **Speech Recognition**: Converts speech to text using Google Speech API
                3. **Translation**: Translates text using advanced AI translation
                4. **Speech Synthesis**: Generates natural-sounding speech in target language
                5. **Video Composition**: Creates new video with translated audio

                ### Supported Languages:
                - 🇬🇧 English
                - 🇮🇹 Italian
                - 🇯🇵 Japanese
                - 🇷🇺 Russian
                - 🇪🇸 Spanish
                - 🇩🇪 German
                - 🇧🇷 Portuguese

                ### Tips for Best Results:
                - Use videos with clear audio and minimal background noise
                - Ensure the source language matches the spoken language in the video
                - Processing time depends on video length (typically 1-3 minutes)
                - Maximum file size: 500 MB
                """
            )

        # Examples section
        gr.Markdown("## 📚 Examples")
        gr.Examples(
            examples=[
                ["obama.mp4", "English", "Spanish"],
                ["obama.mp4", "English", "Italian"],
                ["obama.mp4", "English", "German"],
                ["obama.mp4", "English", "Japanese"],
                ["obama.mp4", "English", "Portuguese"],
            ],
            inputs=[video_input, source_lang, target_lang],
            outputs=video_output,
            fn=translate_video_wrapper,
            cache_examples=False,
        )

        # Footer
        gr.Markdown(
            f"""
            <div class="footer">
                <p>
                    <strong>Video Translator v{__version__}</strong><br>
                    Developed by <a href="https://ruslanmv.com" target="_blank">Ruslan Magana</a><br>
                    Licensed under Apache 2.0
                </p>
            </div>
            """,
            elem_classes="footer",
        )

        # Event handlers
        translate_btn.click(
            fn=translate_video_wrapper,
            inputs=[video_input, source_lang, target_lang],
            outputs=video_output,
            api_name="translate",
        )

    return interface


def main() -> None:
    """Main entry point for the application.

    This function initializes logging, creates the Gradio interface,
    and launches the web server.
    """
    # Setup logging
    setup_logger(name="video_translator", level="INFO")

    logger.info("=" * 80)
    logger.info(f"Video Translator v{__version__} - Starting application")
    logger.info("=" * 80)

    try:
        # Create interface
        interface = create_gradio_interface()

        # Launch with configuration
        logger.info("Launching Gradio interface...")
        interface.launch(
            server_name="0.0.0.0",  # Listen on all interfaces
            server_port=7860,  # Default Gradio port
            share=False,  # Set to True to create a public link
            show_error=True,
            quiet=False,
        )

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
