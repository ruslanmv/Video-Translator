"""Video Translator - Legacy entry point (backwards compatibility).

This file is maintained for backwards compatibility with the original
single-file implementation. It now serves as a simple wrapper around
the production-ready modular implementation.

For new deployments, please use:
    python -m video_translator.main
or:
    video-translator

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import warnings

# Import the new production-ready implementation
from video_translator.main import main

# Show deprecation warning
warnings.warn(
    "Running app.py directly is deprecated. "
    "Please use 'video-translator' command or 'python -m video_translator.main' instead. "
    "This legacy entry point will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2,
)

# Launch the application using the new implementation
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("⚠️  DEPRECATION WARNING")
    print("=" * 80)
    print("You are running the legacy app.py entry point.")
    print("This file is maintained for backwards compatibility only.")
    print("\nPlease update your deployment to use:")
    print("  • Command: video-translator")
    print("  • Or: python -m video_translator.main")
    print("=" * 80 + "\n")

    # Run the production-ready application
    main()