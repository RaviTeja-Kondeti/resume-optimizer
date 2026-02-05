"""
Flask Application for Resume Optimizer
Main API server with endpoints for resume upload, optimization, and download
"""

import os
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from resume_parser import ResumeParser
from resume_optimizer import ResumeOptimizer
from pdf_generator import PDFGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize modules
resume_parser = ResumeParser()
resume_optimizer = ResumeOptimizer()
pdf_generator = PDFGenerator()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Resume Optimizer API is running'})


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """
    Optimize resume based on job description

    Expected form data:
    - resume_file: PDF or DOCX file
    - job_title: String
    - job_description: Text

    Returns:
    - Optimized resume as JSON
    """
    try:
        # Validate request
        if 'resume_file' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400

        file = request.files['resume_file']
        job_title = request.form.get('job_title', '')
        job_description = request.form.get('job_description', '')

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400

        if not job_title or not job_description:
            return jsonify({'error': 'Job title and description are required'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # Parse resume
        resume_text = resume_parser.parse_resume(file_path, file_extension)
        if not resume_text:
            os.remove(file_path)
            return jsonify({'error': 'Failed to parse resume'}), 500

        # Optimize resume using Claude API
        optimized_resume = resume_optimizer.optimize_resume(
            resume_text,
            job_title,
            job_description
        )

        if not optimized_resume:
            os.remove(file_path)
            return jsonify({'error': 'Failed to optimize resume'}), 500

        # Generate PDF
        output_filename = f"optimized_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        success = pdf_generator.generate_pdf(optimized_resume, output_path)

        # Clean up uploaded file
        os.remove(file_path)

        if not success:
            return jsonify({'error': 'Failed to generate PDF'}), 500

        # Return response with download URL
        return jsonify({
            'success': True,
            'message': 'Resume optimized successfully',
            'download_url': f'/api/download/{output_filename}',
            'optimized_data': optimized_resume
        })

    except Exception as e:
        print(f"Error in optimize_resume: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_resume(filename):
    """
    Download optimized resume PDF

    Args:
        filename: Name of the PDF file to download

    Returns:
        PDF file
    """
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='optimized_resume.pdf'
        )

    except Exception as e:
        print(f"Error in download_resume: {e}")
        return jsonify({'error': 'Failed to download file'}), 500


@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    """
    Clean up old files (optional endpoint for maintenance)
    """
    try:
        import time
        current_time = time.time()
        cleanup_age = 3600  # 1 hour

        # Clean uploads
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                if os.path.getmtime(file_path) < current_time - cleanup_age:
                    os.remove(file_path)

        # Clean outputs
        for filename in os.listdir(app.config['OUTPUT_FOLDER']):
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            if os.path.isfile(file_path):
                if os.path.getmtime(file_path) < current_time - cleanup_age:
                    os.remove(file_path)

        return jsonify({'success': True, 'message': 'Cleanup completed'})

    except Exception as e:
        print(f"Error in cleanup_files: {e}")
        return jsonify({'error': 'Cleanup failed'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
