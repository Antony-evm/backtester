# Hawktrader Core - Open Source Backtesting Engine

This is the open-sourced core of **Hawktrader**, a sophisticated backtesting platform for trading strategies. This simplified version provides the essential backtesting functionality while removing the complexity of the full commercial platform.

## What's Included

This open-source version contains:

- ✅ Core backtesting engine
- ✅ Technical indicator calculations (powered by TA-Lib)
- ✅ Trading signal generation
- ✅ Strategy evaluation and performance metrics
- ✅ REST API for backtesting operations
- ✅ Docker containerization

## What's Been Removed

To simplify the codebase and make it more accessible, the following components have been removed from the original Hawktrader platform:

- ❌ Database read/writes
- ❌ Microservices architecture (isolated TA-Lib for easier library upgrades)
- ❌ Authentication system
- ❌ Frontend interface
- ❌ Test suite (may cause some functionality issues - improvements planned)

## Known Areas for Improvement

This is a much simpler version of the original Hawktrader with some acknowledged technical debt:

- **Signals are tightly coupled** and hard to test independently
- **Enums should be replaced** with database lookup tables for better flexibility
- **Interface abstraction** has been simplified - the original version had more complex abstraction layers
- **Test coverage** has been removed and needs to be re-implemented

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)
- TA-Lib (Technical Analysis Library)

### Option 1: Run with Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd backtester

# Build and run with Docker Compose
docker-compose up --build
```

The API will be available at `http://localhost:8080`

### Option 2: Local Development Setup

1. **Install TA-Lib** (required for technical indicators):

   **Windows:**

   - Download TA-Lib from: http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip
   - Extract and follow installation instructions

   **macOS:**

   ```bash
   brew install ta-lib
   ```

   **Linux:**

   ```bash
   wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   tar -xzf ta-lib-0.4.0-src.tar.gz
   cd ta-lib/
   ./configure --prefix=/usr
   make
   sudo make install
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install TA-Lib
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## API Usage

### Endpoint

```
POST http://localhost:8080/api/v1/trading-systems/create
```

### Example Request Body

```json
{
  "ticker_request": {
    "symbol": "AAPL",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "interval": "1d"
  },
  "portfolio_management": {
    "initial_capital": 10000,
    "trade_size_type": "FIXED_AMOUNT",
    "trade_size_value": 1000
  },
  "trading_system_rules": {
    "entry_rules": [
      {
        "indicator": "SMA",
        "parameters": { "period": 20 },
        "comparison": "CROSS_ABOVE",
        "target_indicator": "SMA",
        "target_parameters": { "period": 50 }
      }
    ],
    "exit_rules": [
      {
        "indicator": "SMA",
        "parameters": { "period": 20 },
        "comparison": "CROSS_BELOW",
        "target_indicator": "SMA",
        "target_parameters": { "period": 50 }
      }
    ]
  }
}
```

### Testing with Postman

1. Open Postman
2. Create a new POST request
3. Set URL to: `http://localhost:8080/api/v1/trading-systems/create`
4. Set Content-Type header to: `application/json`
5. Add the example JSON above in the request body
6. Send the request

### Response

The API returns comprehensive backtesting results including:

- Performance metrics (returns, Sharpe ratio, max drawdown)
- Trade history
- Strategy statistics
- Execution metadata

## Project Structure

```
backtester/
├── api/                    # REST API layer
│   ├── requests/          # Request models
│   ├── responses/         # Response models
│   └── routes.py          # API endpoints
├── application/           # Business logic layer
│   ├── backtester.py      # Main backtesting engine
│   ├── indicator_service.py
│   ├── strategy_service.py
│   └── ...
├── domain/                # Domain models and enums
│   ├── enums/            # Trading enums
│   ├── indicators/       # Technical indicators
│   ├── signals/          # Trading signals
│   └── strategy/         # Strategy models
└── infrastructure/        # External services
    └── ticker_provider.py # Data provider
```

## Available Technical Indicators

The system supports various technical indicators through TA-Lib:

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- And many more...

## Contributing

This project is in active development. Contributions are welcome, especially in the following areas:

- Adding comprehensive test coverage
- Improving signal coupling and testability
- Implementing database lookup tables for enums
- Adding more sophisticated portfolio management features
- Performance optimizations

## License

[Add your license information here]

## Roadmap

- [ ] Restore comprehensive test suite
- [ ] Improve signal architecture for better testability
- [ ] Replace enums with database lookup tables
- [ ] Add more portfolio management strategies
- [ ] Performance optimizations
- [ ] Enhanced error handling and validation

## Support

This is an open-source version provided as-is. While we aim to ensure functionality, some features may not work 100% due to the removal of tests and simplified architecture.

For issues and feature requests, please use the GitHub issue tracker.
