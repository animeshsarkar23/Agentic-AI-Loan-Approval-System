# 📹 Screen Recording Guide - Loan Approval System Demo

## Quick Start

### Method 1: Automatic FFmpeg Recording (Easiest)

```bash
cd /home/ubuntu/Capstone
./auto_record_ffmpeg.sh
```

Then:
1. Press ENTER to start recording
2. Demo the application at http://localhost:8501
3. Press 'q' to stop recording
4. Your video will be saved in `recordings/` folder

---

## Detailed Recording Methods

### Method 1: FFmpeg (Professional, Command-Line)

**Installation:**
```bash
sudo apt-get install -y ffmpeg
```

**Record Screen:**
```bash
# Simple one-liner
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 -c:v libx264 -crf 23 demo.mp4

# With audio (if needed)
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 \
  -f pulse -ac 2 -i default \
  -c:v libx264 -c:a aac -crf 23 demo_with_audio.mp4
```

**To Stop:** Press `q` in terminal

**Parameters Explained:**
```
-f x11grab              Capture X11 display
-s 1920x1080           Screen resolution (adjust to your screen)
-r 30                  30 frames per second
-i :0                  Input display (main screen)
-c:v libx264           Video codec (H.264)
-crf 23                Quality (0=best, 51=worst, 23=default)
-preset veryfast       Speed (ultrafast < superfast < veryfast < fast < medium)
demo.mp4               Output filename
```

**Useful Examples:**

High Quality (larger file):
```bash
ffmpeg -f x11grab -s 1920x1080 -r 60 -i :0 -c:v libx264 -crf 18 -preset slow demo_hq.mp4
```

Fast Recording (smaller file):
```bash
ffmpeg -f x11grab -s 1920x1080 -r 24 -i :0 -c:v libx264 -crf 28 -preset ultrafast demo_small.mp4
```

With Timestamp:
```bash
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 \
  -vf "drawtext=text='%{localtime}':fontsize=16:fontcolor=white:x=10:y=10" \
  -c:v libx264 -crf 23 demo_with_time.mp4
```

---

### Method 2: SimpleScreenRecorder (GUI)

**Installation:**
```bash
sudo apt-get install -y simplescreenrecorder
```

**Steps:**
1. Open "SimpleScreenRecorder" from applications
2. Configure:
   - Video area: Full screen (or custom)
   - Video format: MP4
   - FPS: 30
   - Quality: Medium/High
   - Output file: `demo.mp4`
3. Click "Start Recording"
4. Demo your application
5. Click "Stop Recording"
6. Video saved automatically

**Pros:** Easy GUI, good quality
**Cons:** GUI-only, requires X11

---

### Method 3: GNOME Recorder (Built-in)

**Installation (if not pre-installed):**
```bash
sudo apt-get install -y gnome-recorder
```

**Keyboard Shortcuts:**
- `Ctrl+Alt+Shift+R` - Start recording
- `Ctrl+Alt+Shift+R` - Stop recording
- Videos saved to: `~/Videos/`

**Steps:**
1. Press `Ctrl+Alt+Shift+R` (recording starts silently)
2. Demo the application
3. Press `Ctrl+Alt+Shift+R` again (recording stops)
4. Video file appears in `~/Videos/`

**Pros:** Instant, no setup, lightweight
**Cons:** Limited controls, files may be large

---

### Method 4: OBS Studio (Professional)

**Installation:**
```bash
sudo apt-get install -y obs-studio
```

**Setup:**
1. Open OBS Studio
2. Click "+" under "Sources"
3. Select "Display Capture"
4. Choose display and click OK
5. Configure output format and location
6. Click "Start Recording"

**During Recording:**
- Use application normally
- Recording indicator shows in OBS window

**Stop Recording:**
- Click "Stop Recording" button
- Video file created automatically

**Pros:** Professional quality, customizable, powerful
**Cons:** More complex, higher CPU usage

---

### Method 5: Terminal Session Recording (Asciinema)

Good for recording terminal commands and output.

**Installation:**
```bash
pip install asciinema
```

**Record:**
```bash
asciinema rec demo.cast
# Type commands normally
# Press Ctrl+D to stop
```

**Playback:**
```bash
asciinema play demo.cast
```

**Share Online:**
```bash
asciinema upload demo.cast
```

---

## Complete Demo Recording Script

### Step-by-Step Process

**Setup (1 minute):**
```bash
# Start recording with this command
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 -c:v libx264 -crf 23 -preset veryfast demo.mp4
```

**During Recording (10-15 minutes):**

1. **Show the API (1 min)**
   - Open browser to: http://localhost:8000/docs
   - Show the 5 endpoints
   - Show request/response examples

2. **Show Streamlit UI (2 min)**
   - Open: http://localhost:8501
   - Show all 4 pages in sidebar
   - Highlight features on each page

3. **Submit Application (3-5 min)**
   - Navigate to "Submit Application" page
   - Modify some values to show it's customizable
   - Click "🚀 Submit Application & Analyze"
   - Show the loading state
   - Display the final results
   - Expand agent analysis sections

4. **View History (2 min)**
   - Go to "Application History" page
   - Show summary statistics
   - Display applications table
   - Show decision breakdown

5. **Show System Status (1 min)**
   - Go to "System Status" page
   - Show configuration settings
   - Display active agents

6. **Show API Docs (1 min)**
   - Open http://localhost:8000/docs
   - Try a sample API call
   - Show the response

