from fastapi import FastAPI, HTTPException
import subprocess
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

from fastapi import FastAPI, HTTPException
import subprocess
import json
 
app = FastAPI()

@app.get("/ytdl")
def ytdl(url: str, timeout: int = 60):
    """Run yt-dlp and return parsed JSON metadata when available.

    - `url` (str): the YouTube (or other) URL to inspect
    - `timeout` (int): how long to allow the command to run (seconds)
    """
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--dump-single-json",
        url,
        "--cookies",
        "/etc/secrets/cookies.txt"  # use the secret cookies file from Render
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
            # If output isn't JSON for some reason, return raw stdout
            return {"success": True, "raw": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr or str(e))
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="yt-dlp command timed out")



@app.get("/spotdl")
def spotdl_meta(url: str, timeout: int = 60):
    """Run spotdl metadata command and return its stdout.

    Note: CLI behaviour for spotdl can vary across versions. This endpoint returns
    raw stdout so you can inspect what the installed `spotdl` prints.
    """
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
