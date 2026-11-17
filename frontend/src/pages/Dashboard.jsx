
import {
  TrendingUp,
  BriefcaseBusiness,
  BrainCircuit,
  Activity,
  ArrowUpRight,
  Wallet,
  TrendingDown,
} from "lucide-react";

import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import StockChart from "../components/StockChart";
import PredictionCard from "../components/PredictionCard";
import api from "../services/api";

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(value || 0);

function Dashboard() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [selectedStock, setSelectedStock] = useState(
    (searchParams.get("stock") || "RELIANCE").toUpperCase()
  );

  const [portfolioStats, setPortfolioStats] = useState({
    investment: 0,
    currentValue: null,
    profitLoss: null,
    positions: 0,
  });

  const [portfolioLoading, setPortfolioLoading] = useState(true);

  const [marketAvailable, setMarketAvailable] = useState(true);

  // Fetch portfolio analytics
  useEffect(() => {
    const fetchPortfolioStats = async () => {
      setPortfolioLoading(true);

      try {
        const [portfolioResponse, stockResponse] = await Promise.all([
          api.get("/portfolios/"),
          api.get("/stocks/"),
        ]);

        const portfolios = portfolioResponse.data;
        const stocks = stockResponse.data;

        const stockMap = new Map(
          stocks.map((stock) => [stock.id, stock])
        );

        const holdingResponses = await Promise.all(
          portfolios.map((portfolio) =>
            api
              .get(`/portfolios/${portfolio.id}/holdings/`)
              .then((response) => response.data)
          )
        );

        const allHoldings = holdingResponses.flat();

        const investment = allHoldings.reduce(
          (total, holding) =>
            total + holding.quantity * holding.average_buy_price,
          0
        );

        const priceResults = await Promise.all(
          allHoldings.map(async (holding) => {
            const stock = stockMap.get(holding.stock_id);

            if (!stock) return null;

            try {
              const response = await api.get(
                `/stocks/${stock.symbol}/history/latest`
              );

              return {
                holdingId: holding.id,
                value:
                  holding.quantity *
                  Number(response.data.data.close),
              };
            } catch {
              return null;
            }
          })
        );

        const allPricesAvailable = priceResults.every(
          (result) => result !== null
        );

        const currentValue = allPricesAvailable
          ? priceResults.reduce(
              (total, result) => total + result.value,
              0
            )
          : null;

        setPortfolioStats({
          investment,
          currentValue,
          profitLoss:
            currentValue !== null
              ? currentValue - investment
              : null,
          positions: allHoldings.length,
        });
      } catch (error) {
        console.error("Portfolio analytics error:", error);

        setPortfolioStats({
          investment: 0,
          currentValue: null,
          profitLoss: null,
          positions: 0,
        });
      } finally {
        setPortfolioLoading(false);
      }
    };

    fetchPortfolioStats();
  }, []);

  const handleStockChange = (symbol) => {
    setSelectedStock(symbol);
    setSearchParams({ stock: symbol });
  };

  // Sync stock selection with URL
  useEffect(() => {
    const stockFromUrl = searchParams.get("stock");

    if (stockFromUrl) {
      setSelectedStock(stockFromUrl.toUpperCase());
    }
  }, [searchParams]);

  const overviewCards = [
    {
      title: "Supported Stocks",
      value: "05",
      description: "Stocks available for prediction",
      icon: TrendingUp,
    },
    {
      title: "Market Data",
      value: marketAvailable ? "Available" : "Unavailable",
      description: "Historical stock price data",
      icon: Activity,
    },
    {
      title: "Portfolio Value",
      value: portfolioLoading
        ? "Loading..."
        : portfolioStats.currentValue !== null
          ? formatCurrency(portfolioStats.currentValue)
          : "Unavailable",
      description: "Latest available stock prices",
      icon: BriefcaseBusiness,
    },
    {
      title: "AI Models",
      value: "05",
      description: "Trained stock prediction models",
      icon: BrainCircuit,
    },
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <div>
          <h1>Dashboard Overview</h1>
          <p>Welcome back! Here's your financial overview.</p>
        </div>

        <span className="dashboard-date">FinSight AI</span>
      </div>

      {/* Overview cards */}
      <div className="overview-grid">
        {overviewCards.map((card) => {
          const Icon = card.icon;

          return (
            <div className="overview-card" key={card.title}>
              <div className="card-top">
                <span>{card.title}</span>
                <Icon size={22} />
              </div>

              <h2>{card.value}</h2>
              <p>{card.description}</p>
            </div>
          );
        })}
      </div>

      {/* Portfolio analytics */}
      <div className="dashboard-section">
        <div className="section-heading">
          <h2>Portfolio Performance</h2>
          <BriefcaseBusiness size={20} />
        </div>

        <div className="portfolio-overview-grid">
          <div className="portfolio-overview-card">
            <Wallet size={20} />
            <span>Total Investment</span>
            <h2>
              {portfolioLoading
                ? "Loading..."
                : formatCurrency(portfolioStats.investment)}
            </h2>
          </div>

          <div className="portfolio-overview-card">
            <Activity size={20} />
            <span>Total Positions</span>
            <h2>
              {portfolioLoading ? "Loading..." : portfolioStats.positions}
            </h2>
          </div>

          <div className="portfolio-overview-card">
            {portfolioStats.profitLoss !== null &&
            portfolioStats.profitLoss >= 0 ? (
              <TrendingUp size={20} />
            ) : (
              <TrendingDown size={20} />
            )}

            <span>Total Profit / Loss</span>

            <h2
              className={
                portfolioStats.profitLoss === null
                  ? ""
                  : portfolioStats.profitLoss >= 0
                    ? "positive"
                    : "negative"
              }
            >
              {portfolioLoading
                ? "Loading..."
                : portfolioStats.profitLoss !== null
                  ? formatCurrency(portfolioStats.profitLoss)
                  : "Unavailable"}
            </h2>
          </div>
        </div>
      </div>

      {/* Market insights */}
      <div className="dashboard-section">
        <div className="section-heading">
          <h2>Market Insights</h2>
          <ArrowUpRight size={20} />
        </div>

        <p>
          Explore historical stock performance and AI-powered
          return predictions for supported stocks.
        </p>
      </div>

      {/* Stock chart */}
      <StockChart
        symbol={selectedStock}
        onSymbolChange={handleStockChange}
      />

      {/* AI prediction */}
      <PredictionCard symbol={selectedStock} />
    </div>
  );
}

export default Dashboard;
