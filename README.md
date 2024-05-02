This is a portfolio project, the planned function of which is to find similar patterns in historical stock price data to the recent one and with the help of it, try to make some projections for the future. Whether correlation exists or not, this task is perfect to develop Python skills, using such libraries as Pandas, Pandas_ta, Matplotlib, Yfinance and MongoDB to store data. Planned functionality:
- collecting data from Yahoo Finance
- expanding DataFrame with indicators required
- storing data
- visualizing data with candlestick diagram
- processing data: searching for historical patterns similar with the current one (for certain periods, for certain tolerance margins)
- processing, evaluating and visualizing result
- forecasting future price (candlestick) with certain probability

Version of Python libraries used in the development:
(pip install -r requirements.txt)
- matplotlib / 3.8.4
- pandas / 2.2.1
- pandas_ta / 0.3.14b0
- pymongo / 4.6.3
- yfinance/ 0.2.37

Required database manager: MongoDB (mongodb://localhost:27017)