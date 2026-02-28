# Project Cinema

A self-hosted streaming platform for movies and TV shows. Stream your local video library from any device on your network.

## What is this?

I built this for personal use to stream my own video collection. It scans a folder of videos, pulls metadata (posters, descriptions, etc.), and serves them through a nice web interface. Think of it as a personal Netflix.

If you want to use it, cool - just know it was made for my use case, so it might need tweaking for yours.

## Features

- **Video Library** - Automatic scanning and metadata for movies/TV shows
- **User Auth** - Register and login with multiple users
- **Progress Tracking** - Resume where you left off
- **Streaming** - Adaptive streaming with seek support
- **Responsive** - Works on desktop, tablet, mobile
- **Self-hosted** - Runs on your own hardware

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React + TypeScript
- **Database:** SQLite
- **Video Processing:** FFmpeg

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- FFmpeg (for video processing)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure your video folder in .env
# Then run
python -m uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install  # or pnpm install
npm run build
```

The API runs on `http://localhost:8001` and the UI on `http://localhost:8001/ui/`

## Project Structure

```
ProjectCinema/
├── backend/          # FastAPI server
│   ├── main.py       # API endpoints
│   ├── models.py     # Database models
│   ├── auth.py       # Authentication
│   └── video_utils.py # Streaming logic
├── frontend/         # React app
│   └── src/
│       ├── pages/    # UI pages
│       └── components/ # Reusable components
├── data/             # Thumbnails, library.json
└── videos/           # Your video files go here
```

## Configuration

Edit `.env` to configure:
- Video folder path
- Server port
- Admin credentials

## License

MIT License - See LICENSE file. Use at your own risk.

## Disclaimer

This was made for personal use. I'm sharing it because some people asked, but I can't provide support or guarantee it works for your setup. No warranty, no promises.

If it breaks, you get to keep both pieces.