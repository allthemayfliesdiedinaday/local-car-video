# 🐱 cat

Generates a cat video using random cat GIFs from GIPHY and random music tracks. It overlays a banner that says:

> "post this cat on the Xth day of the month"

The script downloads a cat GIF/video, selects a random music track, and uses FFmpeg to generate a finished `.mp4` video and a thumbnail GIF.

## Requirements

- Python 3.6+
- FFmpeg
- Python libraries:

```
requests
```

### Install dependencies

```bash
pip install requests
```

## Install FFmpeg

### Linux

```bash
sudo apt install ffmpeg
```

(or use your package manager, e.g. `pacman`, `dnf`, etc.)

### macOS

```bash
brew install ffmpeg
```

### Windows

```powershell
winget install -e --id Gyan.FFmpeg
```

## Setup

1. Create a free GIPHY API key here:  
   https://developers.giphy.com

2. In the script, replace `YOUR_KEY_HERE` with your API key:

```python
GIPHY_KEY = "YOUR_KEY_HERE"
```

3. Configure your font file path. Arial is provided by default along with the script:

```python
fontfile = "./arial.ttf"
```

4. (Optional) Configure `tracks.txt` to your liking.

## Notes

- The GIPHY API has a limit of ~100 requests per hour
- Some music links may fail if they are invalid
- If many cats have already been used, the script may retry several API requests
- The script randomly chooses a start time in the music (0–30 seconds)
