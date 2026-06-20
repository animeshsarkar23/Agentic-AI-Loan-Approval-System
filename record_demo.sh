#!/bin/bash

# Screen Recording Script for Loan Approval System Demo
# Automatically records your screen while you demo the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           📹 LOAN APPROVAL SYSTEM - SCREEN RECORDING SCRIPT 📹              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check which tools are available
echo -e "${YELLOW}Checking available recording tools...${NC}\n"

FFMPEG_AVAILABLE=false
SIMPLESCREENRECORDER_AVAILABLE=false
GNOME_AVAILABLE=false
OBS_AVAILABLE=false

if command -v ffmpeg &> /dev/null; then
    FFMPEG_AVAILABLE=true
    echo -e "${GREEN}✓${NC} FFmpeg is installed"
fi

if command -v simplescreenrecorder &> /dev/null; then
    SIMPLESCREENRECORDER_AVAILABLE=true
    echo -e "${GREEN}✓${NC} SimpleScreenRecorder is installed"
fi

if command -v gnome-recorder &> /dev/null; then
    GNOME_AVAILABLE=true
    echo -e "${GREEN}✓${NC} GNOME Recorder is installed"
fi

if command -v obs &> /dev/null; then
    OBS_AVAILABLE=true
    echo -e "${GREEN}✓${NC} OBS Studio is installed"
fi

echo ""

# If no tools available, install ffmpeg
if [ "$FFMPEG_AVAILABLE" = false ] && [ "$SIMPLESCREENRECORDER_AVAILABLE" = false ] && [ "$GNOME_AVAILABLE" = false ] && [ "$OBS_AVAILABLE" = false ]; then
    echo -e "${YELLOW}No recording tool found. Installing FFmpeg...${NC}\n"
    sudo apt-get update
    sudo apt-get install -y ffmpeg
    FFMPEG_AVAILABLE=true
fi

echo ""
echo -e "${BLUE}Select recording method:${NC}"
echo ""
echo "1) FFmpeg (Professional, command-line)"
echo "2) SimpleScreenRecorder (GUI-based)"
echo "3) GNOME Recorder (Built-in, instant)"
echo "4) OBS Studio (Professional streaming)"
echo "5) Exit"
echo ""
read -p "Enter your choice (1-5): " choice

OUTPUT_FILE="loan_approval_demo_$(date +%Y%m%d_%H%M%S).mp4"

case $choice in
    1)
        if [ "$FFMPEG_AVAILABLE" = true ]; then
            echo -e "\n${GREEN}Starting FFmpeg recording...${NC}"
            echo -e "${YELLOW}Output file: $OUTPUT_FILE${NC}"
            echo -e "${YELLOW}Press 'q' to stop recording${NC}\n"

            # Get screen resolution
            RESOLUTION=$(xdpyinfo | grep dimensions | awk '{print $2}')

            ffmpeg -f x11grab -s "$RESOLUTION" -r 30 -i :0 \
                -c:v libx264 -crf 23 -preset veryfast \
                "$OUTPUT_FILE"

            echo -e "\n${GREEN}Recording saved to: $OUTPUT_FILE${NC}"
        else
            echo -e "${RED}FFmpeg not available${NC}"
            exit 1
        fi
        ;;
    2)
        if [ "$SIMPLESCREENRECORDER_AVAILABLE" = true ]; then
            echo -e "\n${GREEN}Opening SimpleScreenRecorder...${NC}"
            simplescreenrecorder &
            echo -e "${YELLOW}Configured output file location: $OUTPUT_FILE${NC}"
        else
            echo -e "${RED}SimpleScreenRecorder not available. Install with: sudo apt-get install -y simplescreenrecorder${NC}"
            exit 1
        fi
        ;;
    3)
        if [ "$GNOME_AVAILABLE" = true ]; then
            echo -e "\n${GREEN}GNOME Recorder ready!${NC}"
            echo -e "${YELLOW}Press Ctrl+Alt+Shift+R to start recording${NC}"
            echo -e "${YELLOW}Press Ctrl+Alt+Shift+R again to stop${NC}"
            echo -e "${YELLOW}Video will be saved to: ~/Videos/${NC}"
        else
            echo -e "${RED}GNOME Recorder not available. Install with: sudo apt-get install -y gnome-recorder${NC}"
            exit 1
        fi
        ;;
    4)
        if [ "$OBS_AVAILABLE" = true ]; then
            echo -e "\n${GREEN}Opening OBS Studio...${NC}"
            obs &
            echo -e "${YELLOW}Steps:${NC}"
            echo "  1. Add Source → Display Capture"
            echo "  2. Click Start Recording"
            echo "  3. Use the application"
            echo "  4. Click Stop Recording"
        else
            echo -e "${RED}OBS Studio not available. Install with: sudo apt-get install -y obs-studio${NC}"
            exit 1
        fi
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Recording setup complete!${NC}"
