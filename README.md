
# Job Description Analyzer & Resume Scoring System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai)](https://openai.com/)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

An AI-powered solution for automated job application processing, featuring:
- 📄 Job Description Criteria Extraction
- 📊 Resume Scoring System
- 📈 Excel Report Generation

## Features

### Task 1: Criteria Extraction
- ✅ PDF/DOCX file support
- 🔍 Key requirement identification
- 🚀 GPT-4/3.5 powered analysis
- 📦 Structured JSON output

### Task 2: Resume Scoring
- 📑 Bulk resume processing
- 🎯 Criteria-based scoring (0-5 scale)
- 📊 Excel/CSV report generation
- ⚡ Async processing

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/job-analyzer.git
cd job-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create `.env` file:
```ini
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Start Server
```bash
uvicorn main:app --reload
```

Access Swagger UI at `http://localhost:8000/docs`

### API Endpoints

#### 1. Extract Criteria
```bash
curl -X POST -F "file=@job_description.pdf" http://localhost:8000/extract-criteria
```

#### 2. Score Resumes
```bash
curl -X POST \
-F "criteria=Python" \
-F "criteria=Machine Learning" \
-F "files=@resume1.pdf" \
-F "files=@resume2.docx" \
http://localhost:8000/score-resumes \
-o results.xlsx
```

## Project Structure
```
.
├── main.py             # FastAPI application
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── samples/            # Example files
│   ├── job_description.pdf
│   └── resume_sample.docx
└── README.md           # This document
```

## Documentation

### Request Formats
```json
// Extract Criteria
{
"file": "PDF/DOCX file"
}

// Score Resumes
{
"criteria": ["list", "of", "requirements"],
"files": ["resume1.pdf", "resume2.docx"]
}
```

### Response Samples
```json
// Criteria Extraction
{
"criteria": [
  "5+ years Python experience",
  "Machine Learning expertise",
  "AWS certification"
]
}
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details

---
**Note**: OpenAI API costs may apply. Monitor usage at [OpenAI Dashboard](https://platform.openai.com/usage)
