# Stakeholder Memo: American Option Pricing & Risk Engine

**To:** Equity Derivatives Trading Desk Head / Senior Portfolio Manager  
**From:** Quantitative Trading Analyst / Desk Quant  
**Date:** August 2026  
**Subject:** Binomial Tree Model Scoping for American Options Valuation & Greek Hedging  

---

### Executive Summary
Standard analytical Black-Scholes formulas fail to price American-style options because they cannot evaluate early-exercise optionality across discrete time horizons. Using European approximations to manage American option portfolios introduces systematic pricing inaccuracies and incorrect Greek sensitivities ($\Delta, \Gamma, \Theta$), resulting in unhedged market exposures. This project delivers a discrete-time Cox-Ross-Rubinstein (CRR) binomial lattice pricing and risk engine to calculate fair theoretical prices, early-exercise boundaries, and risk metrics for equity option portfolios.

### Key Objectives & Deliverables
* **Valuation & Early Exercise:** Implement a CRR lattice algorithm to determine fair values and early-exercise premiums for American puts and calls.
* **Risk Sensitivities:** Vectorize the computation of Greek exposures ($\Delta, \Gamma, \Theta, \mathcal{V}, \rho$) to support intra-day delta-neutral hedging.
* **Mispricing Detection:** Automate the ingestion of live options chains to quantify model-vs-market pricing error (RMSE/MAPE) across strike and maturity slices.

### Operational Constraints & Risk Management
* **Step Budget:** A step budget of $N = 100\text{--}250$ time steps will be utilized to balance $\mathcal{O}(N^2)$ computational complexity with valuation precision.
* **Data Quality:** Filtering rules will automatically remove illiquid strikes, inverted bid-ask spreads, and zero-volume quotes.
* **Model Validation:** Tree output will be continuously benchmarked against analytical Black-Scholes baselines on European options to ensure numerical convergence ($< \$0.01$ tolerance).
