# Demand-Based Pricing Optimizer (Elasticity-Based Retail Pricing System)

## Overview

This project analyzes retail sales data to estimate price elasticity of demand and generate pricing recommendations for products. The goal is to understand how changes in price affect quantity sold, revenue, and profit, and to support data-driven pricing decisions.

The system simulates a real-world pricing analytics workflow used in retail and e-commerce environments.

---

## Problem Statement

Businesses often struggle to determine whether they should increase, decrease, or maintain product prices. This project addresses that problem by using historical sales data to measure demand sensitivity and support pricing decisions.

---

## Dataset

The dataset used is the Superstore Sales Dataset from Kaggle.

It contains information such as:

- Product names
- Sales values
- Quantity sold
- Profit
- Order dates
- Product categories

---

## Methodology

The project follows the steps below:

### 1. Data Preparation
- Loading and cleaning the dataset
- Sorting data by product and order date
- Creating derived features such as unit price and unit profit

### 2. Feature Engineering
- Unit Price = Sales / Quantity
- Unit Profit = Profit / Quantity

### 3. Elasticity Calculation
Price elasticity of demand is calculated as:

Elasticity = Percentage change in quantity / Percentage change in price

This measures how sensitive customer demand is to price changes.

### 4. Product-Level Analysis
Each product is analyzed over time to compute:
- Previous price
- Previous quantity
- Percentage changes in price, quantity, revenue, and profit
- Average price elasticity

### 5. Pricing Decision Logic
Products are classified into pricing actions:

- Increase Price
- Decrease Price
- Keep Price
- Monitor / Insufficient variation

---

## Dashboard Features

The project includes a visual analytics dashboard built using Plotly:

- KPI summary of pricing decisions
- Distribution of pricing decisions across all products
- Elasticity distribution histogram showing demand sensitivity patterns

---

## Key Insights

The analysis provides insights such as:

- Products with high price sensitivity where small price changes significantly affect demand
- Products with low sensitivity where prices can potentially be increased safely
- Products with insufficient variation where elasticity cannot be reliably measured
- Overall distribution of pricing behavior across the product portfolio

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Plotly
- OpenPyXL

---

## Limitations

- Elasticity calculations can be unstable when price changes are extremely small
- Some products have insufficient price variation, making elasticity difficult to estimate accurately
- External factors such as promotions and seasonality are not explicitly modeled

---

## Future Improvements

- Improve elasticity stability using smoothing or regularization techniques
- Add time-series forecasting for demand prediction
- Build an interactive dashboard using Streamlit or Power BI
- Integrate profit optimization for automated pricing recommendations

---

## Conclusion

This project demonstrates how pricing decisions can be supported using data analysis and elasticity modeling. It provides a structured approach to understanding demand behavior and generating actionable pricing insights.