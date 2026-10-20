# cURL Video Downloader

A small macOS Python utility that downloads a video using a request copied from a browser's Developer Tools. Instead of manually copying request headers into Python, it reads a copied **cURL** command from the clipboard and runs it with the system `curl` command.

## Features

- Reads a cURL command from the macOS clipboard.
- Reuses the copied URL, HTTP method, headers, cookies, and other supported cURL options.
- Follows redirects and reports HTTP errors.
- Downloads to a temporary `.part` file first, then renames it to the final MP4 filename when cURL succeeds.
- Preserves the temporary file when cURL fails, so data is not automatically deleted during error handling.

> **Note:** This script saves the HTTP response as a file. It does not extract videos from every website automatically, bypass access controls, or convert streaming formats such as HLS/DASH into MP4. Copy the actual video/media request from the Network panel and make sure you are authorized to download it.

## Requirements

- the script uses `pbpaste` to read the clipboard(Replace as per your OS support)
- The `curl` command-line tool
- A browser such as Chrome

No third-party Python package is required for the cURL-based version of the script.

## Setup

1. Save the Python script as `video_downloader.py`.
2. Open Terminal and change to the folder containing the script. For example:

   ```bash
   cd "/Users/your-username/"
   ```

3. Confirm Python and cURL are available:

   ```bash
   python3 --version
   curl --version
   ```

## How to use

1. Open the webpage containing the video and start playing it if necessary.
2. Open Chrome Developer Tools (`View` → `Developer` → `Developer Tools`, or `Cmd` + `Option` + `I`).
3. Select the **Network** tab. If needed, reload the page or play the video to populate the request list.
4. Find the request that returns the video data. It may have a large response size and a media-related content type. Avoid choosing an unrelated page, thumbnail, manifest, or subtitle request.
5. Right-click the relevant request and choose **Copy** → **Copy as cURL**.
6. In Terminal, run the script from the project folder:

   ```bash
   python3 script-name.py
   ```

7. On success, the video is saved as `your-filename.mp4` in the current working directory.

The script reads the clipboard at runtime, so copy the cURL request immediately before running it.

## Output files

- `<your-filename>.mp4` — the completed download from the last successful run.
- `your-filename.mp4.part` — a temporary download file. If cURL fails, the script leaves this file in place for diagnosis instead of deleting it automatically. A `.part` file may be incomplete and may not play correctly.

Run the script from the project directory if you want the output saved there. The output path is relative to the current working directory, not necessarily the directory where the Python script is stored.

## Troubleshooting

### `curl: (3) URL rejected: Malformed input to a URL function`

The copied command may have been parsed incorrectly, or newline-only arguments may have been passed to cURL as extra URLs. Make sure the script removes shell line continuations and filters empty/whitespace-only arguments after parsing the cURL text. The parsed command should not contain standalone `"\n"` arguments.

### `403 Forbidden`

The server refused the request. Copy a fresh **Copy as cURL** command while you are signed in and have access to the video. Requests can depend on cookies, authorization headers, a `Referer`, temporary query parameters, or an active session. Do not publish or share these values.

### The script says it downloaded successfully, but the file will not play

Check whether the selected request is actually the video data. A website may serve a playlist/manifest (for example, HLS or DASH), an encrypted stream, or a non-video error response instead of a standalone MP4. Review the request's response headers and content type in Developer Tools.

### The `.part` file exists after a failure

The file is retained intentionally. It may contain partial data or even a complete response followed by an unrelated command-line error. Do not rename it to `.mp4` unless you have verified that it is a valid video. Review the cURL error and the generated argument list before trying again.

### The clipboard does not contain a cURL command

Copy the request again using **Network** → right-click request → **Copy** → **Copy as cURL**, then immediately rerun the script.

## Security and privacy

A copied cURL command can contain session cookies, authorization tokens, signed URLs, or other credentials. Anyone who obtains them may be able to access your account or the protected resource until they expire or are revoked.

- Keep the command and clipboard contents private.
- Do not commit copied cURL requests, cookies, or tokens to Git.
- Do not paste them into public issue trackers, chats, or online converters.
- Only download content you own or are authorized to access and download.

## Limitations

- The workflow requires a manual copy action from Developer Tools for each request.
- cURL options copied from a browser are passed through to the installed cURL executable, but unusual shell syntax or incompatible options may still need manual adjustment.
- Some media streams require a dedicated downloader or authorized application/API rather than saving a single network response as an MP4 file.

## License

Ashutosh K Roy
