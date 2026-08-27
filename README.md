# American Option Pricing Engine & Greeks Valuation via Binomial Trees
**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement
Standard analytical Black-Scholes-Merton (BSM) formulations are incapable of pricing American-style options due to path-dependent early exercise features. Because optimal early exercise must be evaluated at every discrete point in time prior to expiration, continuous closed-form equations fail. This project develops a discrete-time Cox-Ross-Rubinstein (CRR) binomial lattice pricing and risk engine to accurately price American equity options and capture the early-exercise premium.

Accurate pricing and sensitivity quantification are critical for active derivatives trading desks. If contracts with early-exercise optionality are mispriced or hedged using European analytical approximations, the trading book incurs systematic hedge slippage and unhedged Greek exposures ($\Delta, \Gamma, \Theta$), exposing the portfolio to severe market risk and drawdown.

## Stakeholder & User
* **Decision Owner:** Senior Portfolio Manager / Lead Options Trader / Equity Derivatives Desk Head. Responsible for portfolio risk limits, capital allocation, dynamic delta-hedging strategies, and relative-value trade execution.
* **Tool Operator:** Desk Quant / Quantitative Trading Analyst. Responsible for configuring model parameters, calibrating implied volatility surfaces, running batch chain valuations, and monitoring daily risk reports.
* **Timing & Workflow:** Daily end-of-day valuation and intra-day batch re-pricing across active options chains to flag market mispricings and quantify net Greek exposures.

## Useful Answer & Decision
* **Descriptive / Valuation (Primary):** Computes theoretical fair values and Greek risk sensitivities ($\Delta, \Gamma, \Theta, \mathcal{V}, \rho$) conditional on prevailing spot prices, strikes, interest rates, and calibrated implied volatility.
* **Predictive / Comparative (Secondary):** Evaluates market pricing efficiency by tracking market-versus-model divergence across the volatility surface.
* **Evaluation Metrics:** Pricing Error Root Mean Squared Error (RMSE) and Mean Absolute Percentage Error (MAPE) against live market mid-prices.
* **Deliverable Artifacts:** A modular Python CRR binomial tree library (`src/pricer.py`), an interactive valuation notebook, and a volatility/Greeks risk summary dashboard.

## Assumptions & Constraints
* **Mathematical & Model Assumptions:**
  * Risk-free interest rates ($r$) and asset volatility ($\sigma$) remain constant over the life of each specific option contract.
  * Underlying asset prices follow a recombining binomial lattice (CRR) governed by constant risk-neutral up ($u$) and down ($d$) transition probabilities.
  * Frictionless markets with zero transaction costs, bid-ask spread frictions, or short-selling constraints.
* **Data Constraints:**
  * Ingestion relies on publicly accessible market data (e.g., `yfinance`), which exhibits quote latency (15-minute delay) and missing discrete dividend schedules.
  * Real-world options chains contain noise, including illiquid strikes, wide bid-ask spreads, and zero-volume contracts that require robust filtering.
* **Computational Constraints:**
  * Lattice computation scales quadratically with depth ($\mathcal{O}(N^2)$ time complexity), necessitating a step budget ($N = 100\text{--}250$) to balance valuation precision with processing speed.

## Known Unknowns / Risks
* **Volatility Smile Misspecification:** A standard single-volatility CRR lattice assumes flat volatility across strikes. *Mitigation:* Calibrate strike-specific implied volatilities and monitor pricing RMSE across moneyness buckets.
* **Discretization Error & Greek Oscillation:** Discrete tree depth ($N$) introduces numerical oscillations in delta and gamma estimates. *Mitigation:* Benchmark model output against closed-form European Black-Scholes formulas for convergence validation ($< \$0.01$ tolerance).
* **Illiquid / Stale Market Data:** Zero-bid and deep OTM quotes corrupt implied volatility calculations. *Mitigation:* Implement automated pre-processing data filters to drop contracts with zero volume or bid-ask spreads exceeding $20\%$.

