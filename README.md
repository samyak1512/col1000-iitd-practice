# IIT Delhi COL1000 Practice Platform

LeetCode-style coding platform for the 22 COL1000 Practice Problems (IIT Delhi), with an in-browser Python 3.12 runner, sample + hidden test cases, progressive hints, step-by-step solutions, PDF viewer, Google OAuth Sign-In, and a live student leaderboard.

## Free Hosting Guide (No Credit Card Required)

### Option A: Render.com (Recommended, Free Tier)
1. Push this folder to a GitHub repository.
2. Go to [render.com](https://render.com), sign in with GitHub, and click **New + -> Blueprint** (or **Web Service**).
3. Select your repository — `render.yaml` is already configured (`python3 server.py`, Free plan).
4. Once deployed, copy your live URL (e.g. `https://col1000-iitd-practice.onrender.com`).
5. Add that URL to **Authorized JavaScript origins** in [Google Cloud Console](https://console.cloud.google.com/apis/credentials) for your OAuth Client ID so Google Sign-In works for all your friends.

### Option B: Hugging Face Spaces (Free Docker Tier)
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces) with **Docker** SDK.
2. Push this repository (uses the included `Dockerfile` on port `7860`).
3. Add your `https://<user>-<space>.hf.space` URL to Google Cloud Console **Authorized JavaScript origins**.
