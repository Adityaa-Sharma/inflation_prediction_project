# CPI-Based Inflation Prediction Project

## Project Overview
📈 This project aims to predict Consumer Price Index (CPI)-based inflation using time series forecasting techniques. The goal is to develop a model capable of accurately forecasting future inflation rates based on historical data.

## Data Collection
🔍 Data was collected from reliable sources such as RBI, Statista, and Moneycontrol using web scraping techniques. Selenium was used to navigate complex web structures, while BeautifulSoup was employed to extract relevant information.

## Data Preprocessing
🧹 The collected data underwent thorough cleaning and preprocessing to ensure accuracy and consistency. Techniques such as interpolation and regression were used to fill missing values, and lag features were developed to capture historical dependencies.

## Feature Selection
📊 Key parameters including Broad Money (M3), Repo Rate, Reverse Repo Rate, GDP Growth Rate, M2 Money, Unemployment Rate, and CPI were identified as influential factors for inflation prediction.

## Modeling Approach
⏰ The SARIMA (Seasonal ARIMA) modeling technique was chosen for its effectiveness in capturing both non-seasonal and seasonal components of time series data. The model was refined and tuned to achieve optimal performance, resulting in an impressive mean squared error (MSE) of 0.2527.

### Results
📉 The SARIMA model demonstrated robust performance in predicting CPI-based inflation, showcasing its effectiveness in capturing temporal patterns and seasonality.
- Regularization techniques further improved model performance, achieving a mean squared error of 0.2527.

### Tech Stack
🛠️ Python, Selenium, BeautifulSoup, Pandas, NumPy, Statsmodels

### Future Enhancements
💡 Incorporating domain knowledge for parameter selection to further enhance model accuracy.
- Increasing dataset size to capture more inherent patterns and improve predictions.

