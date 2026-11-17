
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  TrendingUp,
  TrendingDown,
  IndianRupee,
} from "lucide-react";

import api from "../services/api";

const STOCKS = [
  "RELIANCE",
  "TCS",
  "INFY",
  "HDFCBANK",
  "ICICIBANK",
];

function StockChart({ symbol, onSymbolChange }) {
  
  const [stockData, setStockData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStockHistory = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.get(
          `/stocks/${symbol}/history`,
          { params: { limit: 30 } }
        );

        const formattedData = response.data.data.map((item) => ({
          date: new Date(item.date).toLocaleDateString(
            "en-IN",
            { day: "2-digit", month: "short" }
          ),
          close: Number(item.close),
        }));

        setStockData(formattedData);
      } catch (err) {
        setStockData([]);
        setError("Unable to fetch stock data");
      } finally {
        setLoading(false);
      }
    };

    fetchStockHistory();
  }, [symbol]);

  const currentPrice = stockData.length
    ? stockData[stockData.length - 1].close
    : 0;

  const previousPrice = stockData.length > 1
    ? stockData[stockData.length - 2].close
    : 0;

  const dailyChange = currentPrice - previousPrice;

  const changePercent = previousPrice
    ? (dailyChange / previousPrice) * 100
    : 0;

  const formatPrice = (price) =>
    `₹${price.toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;

  return (
    <div className="stock-chart">
      <div className="chart-header">
        <h2>Stock Market Performance</h2>

         <select
        value={symbol}
        onChange={(e) => onSymbolChange(e.target.value)}
        >
          {STOCKS.map((stock) => (
            <option key={stock} value={stock}>
              {stock}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Loading stock data...</p>
      ) : error ? (
        <p>{error}</p>
      ) : stockData.length === 0 ? (
        <p>No stock data available.</p>
      ) : (
        <>
          <div className="stock-summary">
            <div className="summary-card">
              <div className="summary-label">
                <IndianRupee size={17} />
                Current Price
              </div>
              <h3>{formatPrice(currentPrice)}</h3>
            </div>

            <div className="summary-card">
              <div className="summary-label">
                Previous Close
              </div>
              <h3>{formatPrice(previousPrice)}</h3>
            </div>

            <div className="summary-card">
              <div className="summary-label">
                Daily Change
              </div>

              <h3 className={dailyChange >= 0 ? "positive" : "negative"}>
                {dailyChange >= 0 ? (
                  <TrendingUp size={18} />
                ) : (
                  <TrendingDown size={18} />
                )}

                {formatPrice(Math.abs(dailyChange))}
              </h3>

              <p className={dailyChange >= 0 ? "positive" : "negative"}>
                {changePercent >= 0 ? "+" : ""}
                {changePercent.toFixed(2)}%
              </p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={stockData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#26364e"
              />

              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />

              <Tooltip
                formatter={(value) => formatPrice(value)}
                contentStyle={{
                  background: "#111827",
                  border: "1px solid #26364e",
                  color: "#ffffff",
                }}
              />

              <Line
                type="monotone"
                dataKey="close"
                name="Closing Price"
                stroke="#38bdf8"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default StockChart;