**Stop Recording:**
```
Press 'q' in the FFmpeg terminal
```

---

## Post-Recording Tasks

### View Recording
```bash
# Play with default player
ffplay demo.mp4

# Or with VLC
vlc demo.mp4

# Or with other player
mpv demo.mp4
```

### Get Video Info
```bash
ffmpeg -i demo.mp4
# Shows duration, resolution, bitrate, etc.
```

### Convert Format
```bash
# Convert to WebM (smaller)
ffmpeg -i demo.mp4 -c:v libvpx -c:a libvorbis demo.webm

# Convert to animated GIF (for sharing)
ffmpeg -i demo.mp4 -vf "fps=10,scale=1280:-1" demo.gif
```

### Compress Video
```bash
# Reduce file size
ffmpeg -i demo.mp4 -c:v libx264 -crf 28 -c:a aac -b:a 128k demo_compressed.mp4

# Settings:
# -crf 28      : Higher number = more compression (25-28 is good)
# -b:a 128k    : Audio bitrate (lower = smaller file)
```

### Add Text Overlay
```bash
# Add title or watermark
ffmpeg -i demo.mp4 \
  -vf "drawtext=text='Loan Approval System':fontsize=24:fontcolor=white:x=50:y=50" \
  -c:a copy demo_titled.mp4
```

### Trim Video
```bash
# Extract portion from 10s to 60s
ffmpeg -i demo.mp4 -ss 00:00:10 -to 00:01:00 -c copy demo_trimmed.mp4
```

---

## Recording Quality Guidelines

### For Different Purposes

**Quick Demo (Small File):**
```bash
ffmpeg -f x11grab -s 1920x1080 -r 24 -i :0 \
  -c:v libx264 -crf 28 -preset ultrafast demo.mp4
```
- File size: ~50-100 MB for 10 minutes
- Quality: Acceptable for sharing

**High Quality (Large File):**
```bash
ffmpeg -f x11grab -s 1920x1080 -r 60 -i :0 \
  -c:v libx264 -crf 18 -preset slow demo_hq.mp4
```
- File size: ~200-400 MB for 10 minutes
- Quality: Professional grade

**Balanced (Medium File):**
```bash
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 \
  -c:v libx264 -crf 23 -preset veryfast demo.mp4
```
- File size: ~100-150 MB for 10 minutes
- Quality: Good for most uses

---

## Troubleshooting

### FFmpeg not capturing display
```bash
# Check display number
echo $DISPLAY
# Usually :0 or :1

# Try with specific display
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :1 -c:v libx264 demo.mp4
```

### Audio not capturing
```bash
# Record with audio from system/microphone
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 \
  -f pulse -ac 2 -i default \
  -c:v libx264 -c:a aac demo_audio.mp4
```

### High CPU usage
```bash
# Use faster preset
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 \
  -c:v libx264 -preset ultrafast -crf 28 demo.mp4
```

### Very large file size
```bash
# Increase CRF value (0-51, higher = more compression)
ffmpeg -f x11grab -s 1920x1080 -r 24 -i :0 \
  -c:v libx264 -crf 30 demo_small.mp4
```

---

## Video Sharing

### YouTube Upload
1. Use high quality version
2. Max file size: 256 GB
3. Recommended format: MP4 with H.264 video + AAC audio

### Slack/Teams Sharing
1. Compress video: `ffmpeg -i demo.mp4 -crf 28 demo_small.mp4`
2. Upload to platform
3. Max size usually 100-500 MB

### Email Sharing
1. Use lowest quality/compressed version
2. Consider uploading to cloud and sharing link instead
3. Max size: 25 MB typically

### Cloud Storage (Google Drive, Dropbox, OneDrive)
1. Use medium quality version
2. Unlimited storage usually available
3. Easy sharing with link

---

## Automated Recording Script

**Use the included script:**
```bash
cd /home/ubuntu/Capstone
./auto_record_ffmpeg.sh
```

**What it does:**
1. Checks for FFmpeg installation
2. Creates recordings directory
3. Gets screen resolution automatically
4. Starts recording with professional settings
5. Saves with timestamp filename

---

## Quick Reference Commands

```bash
# Record screen
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 -c:v libx264 -crf 23 demo.mp4

# Record with audio
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0 -f pulse -ac 2 -i default \
  -c:v libx264 -c:a aac demo.mp4

# Play recording
ffplay demo.mp4

# Get info
ffmpeg -i demo.mp4

# Compress
ffmpeg -i demo.mp4 -c:v libx264 -crf 28 demo_small.mp4

# Trim
ffmpeg -i demo.mp4 -ss 00:00:10 -to 00:01:00 -c copy demo_trimmed.mp4

# Convert to WebM
ffmpeg -i demo.mp4 -c:v libvpx -c:a libvorbis demo.webm
```

---

## Storage Locations

By default, recordings are saved to:
- **FFmpeg**: Current directory (where you run command)
- **SimpleScreenRecorder**: ~/Videos/
- **GNOME Recorder**: ~/Videos/
- **OBS Studio**: ~/Videos/ (configurable)
- **Asciinema**: Current directory

You can find them using:
```bash
# Find all .mp4 files
find ~ -name "*.mp4" -type f

# Or in recordings directory
ls -lh /home/ubuntu/Capstone/recordings/
```

---

**Happy Recording! 🎬**

For any issues, refer to FFmpeg documentation: https://ffmpeg.org/documentation.html
