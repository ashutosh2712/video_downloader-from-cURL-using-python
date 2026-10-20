
import re
import shlex
import subprocess
from pathlib import Path

OUTPUT_FILE = Path("/Users/<your_username>/Downloads/downloaded_video_new.mp4")
TEMP_FILE = Path("downloaded_video.mp4.part")


def download_video():
    result = subprocess.run(
        ["pbpaste"],
        capture_output=True,
        text=True,
        check=True,
    )

    curl_command = result.stdout.strip()

    if not curl_command.startswith("curl"):
        raise ValueError(
            "Copy the request using Network → Copy as cURL first."
        )

    # Remove shell line continuations before parsing.
    curl_command = re.sub(r"\\\r?\n", " ", curl_command)

    # Parse the command into arguments.
    args = shlex.split(curl_command)

    # Remove arguments containing only whitespace or newlines.
    args = [arg for arg in args if arg.strip()]

    if not args or args[0] != "curl":
        raise ValueError("Invalid cURL command.")

    TEMP_FILE = Path("downloaded_video.mp4.part")

    # Save to a temporary file instead of the final video.
    args.extend([
        "--location",
        "--fail",
        "--show-error",
        "--output",
        str(TEMP_FILE),
    ])

    print("Executing copied cURL request...")

    try:
        subprocess.run(args, check=True)

        if not TEMP_FILE.exists() or TEMP_FILE.stat().st_size == 0:
            raise RuntimeError("The downloaded file is empty.")

        # Rename only after cURL exits successfully.
        TEMP_FILE.replace(Path(OUTPUT_FILE))

        print("Download completed successfully.")

    except subprocess.CalledProcessError as error:
        print(f"cURL failed with exit code {error.returncode}.")

        if TEMP_FILE.exists():
            print(f"Partial or downloaded data preserved at: {TEMP_FILE.resolve()}")

        raise

if __name__ == "__main__":
    try:
        download_video()
    except (
        ValueError,
        RuntimeError,
        subprocess.CalledProcessError,
        subprocess.SubprocessError,
    ) as error:
        print(f"Error: {error}")
