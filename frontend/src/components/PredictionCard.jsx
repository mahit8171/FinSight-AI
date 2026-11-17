
import { useEffect, useState } from "react";
import {
  BrainCircuit,
  TrendingUp,
  TrendingDown,
} from "lucide-react";

import api from "../services/api";

function PredictionCard({ symbol }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPrediction = async () => {
      setLoading(true);
      setError("");
      setPrediction(null);

      try {
        const response = await api.get(
          `/ml-predictions/${symbol}`
        );

        setPrediction(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to fetch prediction"
        );
      } finally {
        setLoading(false);
      }
    };

    if (symbol) fetchPrediction();
  }, [symbol]);

  if (loading) {
    return <div className="prediction-card">Loading AI prediction...</div>;
  }

  if (error) {
    return <div className="prediction-card">{error}</div>;
  }

  if (!prediction) return null;

  const currentPrice = prediction.current_close;
  const predictedReturn = prediction.predicted_return;

  const predictedPrice =
    currentPrice * (1 + predictedReturn);

  const returnPercent =
    prediction.predicted_return_percent;

  const isPositive = returnPercent >= 0;

  const formatPrice = (price) =>
    `₹${price.toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;

  return (
    <div className="prediction-card">
      <div className="prediction-heading">
        <BrainCircuit size={24} />
        <h2>AI Prediction Analysis</h2>
      </div>

      <p className="prediction-symbol">{prediction.symbol}</p>

      <div className="prediction-grid">
        <div>
          <p>Current Price</p>
          <h3>{formatPrice(currentPrice)}</h3>
        </div>

        <div>
          <p>Predicted Price</p>
          <h3>{formatPrice(predictedPrice)}</h3>
        </div>

        <div>
          <p>Expected Return</p>

          <h3 className={isPositive ? "positive" : "negative"}>
            {isPositive ? "+" : ""}
            {returnPercent.toFixed(2)}%
          </h3>
        </div>
      </div>

      <div className={`prediction-signal ${isPositive ? "positive" : "negative"}`}>
        {isPositive ? (
          <TrendingUp size={20} />
        ) : (
          <TrendingDown size={20} />
        )}

        {isPositive ? "Positive Return Forecast" : "Negative Return Forecast"}
      </div>

      <div className="prediction-details">
        <p>Model: {prediction.model_name}</p>
        <p>Version: {prediction.model_version}</p>
        <p>Horizon: {prediction.prediction_horizon}</p>
      </div>

      <p className="prediction-disclaimer">
        {prediction.disclaimer}
      </p>
    </div>
  );
}

export default PredictionCard;
