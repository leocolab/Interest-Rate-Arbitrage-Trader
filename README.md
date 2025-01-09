# Interest-Rate-Arbitrage-Trader

Overview

This Python bot automates trading decisions on Polymarket by leveraging discrepancies between interest rate probabilities implied by the bond market and probabilities listed on Polymarket. It identifies profit opportunities using mean reversion strategies and Z-scores, dynamically adjusts thresholds based on expected volatility, and executes trades via the ClobClient API.

Profit Opportunity

The bot capitalizes on inefficiencies between bond market-implied probabilities and Polymarket betting odds. By analyzing spreads between these probabilities, it detects deviations from historical norms. Mean reversion strategies assume spreads tend to revert to average levels, creating buy or sell signals when outliers are detected. This approach exploits pricing inefficiencies to generate profit.

Volatility Weighting

Volatility weighting adjusts trading signals based on expected market fluctuations. Historical data is used to calculate rolling volatility and predict future volatility using a linear regression model. This prediction scales Z-scores dynamically, ensuring signals account for periods of higher uncertainty and reducing false positives during stable conditions.

Web Scraping

The bot gathers real-time data from:

Investing.com - Bond market probabilities are scraped using BeautifulSoup to assess rate decision expectations.

Polymarket - Betting odds are retrieved via Selenium to evaluate sentiment in prediction markets.
This dual-source approach enables accurate comparisons and timely updates, keeping trading decisions aligned with the latest market trends.

Features

Data Processing: Analyzes historical spreads and calculates volatility.

Signal Generation: Detects outliers using Z-scores adjusted for volatility.

Automated Trading Execution: Places trades directly on Polymarket based on calculated signals.
