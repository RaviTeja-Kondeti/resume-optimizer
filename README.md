# ATS Resume Optimizer

An intelligent web application that tailors resumes to job descriptions using AI, making them ATS-friendly and optimized for interviews.

## Features

- **AI-Powered Optimization**: Uses Anthropic's Claude AI to analyze and tailor resumes
- **ATS-Friendly**: Ensures resumes pass Applicant Tracking Systems
- **Smart Formatting**:
  - ATR (Action-Task-Result) bullet points
  - Strong action verbs
  - Quantifiable metrics in every point
  - Professional summary in bullet format
- **PDF Generation**: Creates professionally formatted PDFs with specific styling:
  - Font: Times New Roman, 10.5pt
  - Margins: Top/Bottom: 0.5", Left/Right: 0.7"
  - Name in 14pt bold
- **File Support**: Upload PDF or DOCX resumes

## Project Structure

```
resume-optimizer/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── resume_parser.py       # PDF/DOCX parser
│   ├── resume_optimizer.py    # Claude AI integration
│   ├── pdf_generator.py       # PDF generation with formatting
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── uploads/              # Temporary upload directory
│   └── outputs/              # Generated PDF directory
└── frontend/                 # React frontend (to be added)
```

## Backend Setup

### Prerequisites

- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Navigate to backend directory**:
   ```bash
   cd resume-optimizer/backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

5. **Run the server**:
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "message": "Resume Optimizer API is running"
}
```

### 2. Optimize Resume
```http
POST /api/optimize
Content-Type: multipart/form-data
```

Parameters:
- `resume_file`: PDF or DOCX file
- `job_title`: Target job title (string)
- `job_description`: Job description text (string)

Response:
```json
{
  "success": true,
  "message": "Resume optimized successfully",
  "download_url": "/api/download/optimized_xxx.pdf",
  "optimized_data": {
    "name": "Full Name",
    "contact": {...},
    "professional_summary": [...],
    "professional_experience": [...],
    ...
  }
}
```

### 3. Download Optimized Resume
```http
GET /api/download/<filename>
```

Returns the generated PDF file.

## Testing the API

### Using cURL

```bash
curl -X POST http://localhost:5000/api/optimize \
  -F "resume_file=@/path/to/your/resume.pdf" \
  -F "job_title=Data Scientist" \
  -F "job_description=We are looking for an experienced Data Scientist..."
```

### Using Postman

1. Create a POST request to `http://localhost:5000/api/optimize`
2. Select "Body" → "form-data"
3. Add fields:
   - `resume_file`: File (select your resume PDF/DOCX)
   - `job_title`: Text (e.g., "Senior Software Engineer")
   - `job_description`: Text (paste the full job description)
4. Send the request
5. Use the `download_url` from the response to download the optimized resume

## Frontend Setup (Coming Soon)

The React frontend will be added when Node.js is available. The frontend will include:
- Drag-and-drop file upload
- Job title and description input form
- Preview of optimized resume
- One-click download

## How It Works

1. **Upload**: User uploads their current resume (PDF/DOCX)
2. **Input**: User provides job title and job description
3. **Parse**: System extracts text from the resume
4. **Optimize**: Claude AI analyzes the JD and tailors the resume:
   - Identifies key terms and requirements
   - Reformats bullet points in ATR format
   - Adds quantifiable metrics
   - Optimizes for ATS compatibility
   - Enhances professional summary
5. **Generate**: Creates a professionally formatted PDF
6. **Download**: User downloads the optimized resume

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `PORT` | Server port | `5000` |

## Key Features Implemented

- ✅ Resume parsing (PDF/DOCX)
- ✅ Claude AI integration
- ✅ ATR format bullet points
- ✅ Quantifiable metrics in every point
- ✅ Professional summary optimization
- ✅ ATS keyword optimization
- ✅ Custom PDF formatting (Times New Roman, specific margins)
- ✅ RESTful API
- ✅ File upload handling
- ✅ CORS support for frontend

## Next Steps

1. Install Node.js to enable React frontend development
2. Create UI components for file upload and form input
3. Add preview functionality
4. Implement responsive design
5. Add user authentication (optional)
6. Deploy to cloud platform

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Make sure you created a `.env` file and added your API key.

### "Command not found: python3"
Install Python from [python.org](https://www.python.org/downloads/)

### "Module not found" errors
Activate the virtual environment and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## License

MIT License - feel free to use this for your personal projects!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
