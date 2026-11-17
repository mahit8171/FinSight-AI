# FinSight AI

An AI-powered Financial Intelligence and Risk Analytics Platform.

## Features

- Stock Price Forecasting
- Financial News Sentiment Analysis
- Credit Risk Prediction
- Market Anomaly Detection
- Portfolio Risk Analytics
- Stock Recommendation System
- Financial Statement Analysis

## Technology Stack

- Python
- FastAPI
- React.js
- PostgreSQL
- Scikit-learn
- PyTorch
- MLflow
- DVC
- Docker
- AWS

## Architecture

Modular Monolith Architecture with separate data engineering, machine learning, backend and frontend layers.

## Project Status

Phase 1 – Foundation Setup

## Author

Mohit Kumar# FinSight AI 📈
### AI-Powered Stock Market Analytics & Prediction Platform

FinSight AI is a full-stack stock market analytics platform that combines machine learning, financial data analysis, and portfolio management to help users understand stock market trends and monitor their investments.

The platform provides stock market data, portfolio tracking, AI-based return predictions, and model experimentation through MLflow and DVC.

> **Note:** The machine learning models are currently experimental. Predictions are for educational and research purposes only and should not be considered financial advice.

---

## 🚀 Features

### 1. User Authentication
- User registration and login.
- JWT-based authentication.
- Protected routes.
- Persistent login sessions.

### 2. Dashboard
- Overview of supported stocks.
- Portfolio value and investment summary.
- Total positions and profit/loss.
- Stock market overview.
- AI prediction summary.

### 3. Stock Market
- View supported stocks.
- Explore stock details.
- View historical stock prices.
- Analyze OHLCV market data.

### 4. Portfolio Management
- Create and manage portfolios.
- Add stocks to portfolios.
- Update holding quantities and purchase prices.
- Delete holdings.
- Track total investment and current portfolio value.
- Monitor profit and loss.

### 5. AI Stock Predictions
- Machine learning-based return predictions.
- Predictions for five supported stocks.
- Predicted return and estimated price.
- Buy/Hold/Sell-style signal display.
- Model name and version information.

### 6. MLOps Integration
- ML experiment tracking using MLflow.
- Dataset and pipeline versioning using DVC.
- Reproducible model training pipeline.
- Separate model artifacts for supported stocks.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, Vite, JavaScript |
| UI & Styling | CSS, Lucide React |
| Charts | Recharts |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Machine Learning | Scikit-learn, Pandas, NumPy |
| Experiment Tracking | MLflow |
| Data Version Control | DVC |
| API Communication | Axios |
| Version Control | Git, GitHub |

---

## 🏗️ Project Architecture

```text
FinSight-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── ml/
│   │
│   ├── data/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── charts/
│   │   └── hooks/
│   │
│   └── package.json
│
├── dvc.yaml
├── params.yaml
├── .gitignore
└── README.md
```

---

## 📊 Supported Stocks

The current project supports the following stocks:

- RELIANCE
- TCS
- INFY
- HDFCBANK
- ICICIBANK

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have installed:

- Python 3.10+
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd FinSight-AI
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your backend environment variables in a `.env` file. Use your own PostgreSQL credentials and secret key. Never commit real credentials.

Run database migrations if Alembic is configured:

```bash
alembic upgrade head
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a `.env` file:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Start the frontend:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🤖 Machine Learning Pipeline

FinSight AI uses a machine learning pipeline to prepare financial data and train stock-specific prediction models.

### Workflow

1. Load historical stock market data.
2. Perform data preprocessing.
3. Generate technical indicators and features.
4. Prepare the prediction target.
5. Split the dataset chronologically into training and testing sets.
6. Train machine learning models.
7. Evaluate model performance.
8. Track experiments using MLflow.
9. Store dataset and pipeline versions using DVC.

### Feature Engineering

The current feature set includes:

- Daily Returns
- 5-Day Returns
- Rolling Volatility
- Volume Change
- Open/Close Ratio
- High/Close Ratio
- Low/Close Ratio
- SMA 5 Ratio
- SMA 10 Ratio
- EMA 20 Ratio
- RSI 14
- MACD
- MACD Histogram
- Momentum 10
- Bollinger Band Position

### Model Tracking

MLflow is used to track:
- Model parameters
- Evaluation metrics
- Experiments
- Model artifacts

To open the MLflow UI, start your configured MLflow tracking server and visit:

```text
http://127.0.0.1:5001
```

### DVC Pipeline

DVC manages dataset and pipeline versioning.

Useful commands:

```bash
dvc status
```

Reproduce the pipeline:

```bash
dvc repro
```

---

## 🔌 API Documentation

The backend exposes REST APIs through FastAPI.

| Module | Functionality |
|---|---|
| Authentication | Registration, login, current user |
| Stocks | Stock listing and details |
| Stock History | Historical price data |
| Portfolio | Portfolio CRUD operations |
| Holdings | Manage portfolio holdings |
| ML Predictions | Stock return predictions |

Explore all available endpoints through Swagger:

`http://127.0.0.1:8000/docs`

---

## 🔐 Security

- JWT-based authentication.
- Password hashing.
- Protected API endpoints.
- User-specific portfolio access.
- Environment variables for sensitive configuration.

Do not commit `.env` files, database passwords, JWT secrets, or other credentials.

---

## 🔮 Future Improvements

- Improve prediction accuracy through model experimentation.
- Add advanced models such as Random Forest, XGBoost and LSTM.
- Integrate real-time stock market data.
- Add interactive technical analysis indicators.
- Implement automated model retraining.
- Add model monitoring and performance tracking.
- Deploy the application using Docker and cloud infrastructure.

---

## ⚠️ Disclaimer

FinSight AI is an educational and experimental project. Stock predictions are generated by machine learning models and may be inaccurate. This platform does not provide financial or investment advice. Always conduct independent research before making investment decisions.

---

## 👨‍💻 Author

**Mohit Kumar**

B.Tech – Artificial Intelligence & Machine Learning

University of Lucknow

---

⭐ If you find this project interesting, consider giving it a star on GitHub!