This is a portfolio project, the function of which is to search for similar patterns in historical stock price data to the recent one and with the help of it, try to make some sort of projection for the future. Whether correlation exists or not, this task is perfect to develop Python skills, using such libraries as Pandas, Pandas_ta, Matplotlib, Yfinance and MongoDB to store data. Functionality:
- collecting data from Yahoo Finance
- expanding DataFrame with indicators required
- storing data
- processing data: searching for historical patterns similar with the current one (for certain periods, for certain tolerance margins)
- evaluating and visualizing data with histogram, box plot and candlestick chart
- forecasting future (next day) price range with certain probability

See versions of Python libraries used in the project in requirements.txt.
(pip install -r requirements.txt)

Required database manager: MongoDB (mongodb://localhost:27017)

Usage:
- RUN stock_price_forecast.py
- SET MAIN DRIVER VARIABLES IN RAW 17-38 (such as stock /ticker/, analysed date, compared period, etc.)
