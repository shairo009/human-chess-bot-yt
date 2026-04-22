# YouTube Ninja Guide: Stay Safe & Grow Fast 🚀

To make your channel look 100% human and avoid being flagged as a "bot channel", follow these **Ninja Tactics**:

## 1. The "First 5" Rule
> [!IMPORTANT]
> **Don't automate the first 5 videos.**
> Upload them manually via the YouTube Studio mobile app. This builds initial "Human Trust" with YouTube's algorithm.

## 2. Posting Randomization
- **Don't post at the exact same time every day.**
- Use the `gap_hours` in `config.json` but occasionally change it (e.g., sometimes 2 hours, sometimes 4 hours).
- **Human behavior is unpredictable; bot behavior is a pattern.**

## 3. Engagement (Crucial) 💬
- YouTube tracks if a creator replies to comments.
- **Action:** Reply to at least 2-3 comments on every video. Use Hinglish slang like "Bhai ye toh next level tha!" or "Thanks for watching!".

## 4. Content Policy Guardrails 🛡️
- **No Profanity:** We have set the bot to be "Aggressive" but "Clean". Never manually add gaali/bad words in titles or descriptions.
- **Shorts Loop:** YouTube Shorts work best when they loop. Our scripts are designed to have a strong hook that makes people watch twice.

## 5. Thumbnail Customization
- Occasionally change the "Theme" in `config.json` (brown, green, blue) so the chess board looks different across videos.

## 6. Description Optimization
- Our bot adds a "NCS Credit" and hashtags automatically. 
- **Pro Tip:** Occasionally add a link to a related video or a "Subscribe" call-to-action manually in the first 24 hours.

---

### How to run safely:
1. Fill `.env` with your keys.
2. Run `python setup_youtube_token.py` (One time).
3. Run `python main.py --single` for the first few videos to review them.
4. Once you are happy, run `python main.py` for full automation.
