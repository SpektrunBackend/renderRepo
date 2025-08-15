# Spek Api (Render-ready)

## Files
- `main.py` — FastAPI app with endpoints `/`, `/ytdl`, and `/spotdl`
- `requirements.txt` — dependencies

## Deploy to Render (manual)
1. Create a GitHub repo and push these files to `master`.
2. In Render dashboard, create a **New Web Service** and connect your GitHub repo.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Choose the **Free** instance type to start.
6. Deploy. After deploy, test the root URL and endpoints.

## Example tests
- Root: `GET https://<your-service>.onrender.com/`
- ytdl: `GET https://<your-service>.onrender.com/ytdl?url=<video-url>`
- spotdl: `GET https://<your-service>.onrender.com/spotdl?url=<spotify-or-youtube-url>`

## Notes & warnings
- Running `yt-dlp`/`spotdl` against copyrighted content may violate platform TOS.
- Free Render instances sleep and have limited CPU/RAM. Expect slower runs and possible throttling.
- Consider adding request validation, rate-limiting, authentication, and quotas before exposing to users.
