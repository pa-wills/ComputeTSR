# ComputeTSR.py
A basic TSR computer that draws from a SQLite DB of positions and distributions.

The tool expects a sqlite3 database ./TSR.db. It processes the *Positions* table,
and attempts to compute the TSR of each. It builds this calculation by:

1. Scanning the *Distributions* table for any Distributions during the holding period;
2. Calculating the end price from either:
  * The sold price, for closed positions; or
  * The most recent closing price, recorded in the *ClosingPrices* table, for open positions.
3. And then writing the computed TSR into the *Performance* table.

## Command line usage / options
```
Usage: python computeTSR.py [OPTIONS]

Options:
    -f                  Specify the db's filename. Defaults to *TSR.db*
    -v                  Verbose mode.
    --refresh-prices    Grabs the latest closing prices from Yahoo Finance.
    --todays-date       Testing feature. Sets the current date.
```
