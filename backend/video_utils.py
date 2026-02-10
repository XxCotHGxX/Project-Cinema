import os
from fastapi import HTTPException
from starlette.responses import StreamingResponse, RedirectResponse

def send_video_range_requests(file_path: str, range_header: str):
    file_size = os.path.getsize(file_path)
    
    # Parse range header (e.g. bytes=0-1023)
    try:
        range_start, range_end = range_header.replace("bytes=", "").split("-")
        range_start = int(range_start)
        range_end = int(range_end) if range_end else file_size - 1
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid range header")

    if range_start >= file_size:
        raise HTTPException(status_code=416, detail="Requested range not satisfiable")

    chunk_size = 1024 * 1024 # 1MB chunks
    
    def file_iterator():
        with open(file_path, "rb") as f:
            f.seek(range_start)
            remaining = range_end - range_start + 1
            while remaining > 0:
                to_read = min(remaining, chunk_size)
                data = f.read(to_read)
                if not data:
                    break
                yield data
                remaining -= len(data)

    headers = {
        "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(range_end - range_start + 1),
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(file_iterator(), status_code=206, headers=headers)
