
import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown, Eye } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function StockMarket() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await api.get("/stocks/");
        setStocks(response.data);
      } catch (err) {
        setError("Unable to fetch stocks");
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  if (loading) return <p>Loading stocks...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="stock-market-page">
      <div className="page-heading">
        <h1>Stock Market</h1>
        <p>Explore available stocks and market information.</p>
      </div>

      <div className="stock-list">
        {stocks.map((stock) => (
          <div className="stock-item" key={stock.id}>
            <div>
              <h3>{stock.symbol}</h3>
              <p>{stock.company_name}</p>
              <span>{stock.sector || "N/A"}</span>
            </div>

            <button
              onClick={() =>
                navigate("/?stock=" + stock.symbol)
              }
            >
              <Eye size={17} />
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StockMarket;
