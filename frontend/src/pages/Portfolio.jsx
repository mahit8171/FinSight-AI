
import { useEffect, useState } from "react";
import {
  Plus,
  BriefcaseBusiness,
  Trash2,
  Pencil,
  TrendingUp,
  TrendingDown,
  Wallet,
  X,
  RefreshCw,
} from "lucide-react";
import api from "../services/api";

function Portfolio() {
  const [portfolios, setPortfolios] = useState([]);
  const [stocks, setStocks] = useState([]);
  const [holdings, setHoldings] = useState([]);
  const [currentPrices, setCurrentPrices] = useState({});

  const [selectedPortfolioId, setSelectedPortfolioId] = useState("");
  const [loading, setLoading] = useState(true);
  const [holdingsLoading, setHoldingsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const [showHoldingForm, setShowHoldingForm] = useState(false);
  const [editingHolding, setEditingHolding] = useState(null);
  const [holdingForm, setHoldingForm] = useState({
    stock_id: "",
    quantity: "",
    average_buy_price: "",
  });

  const [savingHolding, setSavingHolding] = useState(false);

  // Fetch portfolios and stocks
  const fetchInitialData = async () => {
    setLoading(true);
    setError("");

    try {
      const [portfolioResponse, stockResponse] = await Promise.all([
        api.get("/portfolios/"),
        api.get("/stocks/"),
      ]);

      setPortfolios(portfolioResponse.data);
      setStocks(stockResponse.data);

      if (portfolioResponse.data.length > 0) {
        setSelectedPortfolioId((previous) =>
          previous || String(portfolioResponse.data[0].id)
        );
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load portfolio data"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInitialData();
  }, []);

  // Fetch holdings for selected portfolio
  const fetchHoldings = async () => {
    if (!selectedPortfolioId) {
      setHoldings([]);
      return;
    }

    setHoldingsLoading(true);
    setError("");

    try {
      const response = await api.get(
        `/portfolios/${selectedPortfolioId}/holdings/`
      );

      setHoldings(response.data);

      // Fetch current price for each stock
      const priceResults = await Promise.all(
        response.data.map(async (holding) => {
          const stock = stocks.find(
            (item) => item.id === holding.stock_id
          );

          if (!stock) return [holding.stock_id, null];

          try {
            const priceResponse = await api.get(
              `/stocks/${stock.symbol}/history/latest`
            );

            return [
              holding.stock_id,
              Number(priceResponse.data.data.close),
            ];
          } catch {
            return [holding.stock_id, null];
          }
        })
      );

      setCurrentPrices(Object.fromEntries(priceResults));
    } catch (err) {
      setHoldings([]);
      setError(
        err.response?.data?.detail || "Unable to fetch holdings"
      );
    } finally {
      setHoldingsLoading(false);
    }
  };

  useEffect(() => {
    if (stocks.length > 0 && selectedPortfolioId) {
      fetchHoldings();
    }
  }, [selectedPortfolioId, stocks]);

  // Create portfolio
  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const response = await api.post("/portfolios/", {
        name,
        description: description || null,
      });

      setName("");
      setDescription("");

      const updatedPortfolios = [...portfolios, response.data];
      setPortfolios(updatedPortfolios);
      setSelectedPortfolioId(String(response.data.id));
      setSuccess("Portfolio created successfully.");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to create portfolio"
      );
    }
  };

  // Delete portfolio
  const handleDeletePortfolio = async (id) => {
    if (!window.confirm("Are you sure you want to delete this portfolio?")) {
      return;
    }

    try {
      await api.delete(`/portfolios/${id}`);

      const remaining = portfolios.filter((item) => item.id !== id);
      setPortfolios(remaining);
      setSelectedPortfolioId(
        remaining.length ? String(remaining[0].id) : ""
      );
      setHoldings([]);
      setSuccess("Portfolio deleted successfully.");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete portfolio"
      );
    }
  };

  // Open add holding form
  const openAddHolding = () => {
    setEditingHolding(null);
    setHoldingForm({
      stock_id: "",
      quantity: "",
      average_buy_price: "",
    });
    setShowHoldingForm(true);
    setError("");
  };

  // Open edit holding form
  const openEditHolding = (holding) => {
    setEditingHolding(holding);
    setHoldingForm({
      stock_id: String(holding.stock_id),
      quantity: String(holding.quantity),
      average_buy_price: String(holding.average_buy_price),
    });
    setShowHoldingForm(true);
    setError("");
  };

  // Add or update holding
  const handleHoldingSubmit = async (e) => {
    e.preventDefault();

    if (!selectedPortfolioId) return;

    setSavingHolding(true);
    setError("");
    setSuccess("");

    const payload = {
      quantity: Number(holdingForm.quantity),
      average_buy_price: Number(holdingForm.average_buy_price),
    };

    try {
      if (editingHolding) {
        await api.patch(
          `/portfolios/${selectedPortfolioId}/holdings/${editingHolding.id}`,
          payload
        );
        setSuccess("Holding updated successfully.");
      } else {
        await api.post(
          `/portfolios/${selectedPortfolioId}/holdings/`,
          {
            ...payload,
            stock_id: Number(holdingForm.stock_id),
          }
        );
        setSuccess("Stock added to portfolio successfully.");
      }

      setShowHoldingForm(false);
      setEditingHolding(null);
      await fetchHoldings();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to save holding"
      );
    } finally {
      setSavingHolding(false);
    }
  };

  // Delete holding
  const handleDeleteHolding = async (holdingId) => {
    if (!window.confirm("Remove this stock from your portfolio?")) {
      return;
    }

    try {
      await api.delete(
        `/portfolios/${selectedPortfolioId}/holdings/${holdingId}`
      );

      setSuccess("Holding deleted successfully.");
      await fetchHoldings();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete holding"
      );
    }
  };

  // Portfolio calculations
  const totalInvestment = holdings.reduce(
    (total, holding) =>
      total + holding.quantity * holding.average_buy_price,
    0
  );

  const currentValue = holdings.reduce((total, holding) => {
    const price = currentPrices[holding.stock_id];

    return total + holding.quantity * (price ?? holding.average_buy_price);
  }, 0);

  const profitLoss = currentValue - totalInvestment;

  const profitLossPercent =
    totalInvestment > 0
      ? (profitLoss / totalInvestment) * 100
      : 0;

  const selectedPortfolio = portfolios.find(
    (item) => String(item.id) === selectedPortfolioId
  );

  const formatCurrency = (value) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(value || 0);

  if (loading) {
    return <div className="portfolio-page">Loading portfolio...</div>;
  }

  return (
    <div className="portfolio-page">
      <div className="portfolio-header">
        <div>
          <span className="portfolio-eyebrow">INVESTMENT MANAGEMENT</span>
          <h1>My Portfolio</h1>
          <p>Manage and track your stock investments.</p>
        </div>

        <button
          className="portfolio-primary-btn"
          onClick={openAddHolding}
          disabled={!selectedPortfolioId}
        >
          <Plus size={18} />
          Add Holding
        </button>
      </div>

      {error && <div className="portfolio-alert error">{error}</div>}
      {success && (
        <div className="portfolio-alert success">{success}</div>
      )}

      {/* Portfolio selector */}
      <div className="portfolio-toolbar">
        <div className="portfolio-select-wrapper">
          <BriefcaseBusiness size={19} />
          <select
            value={selectedPortfolioId}
            onChange={(e) => setSelectedPortfolioId(e.target.value)}
          >
            <option value="">Select Portfolio</option>
            {portfolios.map((portfolio) => (
              <option key={portfolio.id} value={portfolio.id}>
                {portfolio.name}
              </option>
            ))}
          </select>
        </div>

        <button
          className="portfolio-secondary-btn"
          onClick={() => {
            fetchHoldings();
            setSuccess("");
          }}
          disabled={!selectedPortfolioId || holdingsLoading}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      {/* Create portfolio */}
      <form className="portfolio-create-form" onSubmit={handleCreate}>
        <div>
          <h3>Create New Portfolio</h3>
          <p>Organize your investments into separate portfolios.</p>
        </div>

        <input
          type="text"
          placeholder="Portfolio name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          minLength={2}
          maxLength={100}
          required
        />

        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button type="submit" className="portfolio-secondary-btn">
          <Plus size={16} />
          Create
        </button>
      </form>

      {!selectedPortfolioId ? (
        <div className="portfolio-empty">
          <BriefcaseBusiness size={38} />
          <h3>No portfolio selected</h3>
          <p>Create a portfolio to start adding your stock holdings.</p>
        </div>
      ) : (
        <>
          {/* Selected portfolio info */}
          <div className="selected-portfolio-heading">
            <div>
              <h2>{selectedPortfolio?.name}</h2>
              <p>
                {selectedPortfolio?.description || "Your investment portfolio"}
              </p>
            </div>

            <button
              className="portfolio-delete-btn"
              onClick={() =>
                handleDeletePortfolio(Number(selectedPortfolioId))
              }
              title="Delete portfolio"
            >
              <Trash2 size={17} />
            </button>
          </div>

          {/* Summary cards */}
          <div className="portfolio-stats-grid">
            <div className="portfolio-stat-card">
              <div className="portfolio-stat-icon">
                <Wallet size={20} />
              </div>
              <span>Total Investment</span>
              <h2>{formatCurrency(totalInvestment)}</h2>
            </div>

            <div className="portfolio-stat-card">
              <div className="portfolio-stat-icon">
                <BriefcaseBusiness size={20} />
              </div>
              <span>Current Value</span>
              <h2>{formatCurrency(currentValue)}</h2>
            </div>

            <div className="portfolio-stat-card">
              <div className="portfolio-stat-icon">
                {profitLoss >= 0 ? (
                  <TrendingUp size={20} />
                ) : (
                  <TrendingDown size={20} />
                )}
              </div>
              <span>Total Profit / Loss</span>
              <h2 className={profitLoss >= 0 ? "positive" : "negative"}>
                {formatCurrency(profitLoss)}
              </h2>
              <small className={profitLoss >= 0 ? "positive" : "negative"}>
                {profitLossPercent.toFixed(2)}%
              </small>
            </div>

            <div className="portfolio-stat-card">
              <div className="portfolio-stat-icon">
                <TrendingUp size={20} />
              </div>
              <span>Total Holdings</span>
              <h2>{holdings.length}</h2>
            </div>
          </div>

          {/* Holdings table */}
          <div className="holdings-section">
            <div className="holdings-heading">
              <div>
                <h2>Stock Holdings</h2>
                <p>Your investments in this portfolio.</p>
              </div>

              <button
                className="portfolio-primary-btn"
                onClick={openAddHolding}
              >
                <Plus size={17} />
                Add Stock
              </button>
            </div>

            {holdingsLoading ? (
              <p className="portfolio-loading">Loading holdings...</p>
            ) : holdings.length === 0 ? (
              <div className="portfolio-empty">
                <BriefcaseBusiness size={36} />
                <h3>No holdings yet</h3>
                <p>Add your first stock to start tracking your investment.</p>
                <button
                  className="portfolio-primary-btn"
                  onClick={openAddHolding}
                >
                  <Plus size={17} />
                  Add First Stock
                </button>
              </div>
            ) : (
              <div className="holdings-table-wrapper">
                <table className="holdings-table">
                  <thead>
                    <tr>
                      <th>Stock</th>
                      <th>Quantity</th>
                      <th>Avg. Buy Price</th>
                      <th>Current Price</th>
                      <th>Investment</th>
                      <th>Current Value</th>
                      <th>Profit / Loss</th>
                      <th>Actions</th>
                    </tr>
                  </thead>

                  <tbody>
                    {holdings.map((holding) => {
                      const stock = stocks.find(
                        (item) => item.id === holding.stock_id
                      );

                      const price = currentPrices[holding.stock_id];
                      const investment =
                        holding.quantity * holding.average_buy_price;

                      const marketValue =
                        holding.quantity *
                        (price ?? holding.average_buy_price);

                      const pnl = marketValue - investment;

                      return (
                        <tr key={holding.id}>
                          <td>
                            <strong>{stock?.symbol || `Stock #${holding.stock_id}`}</strong>
                            <small>{stock?.company_name || "Unknown stock"}</small>
                          </td>
                          <td>{holding.quantity}</td>
                          <td>{formatCurrency(holding.average_buy_price)}</td>
                          <td>
                            {price !== null && price !== undefined
                              ? formatCurrency(price)
                              : "Unavailable"}
                          </td>
                          <td>{formatCurrency(investment)}</td>
                          <td>{formatCurrency(marketValue)}</td>
                          <td className={pnl >= 0 ? "positive" : "negative"}>
                            {price !== null && price !== undefined
                              ? formatCurrency(pnl)
                              : "Unavailable"}
                          </td>
                          <td>
                            <div className="holding-actions">
                              <button
                                onClick={() => openEditHolding(holding)}
                                title="Edit holding"
                              >
                                <Pencil size={16} />
                              </button>

                              <button
                                className="delete-action"
                                onClick={() => handleDeleteHolding(holding.id)}
                                title="Delete holding"
                              >
                                <Trash2 size={16} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}

      {/* Add / Edit holding modal */}
      {showHoldingForm && (
        <div className="holding-modal-overlay">
          <form
            className="holding-modal"
            onSubmit={handleHoldingSubmit}
          >
            <div className="holding-modal-heading">
              <div>
                <h2>{editingHolding ? "Edit Holding" : "Add Stock Holding"}</h2>
                <p>
                  {editingHolding
                    ? "Update your investment details."
                    : "Add a stock to your selected portfolio."}
                </p>
              </div>

              <button
                type="button"
                className="modal-close-btn"
                onClick={() => setShowHoldingForm(false)}
              >
                <X size={20} />
              </button>
            </div>

            <label>Stock</label>
            <select
              value={holdingForm.stock_id}
              onChange={(e) =>
                setHoldingForm({
                  ...holdingForm,
                  stock_id: e.target.value,
                })
              }
              required
              disabled={Boolean(editingHolding)}
            >
              <option value="">Select stock</option>
              {stocks.map((stock) => (
                <option key={stock.id} value={stock.id}>
                  {stock.symbol} - {stock.company_name}
                </option>
              ))}
            </select>

            <label>Quantity</label>
            <input
              type="number"
              min="0.000001"
              step="any"
              placeholder="Enter quantity"
              value={holdingForm.quantity}
              onChange={(e) =>
                setHoldingForm({
                  ...holdingForm,
                  quantity: e.target.value,
                })
              }
              required
            />

            <label>Average Buy Price (₹)</label>
            <input
              type="number"
              min="0.01"
              step="any"
              placeholder="Enter average buy price"
              value={holdingForm.average_buy_price}
              onChange={(e) =>
                setHoldingForm({
                  ...holdingForm,
                  average_buy_price: e.target.value,
                })
              }
              required
            />

            <div className="holding-modal-actions">
              <button
                type="button"
                className="portfolio-secondary-btn"
                onClick={() => setShowHoldingForm(false)}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="portfolio-primary-btn"
                disabled={savingHolding}
              >
                {savingHolding
                  ? "Saving..."
                  : editingHolding
                    ? "Update Holding"
                    : "Add Holding"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default Portfolio;
