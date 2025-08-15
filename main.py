from fastapi import FastAPI, HTTPException, Query
import subprocess
import json
import streamlink


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