## Lifecycle Mapping
* **Define Valuation Scope & Desk Requirements** → Problem Framing & Scoping (Stage 01) → Scoping document in `README.md` and Stakeholder Memo in `docs/stakeholder_memo.md`
* **Scaffold Project Architecture & Environment** → Tooling Setup (Stage 02) → Project folder tree (`data/`, `src/`, `notebooks/`, `docs/`) and `requirements.txt`
* **Implement Analytical Pricing Baselines** → Python Fundamentals (Stage 03) → Vectorized Black-Scholes benchmark and mathematical utility functions in `src/utils.py`
* **Acquire & Persist Market Chains** → Data Acquisition & Storage (Stages 04–05) → Pipeline fetching raw options chains into `data/raw/` (Parquet/CSV)
* **Clean Chain Noise & Model Volatility Smile** → Preprocessing & EDA (Stages 06–07) → Filtered dataset in `data/processed/` and volatility skew visualization notebook
* **Build Binomial Lattice & Evaluate Risk** → Modeling & Risk Evaluation (Stages 08–09) → Reusable CRR pricing engine class (`src/pricer.py`) and pricing error RMSE report
* **Deploy Desk Pricing Tool** → Reporting & Productization (Stage 10+) → End-to-end pricing script with automated daily mispricing and risk summaries

## Repo Plan
* **Directory Structure:**
  * `data/`: Raw market downloads (`data/raw/`) and filtered options chains (`data/processed/`).
  * `src/`: Modular code base including data loaders (`src/data_loader.py`), utility functions (`src/utils.py`), and pricing classes (`src/pricer.py`).
  * `notebooks/`: Exploratory data analysis, convergence tests, and valuation workflows.
  * `docs/`: Technical documentation, stakeholder memos, and project framing slides.
* **Update Cadence:** Committed and pushed at each milestone following the course lifecycle stages.

## Data Storage

### Folder Structure
* `data/raw/`: Dedicated to storing raw, immutable incoming files (CSV format) directly as ingested from sources.
* `data/processed/`: Dedicated to persisting cleaned, typed, and structured datasets in optimized binary storage (Parquet format).

### Storage Formats & Rationale
* **CSV (`data/raw/`):** Human-readable, portable, and universal text format ideal for inspecting original ingested source data.
* **Parquet (`data/processed/`):** Columnar, compressed, and high-performance binary storage format that preserves native column data types (such as `datetime64` and numeric types) without precision loss and enables efficient read operations.

### Environment-Driven Path Routing
* Storage directories are resolved dynamically at runtime using `python-dotenv`:
  * `DATA_DIR_RAW`: Configured to `data/raw`
  * `DATA_DIR_PROCESSED`: Configured to `data/processed`
* Fallback defaults ensure cross-platform reproducibility even if environment variables are unset.

### Validation & Reusable Utilities
* **Validation Checks:** Every reloaded DataFrame is verified against the source for shape equivalence, datetime integrity on timestamp columns, and numeric type preservation.
* **I/O Utilities (`write_df`, `read_df`):** Automatically route file operations by extension (`.csv` vs `.parquet`), dynamically generate missing parent directories, and handle missing Parquet engines (`pyarrow`/`fastparquet`) with clear error messaging.

## Stage 06: Data Preprocessing Strategy & Assumptions

### 1. Imputation Strategy (`fill_missing_median`)
* **Mechanism:** Fills missing values in continuous numeric columns (`age`, `income`, `score`) using each column's calculated median.
* **Assumption:** Missingness is assumed to follow a Missing Completely at Random (MCAR) or Missing at Random (MAR) mechanism. The median is preferred over the mean to provide robustness against skewness and extreme outliers.

### 2. Filtering & Dropping Strategy (`drop_missing`)
* **Mechanism:** Evaluates row completeness and drops records containing fewer non-null values than the required threshold (e.g., $\ge 70\%$ non-null columns).
* **Tradeoff:** Sparse columns with high unobserved rates (`extra_data`) are eliminated to avoid introducing noisy imputation artifacts, trading a minor loss of observations for improved dataset integrity.

### 3. Feature Scaling & Normalization (`normalize_data`)
* **Mechanism:** Maps numeric features to the interval $[0, 1]$ using `MinMaxScaler`.
* **Assumption:** Assumes that observed minimums and maximums reflect true feature bounds. This standardizes magnitude scales across disparate financial metrics, preventing scale-dominant attributes from distorting downstream modeling.
