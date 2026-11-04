import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="navbar">
        <h2>FinSight AI</h2>

        <span className="status">
          System Online
        </span>
      </header>

      <main className="hero">
        <div className="tag">
          AI Powered Financial Intelligence
        </div>

        <h1>
          Welcome to <span>FinSight AI</span>
        </h1>

        <p>
          Intelligent financial analytics,
          stock forecasting and portfolio
          risk management platform.
        </p>

        <div className="cards">

          <div className="card">
            <h3>Stock Forecasting</h3>
            <p>Predict future market trends.</p>
          </div>

          <div className="card">
            <h3>Sentiment Analysis</h3>
            <p>Analyze financial news.</p>
          </div>

          <div className="card">
            <h3>Portfolio Analytics</h3>
            <p>Understand portfolio risks.</p>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;