#!/bin/bash

# Auto-recording script using FFmpeg
# Records screen while running the demo application

set -e

# Configuration
OUTPUT_DIR="/home/ubuntu/Capstone/recordings"
OUTPUT_FILE="$OUTPUT_DIR/loan_approval_demo_$(date +%Y%m%d_%H%M%S).mp4"
DURATION=600  # Default 10 minutes (can be adjusted)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << 'HEADER'
╔══════════════════════════════════════════════════════════════════════════════╗
║                     AUTOMATIC SCREEN RECORDING SETUP                        ║
║                                                                              ║
║            Recording: Loan Approval System Web UI + API Demo                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
HEADER
echo -e "${NC}"

# Create recordings directory
mkdir -p "$OUTPUT_DIR"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}Installing FFmpeg...${NC}"
    sudo apt-get update
    sudo apt-get install -y ffmpeg
fi

# Get screen resolution
RESOLUTION=$(xdpyinfo 2>/dev/null | grep dimensions | awk '{print $2}' || echo "1920x1080")

echo -e "${YELLOW}Configuration:${NC}"
echo "  Output: $OUTPUT_FILE"
echo "  Resolution: $RESOLUTION"
echo "  FPS: 30"
echo ""
echo -e "${YELLOW}Ready to record. Instructions:${NC}"
echo "  1. Application is already running at http://localhost:8501"
echo "  2. Press ENTER to START recording"
echo "  3. Demo the application in your browser"
echo "  4. Press 'q' in terminal to STOP recording"
echo ""

read -p "Press ENTER to start recording..."

echo -e "${GREEN}⏹️  Recording started! Press 'q' to stop...${NC}\n"

# Start recording
ffmpeg -f x11grab -s "$RESOLUTION" -r 30 -i :0 \
    -c:v libx264 -crf 23 -preset veryfast \
    -y "$OUTPUT_FILE"

# After recording stops
echo ""
echo -e "${GREEN}✅ Recording completed!${NC}"
echo -e "${GREEN}📁 Saved to: $OUTPUT_FILE${NC}"
echo ""
echo -e "${YELLOW}Video Info:${NC}"
ffmpeg -i "$OUTPUT_FILE" 2>&1 | grep "Duration" || true
echo ""
echo -e "${YELLOW}You can now:${NC}"
echo "  • Play: ffplay $OUTPUT_FILE"
echo "  • Share: scp $OUTPUT_FILE user@server:"
echo "  • Convert: ffmpeg -i $OUTPUT_FILE -c:v libvpx output.webm"
echo ""

