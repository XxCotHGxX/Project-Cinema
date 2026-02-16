from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, auth, database, video_utils
from .config import settings
from datetime import datetime
import os
import json

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Project Cinema API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for thumbnails/data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=DATA_DIR), name="static")

# Mount frontend build
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
    app.mount("/ui", StaticFiles(directory=FRONTEND_DIST, html=True), name="ui")

from starlette.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/ui/")

@app.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = auth.get_password_hash(password)
    user_type = "ADMIN" if db.query(models.User).count() == 0 else "USER"
    
    new_user = models.User(username=username, email=email, hashed_password=hashed_pwd, user_type=user_type)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": new_user.username, "role": new_user.user_type}

@app.post("/token")
def login(email: str, password: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.user_type})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/movies")
def get_movies(db: Session = Depends(database.get_db)):
    # First, ensure DB is synced with library.json
    library_path = os.path.join(DATA_DIR, "library.json")
    if os.path.exists(library_path):
        with open(library_path, "r") as f:
            library_data = json.load(f)
            for item in library_data:
                video = db.query(models.Video).filter(models.Video.file_path == item["path"]).first()
                if not video:
                    video = models.Video(
                        title=item["title"],
                        filename=item["filename"],
                        file_path=item["path"],
                        description=item["description"],
                        release_date=str(item["year"]),
                        poster_url=item["poster_url"],
                        backdrop_url=item["backdrop_url"],
                        genre=item.get("genre", "Uncategorized"),
                        media_type=item.get("media_type", "Movie"),
                        season=item.get("season"),
                        episode=item.get("episode")
                    )
                    db.add(video)
                else:
                    # Update existing fields if they were missing
                    if not video.media_type:
                        video.media_type = item.get("media_type", "Movie")
                    if not video.season:
                        video.season = item.get("season")
                    if not video.episode:
                        video.episode = item.get("episode")
                    if not video.genre:
                        video.genre = item.get("genre", "Uncategorized")
            db.commit()
    
    return db.query(models.Video).order_by(models.Video.media_type, models.Video.title, models.Video.season, models.Video.episode).all()

@app.post("/progress/{video_id}")
def update_progress(video_id: int, seconds: int, duration: int = 0, db: Session = Depends(database.get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video.progress = seconds
    if duration > 0:
        video.duration = duration
    video.last_watched = datetime.utcnow()
    db.commit()
    return {"message": "Progress updated", "progress": seconds, "duration": video.duration}

@app.get("/stream/{video_id}")
async def stream_video(video_id: int, range: str = Header(None), db: Session = Depends(database.get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_path = video.file_path
    
    if not video_path or not os.path.exists(video_path):
        # Fallback to sample if the specific file is gone
        video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "videos", "sample.mp4")
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Video file not found")
    
    return video_utils.send_video_range_requests(video_path, range)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
