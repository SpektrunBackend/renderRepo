from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/ytdl")
def ytdl(url: str):
    result = subprocess.run(
        ["yt-dlp", "--no-warnings", "--dump-json", url],
        capture_output=True, text=True
    )
    return {"output": result.stdout}
