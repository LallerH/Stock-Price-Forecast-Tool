# 📈 Stock Price Forecasting Project

## 🚀 **Project Overview**
This is a portfolio project, the function of which is to search for similar patterns in historical stock price data to the recent one and with the help of it, try to make projection for the future. 

**Key Technologies**:
- **Python Libraries**: `Pandas`, `Pandas_ta`, `Matplotlib`, `Yfinance`, `PyQt`
- **Database**: MongoDB
- **Visualization**: candlestick charts, histograms, box plots


## ⚙️ **Features**

### 📥 **Data Pipeline**
- **Automated Data Collection**: Fetch historical data from Yahoo Finance
- **Feature Engineering**: Expand DataFrames with technical indicators
- **Database Integration**: Store/retrieve data via MongoDB

### 🔍 **Pattern Analysis**
- **Similarity Search**: Identify historical patterns matching current trends
  - Adjustable time windows
  - Customizable tolerance thresholds
- **Statistical Evaluation**: Quantify pattern significance

### 📊 **Insights & Forecasting**  
- **Visualizations**:  
  Histograms | Box Plots | Candlestick Charts  
- **Probabilistic Forecasts**:  
  Next-day price range predictions


## 🛠️ **Installation and usage**  
1. Clone repository  
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Required database manager: MongoDB (mongodb://localhost:27017)
4. Run stock_price_forecast.py