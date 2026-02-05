# Quick Start Guide

Get your ATS Resume Optimizer running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Step 1: Set Up Backend

```bash
# Navigate to backend directory
cd resume-optimizer/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

## Step 2: Add Your API Key

Edit `backend/.env` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Step 3: Start the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

## Step 4: Open the Frontend

Open `frontend/index.html` in your web browser (double-click the file or drag it to your browser).

## Step 5: Use the Application

1. **Upload your resume** (PDF or DOCX)
2. **Enter the job title** you're applying for
3. **Paste the job description** from the job posting
4. Click **"Optimize My Resume"**
5. Wait 20-30 seconds for AI processing
6. **Download your optimized resume** as PDF

## Troubleshooting

### "Backend API is not running"
Make sure the Flask server is running on port 5000. Check the terminal for errors.

### "ANTHROPIC_API_KEY not found"
Ensure you created the `.env` file and added your API key.

### CORS errors in browser
The Flask backend has CORS enabled. If you still see errors, make sure the API_URL in index.html matches your backend URL (default: http://localhost:5000).

### File upload fails
Check that your resume is in PDF or DOCX format and under 16MB.

## Testing the Setup

Test the backend is working:

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "ok", "message": "Resume Optimizer API is running"}
```

## Next Steps

- Save your optimized resumes
- Try with different job descriptions
- Compare before/after versions
- Apply with confidence!

## Need Help?

Check the main [README.md](README.md) for detailed documentation and API usage.
