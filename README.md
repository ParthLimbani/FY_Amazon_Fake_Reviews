# Fake Review Detection System

> A production-ready web application that detects fake Amazon reviews using Machine Learning and NLP.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

## 🎯 Project Overview

This system analyzes Amazon product reviews to identify fake or incentivized reviews, helping consumers make informed purchasing decisions. It uses a hybrid approach combining rule-based heuristics with machine learning for accurate and explainable results.

### Key Features

- **Real Review Analysis**: Fetches actual reviews via Bright Data API
- **ML-Powered Detection**: TF-IDF + Logistic Regression with rule-based enhancements
- **Explainable Results**: Clear reasons for each classification
- **Comprehensive Metrics**: Fake percentage, adjusted ratings, authenticity grades
- **Modern Dashboard**: React-based UI with visualizations

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend │────▶│  FastAPI Backend │────▶│  Bright Data API │
│   (Vite + TailwindCSS) │     │  (Python)         │     │  (Reviews)        │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                        ┌────────▼────────┐
                        │   ML Pipeline    │
                        │  - Preprocessor  │
                        │  - Classifier    │
                        │  - Aggregator    │
                        └─────────────────┘
```

## 📁 Project Structure

```
fake_review_v2/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bright_data_service.py  # Bright Data integration
│   │   └── analysis_service.py     # Analysis orchestration
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── preprocessor.py    # Text cleaning & feature extraction
│   │   ├── classifier.py      # ML classification model
│   │   └── aggregator.py      # Results aggregation
│   ├── utils/
│   │   ├── __init__.py
│   │   └── asin_extractor.py  # Amazon URL parsing
│   ├── main.py                # FastAPI application
│   ├── config.py              # Configuration
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components
│   │   ├── charts/            # Chart components
│   │   ├── services/          # API service
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Bright Data API token (for real data)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Edit .env and add your Bright Data API token

# Run server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Visit `http://localhost:5173` to use the application.

## 🧠 Fake Review Detection Logic

### Signals Detected

#### Text-Based Signals
- Excessive positivity without specifics
- Short, generic reviews
- Marketing language patterns
- Repetitive phrases
- Sentiment-rating mismatch

#### Metadata Signals
- Unverified purchases
- Extreme ratings (1 or 5 stars)
- Low specificity score

### Classification Approach

1. **Rule-Based Scoring**: Applies heuristics for known fake patterns
2. **ML Model**: TF-IDF + Logistic Regression for complex cases
3. **Hybrid Combination**: Weighted combination for final score

### Output Format

```json
{
  "label": "genuine | fake",
  "confidence": 0.85,
  "reasons": [
    "Unverified purchase",
    "Short, generic review"
  ]
}
```

## 📊 Metrics Computed

| Metric | Description |
|--------|-------------|
| Total Reviews | Number of reviews analyzed |
| Fake Percentage | Proportion of suspicious reviews |
| Original Rating | Average rating of all reviews |
| Adjusted Rating | Rating excluding fake reviews |
| Authenticity Grade | A-F grade based on fake % |

### Grading Scale

| Grade | Fake % | Interpretation |
|-------|--------|----------------|
| A | <5% | Excellent authenticity |
| B | 5-15% | Good authenticity |
| C | 15-30% | Moderate concerns |
| D | 30-50% | Significant issues |
| F | >50% | Poor authenticity |

## 🔌 API Reference

### POST /api/analyze

Analyze reviews for a product.

**Request:**
```json
{
  "url": "https://www.amazon.in/dp/B08N5WRWNW"
}
```

**Response:**
```json
{
  "success": true,
  "asin": "B08N5WRWNW",
  "product_title": "Product Name",
  "metrics": {
    "total_reviews": 150,
    "fake_percentage": 25.3,
    "authenticity_grade": "C"
  },
  "reviews": [...]
}
```

### GET /api/demo

Get demo analysis for testing.

### GET /api/health

Health check endpoint.

## 🎓 Academic Justification

### Why This Approach?

1. **Hybrid Model**: Combines interpretability of rules with pattern recognition of ML
2. **Explainability**: Each decision can be justified (important for academic evaluation)
3. **Modularity**: Easy to upgrade individual components
4. **Real Data**: Uses actual Amazon reviews via legitimate API

### Related Research

- Mukherjee et al. (2013) - "What Yelp Fake Review Filter Might Be Doing"
- Jindal & Liu (2008) - "Opinion Spam and Analysis"
- Ott et al. (2011) - "Finding Deceptive Opinion Spam"

### Ethical Considerations

This tool is designed to:
- Help consumers make informed decisions
- Highlight the prevalence of fake reviews
- Promote transparency in e-commerce

It should NOT be used to:
- Defame legitimate reviewers
- Make absolute judgments about review authenticity

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

This is a final year project. Contributions are welcome for educational purposes.

## 📧 Contact

For academic inquiries, please contact the project team.
