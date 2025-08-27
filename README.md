# project_barbossa

This project generates an M3U8 playlist file (`streamed.m3u8`) from live match data fetched from streamed.

## Disclaimer
I am not responsible for the content, availability, or legality of the streams referenced in the generated playlist. Use at your own risk.

## How it works
- The script `m3u8_builder.py` fetches match data from a remote API.
- It builds an M3U8 playlist with match info and stream URLs.
- The generated file is saved as `streamed.m3u8`.

## Usage

### Local
1. Install Python 3.11+ and dependencies:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```bash
   python m3u8_builder.py
   ```
3. The output file `streamed.m3u8` will be created in the project directory.

### GitHub Actions
A workflow is included to automatically run the script and commit the output every hour.

## Files
- `m3u8_builder.py`: Main script to generate the playlist.
- `.github/workflows/build_and_commit.yml`: GitHub Actions workflow for automation.
- `streamed.m3u8`: Generated playlist file (auto-updated).


