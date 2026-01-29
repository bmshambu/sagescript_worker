# SageScript Worker - Test Case Generation

An intelligent test case generation system powered by AI that automatically generates unit and functional test cases for multiple programming languages.

## Overview

This worker processes jobs to generate comprehensive test cases using Google's Gemini AI models. It supports multiple programming languages and testing frameworks, providing both unit tests and functional tests with proper documentation and edge case coverage.

## Features

- **Multi-Language Support**: Python, JavaScript, TypeScript, Java
- **AI-Powered Generation**: Uses Google Gemini 2.5 Flash model
- **Test Framework Integration**: 
  - Python: unittest/pytest
  - JavaScript: Jest
  - TypeScript: Jest/Mocha
  - Java: JUnit
- **Job Queue Processing**: Redis-based queue (RQ) for background job processing
- **Database Integration**: PostgreSQL backend for job storage and tracking
- **REST API**: FastAPI endpoints for job submission and monitoring
- **RAG Pipeline**: Integrated retrieval-augmented generation for context-aware test generation

## Project Structure

```
sagescript_worker/
├── config.py                          # Application configuration
├── db.py                              # Database connection and utilities
├── worker.py                          # RQ worker entry point
├── rq_config.py                       # RQ configuration
├── requirements.txt                   # Python dependencies
├── field_metadata.json                # Field metadata definitions
│
├── schemas/                           # Data models and constants
│   ├── test_case.py                   # Test case schema
│   ├── constants/
│   │   ├── system_prompt.py           # AI system prompts
│   │   ├── system_prompt_unit_test_case.py
│   │   ├── framework_prompts.py       # Framework-specific prompts
│   │   ├── output_format.py           # Output formatting specifications
│   │   ├── script_generation.py       # Script generation constants
│   │   └── examples.py                # Example test cases
│
├── tools/                             # Core tools and engines
│   └── ai_engine.py                   # AI test case generation engine
│
└── utils/                             # Utility functions
    ├── google_llm_handler.py          # Google LLM API integration
    ├── json_parse.py                  # JSON parsing utilities
    ├── language_detect.py             # Programming language detection
    ├── clone_repo.py                  # Repository cloning utilities
    ├── priority_summary.py            # Priority calculation
    ├── functional_test/               # Functional test generation
    │   ├── functional_test_case_generator_svc.py
    │   ├── functional_test_rag_pipeline.py
    │   └── graph_initialize_functional_test.py
    └── unit_test/                     # Unit test generation
        ├── unit_test_case_generator_svc.py
        ├── graph_initialize_unit_test.py
        └── test.ipynb
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sagescript_worker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `config.py`:
```python
- API_KEY: Google Gemini API key
- DATABASE_URL: PostgreSQL connection string
- MODEL_NAME: Gemini model to use (e.g., "gemini-2.5-flash")
```

## Usage

### Starting the Worker

```bash
python worker.py
```

This will start the RQ worker that listens for test case generation jobs from the Redis queue.

### Generating Test Cases

#### Unit Tests
```python
from utils.unit_test.unit_test_case_generator_svc import generate_unit_tests

test_cases = generate_unit_tests(
    code_snippet="your code here",
    language="Python",
    framework="pytest"
)
```

#### Functional Tests
```python
from utils.functional_test.functional_test_case_generator_svc import generate_functional_tests

test_cases = generate_functional_tests(
    code_snippet="your code here",
    language="JavaScript",
    framework="Jest"
)
```

## Configuration

### Database Setup
The application uses PostgreSQL. Configure the connection string in `config.py`:
```python
self.database_url = "postgresql://user:password@host:port/database"
```

### AI Model Configuration
Configure the Gemini model in `config.py`:
```python
self.model_name = "gemini-2.5-flash"
self.api_key = "your-google-ai-key"
```

## Dependencies

Core dependencies:
- **redis** (>=5.0.0) - Redis client
- **rq** (>=1.15.0) - Job queue system
- **fastapi** (>=0.70.0) - REST API framework
- **uvicorn** (>=0.15.0) - ASGI server
- **langchain_google_genai** - Google AI integration
- **langgraph** (==0.3.2) - Graph-based workflow
- **sentence-transformers** - Text embedding for RAG
- **psycopg** - PostgreSQL adapter
- **streamlit** - Web UI

## Architecture

### Job Processing Flow
1. Job is submitted to Redis queue
2. Worker picks up job and marks it as `PROCESSING`
3. Framework choice is fetched from database
4. AI engine generates test cases based on code and framework
5. Results are stored back in PostgreSQL
6. Job status is updated to `COMPLETED`

### RAG Pipeline
The system uses a retrieval-augmented generation pipeline to:
- Search for similar test cases
- Leverage historical context
- Generate more relevant and consistent test cases

## API Endpoints

The FastAPI server provides endpoints for:
- Submitting test generation jobs
- Retrieving job status
- Fetching generated test cases
- Monitoring worker activity

## Testing

A Jupyter notebook for testing is available at:
```
utils/unit_test/test.ipynb
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues and questions, please open an issue in the repository.
