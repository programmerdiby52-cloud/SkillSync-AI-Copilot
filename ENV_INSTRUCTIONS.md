# SkillSync AI - .env Setup Instructions

To securely store API keys, you need to create a file named `.env` in the root directory of this project (the same folder as `app.py`).

1. Create a new text file and name it exactly `.env` (no filename before the dot).
2. Open the file and add your Google Gemini API key in the following format:

```env
GOOGLE_API_KEY="your_actual_api_key_here"
```

3. Save the file. The application will automatically load this key when running.
4. **Important**: Never commit your `.env` file to version control (e.g., GitHub). Make sure it's added to your `.gitignore` file if you are using git.
