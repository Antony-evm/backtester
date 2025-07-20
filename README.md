# Hawktrader Core - Open Source Backtesting Engine

This is the open-sourced core of **Hawktrader**, a backtesting platform for trading strategies. This simplified version provides the essential backtesting functionality while removing the complexity of the initial commercial platform.

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
- Docker
- TA-Lib

```bash
# Clone the repository
git clone https://github.com/Antony-evm/backtester.git
cd backtester

# Build and run with Docker Compose
docker compose build
docker compose up
```

The API will be available at `http://localhost:8080`
Docs can found under `http://localhost:8080/docs`

### Example Request Body

This example demonstrates a **Moving Average Crossover + RSI Filter Strategy**:

**Strategy Logic:**

- **BUY Signal**: When 7-period MA crosses above 21-period MA AND RSI > 20
- **SELL Signal**: When 7-period MA crosses below 21-period MA AND RSI < 80

```json
{
  "ticker_request": {
    "ticker": "MSFT",
    "start_date": "2000-01-01",
    "end_date": "2010-01-01",
    "interval": "1d"
  },
  "portfolio_management": {
    "starting_amount": 10000,
    "trade_size": {
      "value": 0.2,
      "type": "DYNAMIC"
    },
    "trade_targets": {
      "take_profit": 0.2,
      "stop_loss": -0.1
    }
  },
  "trading_system_rules": {
    "BUY": {
      "order_type_rule_id": "1",
      "group_rules": {
        "1": {
          "group_rule_id": "1",
          "rules": {
            "1": {
              "rule_id": "1",
              "first_property": {
                "type": "INDICATOR",
                "name": "MA",
                "parameters": {
                  "timeperiod": 7
                }
              },
              "comparison": {
                "value": "CROSSES_ABOVE"
              },
              "second_property": {
                "type": "INDICATOR",
                "name": "MA",
                "parameters": {
                  "timeperiod": 21
                }
              }
            }
          }
        },
        "2": {
          "group_rule_id": "2",
          "rules": {
            "2": {
              "rule_id": "2",
              "first_property": {
                "type": "INDICATOR",
                "name": "RSI",
                "parameters": {
                  "timeperiod": 7
                }
              },
              "comparison": {
                "value": "IS_ABOVE"
              },
              "second_property": {
                "type": "VALUE",
                "name": "value",
                "parameters": {
                  "value": 20
                }
              }
            }
          }
        }
      }
    },
    "SELL": {
      "order_type_rule_id": "2",
      "group_rules": {
        "3": {
          "group_rule_id": "3",
          "rules": {
            "3": {
              "rule_id": "3",
              "first_property": {
                "type": "INDICATOR",
                "name": "MA",
                "parameters": {
                  "timeperiod": 7
                }
              },
              "comparison": {
                "value": "CROSSES_BELOW"
              },
              "second_property": {
                "type": "INDICATOR",
                "name": "MA",
                "parameters": {
                  "timeperiod": 21
                }
              }
            }
          }
        },
        "4": {
          "group_rule_id": "4",
          "rules": {
            "4": {
              "rule_id": "4",
              "first_property": {
                "type": "INDICATOR",
                "name": "RSI",
                "parameters": {
                  "timeperiod": 7
                }
              },
              "comparison": {
                "value": "IS_BELOW"
              },
              "second_property": {
                "type": "VALUE",
                "name": "value",
                "parameters": {
                  "value": 80
                }
              }
            }
          }
        }
      }
    }
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

## Available Technical Indicators

The system supports various technical indicators through TA-Lib:

- Simple Moving Average (MA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)

Feel free to contribute further. Talib has several implemented.

## Learn More

I'm documenting the entire development process and architectural decisions on Medium. Follow and clap if you find it helpful!

**Article Series:**

- [Part 1 - Architecture](https://medium.com/@antony.evmo/building-a-backtesting-engine-with-fastapi-yfinance-and-ta-lib-part-1-b9ee02c2ceb5): Building a backtesting engine with FastAPI, yfinance and TA-Lib
- [Part 2 - Ticker Data](https://medium.com/@antony.evmo/building-a-backtesting-engine-with-fastapi-yfinance-and-ta-lib-part-2-18cce7342814): Implementing ticker data retrieval with yfinance

Each article explains the reasoning behind technical decisions, trade-offs, and lessons learned during development.

## Homage

Before diving into the code, please pay homage to the fallen:
🪦 [Visit the 404 Tomb](https://www.404tomb.com/tombstone/b3820b48-567b-4771-a1d4-ba841bf8fcc2)
