# GenAI Risk Mirror: Smart Risk Assessment for Health & Finance

An AI-powered personalized risk assessment platform providing comprehensive, domain-specific health and financial risk analysis with professional PDF report generation.

-----

## Project Overview

This web application uses cutting-edge Generative AI (powered by **AI21 Labs**) to analyze personal health or financial data provided by a user. It then creates detailed "**Risk Mirror**" reports that include a risk score, a complete analysis, personalized recommendations, and expert insights. The reports are generated as professionally formatted **PDF documents**, branded for MUFG.

-----

## Features

  - **Generative AI-powered analysis** for both health and finance risk domains.
  - Dynamic **personalized risk scoring** based on user data.
  - An intuitive and responsive **web UI** for data input.
  - On-demand generation of **professional PDF reports** with custom sections and branding.
  - Downloadable reports with clear, meaningful filenames.
  - A persistence-ready backend architecture with optional MongoDB support.
  - A clear, modular Python **Flask** backend integrating the AI21 API and **ReportLab**.

-----

## Technology Stack

  - **Backend**: Python, Flask framework
  - **AI**: AI21 Labs' Jamba-large language model via the AI21 Python SDK
  - **PDF Generation**: ReportLab library
  - **Frontend**: HTML, CSS (custom), JavaScript
  - **Database** (optional): MongoDB
  - **Environment Management**: `dotenv` for API keys and configuration

-----

## Project Structure

```
/app.py              # Main Flask backend app
/config.py           # Configuration management (API keys, DB URI)
/database.py         # MongoDB helper functions (optional)
/static/
├── css/         # Stylesheets (e.g., style.css)
└── js/          # JavaScript files (e.g., script.js)
/templates/
└── index.html   # Main web UI template
/.env                # Environment variables including AI21_API_KEY
/README.md           # This project documentation file
```

-----

## Setup & Installation

### 1\. Clone the repository

```bash
git clone https://github.com/deep-khimani/GenAI-Risk-Mirror-Smart-Risk-Assessment-for-Health-Finance.git
cd "GenAI-Risk-Mirror-Smart-Risk-Assessment-for-Health-Finance"
```

### 2\. Create and activate a Python virtual environment

```bash
# Create the virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set environment variables

Create a `.env` file in the project's root directory and add the following:

```
AI21_API_KEY=your_ai21_api_key_here
MONGODB_URI=your_mongodb_uri_here     # Optional
DB_NAME=your_database_name_here       # Optional
```

### 5\. Run the application

```bash
python app.py
```
