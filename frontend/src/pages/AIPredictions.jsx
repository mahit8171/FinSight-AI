
import { useState } from "react";
import {
  BrainCircuit,
  TrendingUp,
  Activity,
  ShieldAlert,
} from "lucide-react";

import PredictionCard from "../components/PredictionCard";

const STOCKS = [
  "RELIANCE",
  "TCS",
  "INFY",
  "HDFCBANK",
  "ICICIBANK",
];

function AIPredictions() {
  const [selectedStock, setSelectedStock] = useState("RELIANCE");

  return (
    <div className="ai-predictions-page">
      <div className="ai-page-header">
        <div>
          <span className="ai-eyebrow">MACHINE LEARNING</span>
          <h1>AI Predictions</h1>
          <p>
            Explore machine learning based stock return predictions.
          </p>
        </div>

        <div className="ai-header-icon">
          <BrainCircuit size={28} />
        </div>
      </div>

      {/* Overview */}
      <div className="ai-overview-grid">
        <div className="ai-overview-card">
          <BrainCircuit size={22} />
          <span>Trained Models</span>
          <h2>05</h2>
          <p>Individual stock prediction models</p>
        </div>

        <div className="ai-overview-card">
          <Activity size={22} />
          <span>Supported Stocks</span>
          <h2>05</h2>
          <p>Available for prediction</p>
        </div>

        <div className="ai-overview-card">
          <TrendingUp size={22} />
          <span>Prediction Horizon</span>
          <h2>1 Day</h2>
          <p>Next available trading day</p>
        </div>
      </div>

      {/* Stock selector */}
      <div className="ai-stock-selector-section">
        <div>
          <h2>Select Stock</h2>
          <p>Choose a stock to view its AI prediction.</p>
        </div>

        <div className="ai-stock-buttons">
          {STOCKS.map((symbol) => (
            <button
              key={symbol}
              className={
                selectedStock === symbol ? "active" : ""
              }
              onClick={() => setSelectedStock(symbol)}
            >
              {symbol}
            </button>
          ))}
        </div>
      </div>

      {/* Selected prediction */}
      <div className="ai-prediction-result">
        <PredictionCard symbol={selectedStock} />
      </div>

      {/* All stock predictions */}
      <div className="ai-all-stocks-section">
        <div className="ai-section-heading">
          <div>
            <h2>All Stock Predictions</h2>
            <p>
              Compare AI predictions across supported stocks.
            </p>
          </div>
        </div>

        <div className="ai-prediction-grid">
          {STOCKS.map((symbol) => (
            <div key={symbol} className="ai-mini-prediction">
              <div>
                <strong>{symbol}</strong>
                <span>ML Prediction Model</span>
              </div>

              <button
                onClick={() => {
                  setSelectedStock(symbol);
                  window.scrollTo({
                    top: 0,
                    behavior: "smooth",
                  });
                }}
              >
                View Prediction
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="ai-disclaimer">
        <ShieldAlert size={22} />
        <div>
          <h3>Important Risk Disclaimer</h3>
          <p>
            These predictions are experimental machine learning
            outputs based on historical data. They are not
            financial advice and do not guarantee future returns.
            Always conduct your own research before making
            investment decisions.
          </p>
        </div>
      </div>
    </div>
  );
}

export default AIPredictions;
