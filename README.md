# Project Trade

## Introduction

### Project Name: Trade

#### Objective of the Crypto Trading Bot
The Trade project aims to develop a sophisticated crypto trading bot capable of making automated buying and selling decisions based on a detailed analysis of recent market data. Through leveraging state-of-art machine learning algorithms and real-time data acquisition, this bot seeks to optimize trading strategies to achieve potentially higher returns.

#### Presentation Structure
In this README document, we will walk you through the different components of the project, elaborating on the data analysis process, data acquisition methods, model creation, decision-making criteria, and risk estimation procedures we used to build this advanced trading bot.

## Data Analysis

### Data Analysis Explanation
Our data analysis phase involved scrutinizing historical cryptocurrency market data to identify key variables and trends that influence price movements. This involved a comprehensive statistical analysis to extract meaningful information that could guide the bot's trading decisions.

### List of Utilizable Information
- Price trends (Historical and recent)
- Volume changes
- Market sentiments
- Moving Averages
- Technical Indicators (RSI, MACD)

### Note on Missing Data
Some potential data could not be acquired or were unavailable during the initial stages of analysis. We mitigated this by supplementing with additional data sources to create a rich dataset for model training.

## Additional Data Acquisition

### API Usage for Extra Data
To enhance our data pool, we employed APIs that provide real-time market data, including live price feeds, trading volumes, and other relevant market indicators. 

### Justification for the Selected API
The chosen API was selected due to its reliability, extensive data offerings, and low latency, ensuring our bot receives the most accurate and timely data for making informed trading decisions.

## Model Creation

### Prediction Model Description
We utilized a two-pronged approach in creating the prediction model; incorporating both Gradient Boosting through XGBoost and LSTM neural networks. This dual-model approach allows the bot to learn complex patterns and relationships within the data.

#### Utilization of Recent Data to Avoid Overfitting
In order to prevent overfitting, we prioritized the incorporation of more recent data into our training dataset. This strategy ensures that our model is tuned to recent market dynamics, enhancing its predictive accuracy.

## Implementation of Dropout Layers

### Definition of Dropout Layers
Dropout layers are a technique used during the training phase to prevent overfitting. They work by randomly setting a fraction of the input units to 0 at each update during training, which helps prevent overfitting.

### Role in Preventing Overfitting
Dropout layers play a significant role in preventing overfitting by promoting a more generalized model that performs better on unseen data.

### Highlight of Performance Improvement
The implementation of dropout layers substantially improved our model's performance, particularly in minimizing the errors in predictions and enhancing the overall reliability of the bot.

## Decision Making

### Decision Making Method Description
The bot makes trading decisions based on a set of predefined criteria that are formulated based on price variation predictions. It carefully evaluates potential trades and executes them when the set criteria are met.

#### Criteria Based on Price Variation Predictions
Trading decisions are anchored on predicted price variations, with a fixed threshold of 2% variation to trigger a buy or sell decision.

## Risk Estimation

### Risk Estimation Method
The Monte Carlo method with dropout is utilized to estimate potential risk associated with each trading decision. It helps in understanding the possible outcomes and uncertainties in predictions.

#### Statistics Used for Risk Evaluation
We use several statistics, including mean, standard deviation, variance, and potential worst loss, to evaluate the risk associated with each prediction.

## Risk Evaluation

### Risk Scale Explanation
The risk is evaluated on a scale of 1 to 5, with each level representing an increased level of risk based on the calculated statistics.

#### Description of Different Risk Levels
- **1**: Low Risk
- **2**: Moderate Risk
- **3**: Medium-High Risk
- **4**: High Risk
- **5**: Very High Risk

#### Capital Allocation Based on Associated Risk
Capital is allocated based on the risk level associated with each prediction, with lower risk predictions receiving higher capital allocation and vice versa.

## Project Grade
**Grade**: A
