
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";
import StockChart from "../components/StockChart";
import PredictionCard from "../components/PredictionCard";

import api from "../services/api";

function StockDetails() {
  const { symbol } = useParams();

  const [stock, setStock] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStockDetails = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.get(
          `/stocks/${symbol}/history/latest`
        );

        setStock(response.data.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to fetch stock details"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchStockDetails();
  }, [symbol]);

  if (loading) return <p>Loading stock details...</p>;
  if (error) return <p>{error}</p>;
  if (!stock) return <p>No stock data available.</p>;

  return (
    <div className="stock-details-page">
      <h1>{symbol} Stock Details</h1>

      <div className="stock-details-grid">
        <div className="detail-card">
          <p>Open Price</p>
          <h2>₹{stock.open.toFixed(2)}</h2>
        </div>

        <div className="detail-card">
          <p>High Price</p>
          <h2>₹{stock.high.toFixed(2)}</h2>
        </div>

        <div className="detail-card">
          <p>Low Price</p>
          <h2>₹{stock.low.toFixed(2)}</h2>
        </div>

        <div className="detail-card">
          <p>Closing Price</p>
          <h2>₹{stock.close.toFixed(2)}</h2>
        </div>

        <div className="detail-card">
          <p>Trading Volume</p>
          <h2>{stock.volume.toLocaleString("en-IN")}</h2>
        </div>
      </div>

      <div className="detail-card">
        <Activity size={22} />
        <p>Latest Trading Date</p>
        <h3>{new Date(stock.date).toLocaleDateString("en-IN")}</h3>
      </div>

      <StockChart
        symbol={symbol}
        onSymbolChange={() => {}}
        />
      <PredictionCard symbol={symbol} />
    </div>
  );
}

export default StockDetails;
