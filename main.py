from fastapi import FastAPI, HTTPException, Query
import subprocess
import json
import streamlink
from pytube import YouTube
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/ytdl")
def ytdl(url: str, timeout: int = 60):
    """Run yt-dlp and return parsed JSON metadata when available."""
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--dump-single-json",
        url,
        "--cookies",
        "/etc/secrets/cookies.txt"
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
        try:
            data = json.loads(result.stdout)
            return {"success": True, "data": data}
        except json.JSONDecodeError:
            return {"success": True, "raw": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr or str(e))
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="yt-dlp command timed out")


@app.get("/ytdl_download")
def ytdl_download(url: str, output_dir: str = "/tmp", timeout: int = 600):
    """Download video/audio via yt-dlp to server and return file path."""
    filename_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-o", filename_template,
        url
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            timeout=timeout
        )
        return {"success": True, "message": f"Downloaded to {output_dir}"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr or str(e))
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="yt-dlp command timed out")


@app.get("/spotdl")
def spotdl_meta(
    url: str = Query(..., description="Spotify track or playlist URL"),
    timeout: int = 60
):
    """Run spotdl metadata command and return structured output."""
    if not url.startswith("https://open.spotify.com/"):
        raise HTTPException(
            status_code=400,
            detail="Only Spotify track or playlist URLs are supported."
        )
    cmd = ["spotdl", "meta", url]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
        return {"success": True, "output": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr or str(e))
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="spotdl command timed out")


@app.get("/streamlink")
def streamlink_stream(url: str, quality: str = "best"):
    """Return available stream URL using Streamlink."""
    try:
        streams = streamlink.streams(url)
        if not streams:
            raise HTTPException(status_code=404, detail="No streams found")
        if quality not in streams:
            raise HTTPException(status_code=404, detail=f"Quality '{quality}' not found")
        stream_url = streams[quality].to_url()
        return {"success": True, "stream_url": stream_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pytube_download")
def pytube_download(url: str):
    """Get YouTube video info and downloadable streams via Pytube."""
    try:
        yt = YouTube(url)
        streams = []
        for s in yt.streams.filter(progressive=True).order_by('resolution'):
            streams.append({
                "itag": s.itag,
                "mime_type": s.mime_type,
                "resolution": s.resolution,
                "fps": s.fps,
                "filesize": s.filesize
            })
        return {
            "success": True,
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "streams": streams
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
