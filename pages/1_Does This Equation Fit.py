import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

st.title("Evaluating How Well Goals and Wins are Connected")

st.markdown("The first thing we want to check is if using 2 as the exponent is a good fit for our data. For each season that has been played since 1917 we calcuate each team's points percentage. Then we plug 2 in for gamma in our pythagorean equation to calculate an 'Expected Pts Percentage' for each team. Doing some simple linear regression will allow us to evaluate how well this fits.")
# Load data
nhl_data = pd.read_csv('https://github.com/JLarabee32/CMSE830/raw/refs/heads/main/NHLResults.csv', encoding='iso-8859-1')
cup = pd.read_csv('https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Champs.csv')
nhl_data['Season'] = nhl_data['Season'] // 10000
# Calculate Win Percentage and Y
nhl_data['Win_Pct_real'] = (nhl_data['P'] / nhl_data['GP']) / 2
nhl_data['Y'] = nhl_data['GF'] ** 2 / (nhl_data['GF'] ** 2 + nhl_data['GA'] ** 2)

# Linear regression plot
st.subheader("Linear Regression: Win_Pct vs Y")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Y', y='Win_Pct_real', data=nhl_data, ax=ax)
sns.regplot(x='Y', y='Win_Pct_real', data=nhl_data, scatter=False, color='red', ax=ax)
ax.set_title("Pythagorean Linear Regression (1917-2024 NHL seasons): Exponent = 2")
ax.set_xlabel("Expected Pts Pct")
ax.set_ylabel("Actual Pts Pct")

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("From the visualization alone we can see this model is a relatively good fit for the data (regression analysis can be found on a later page), but we can do better. For that we must find the actual observed exponent from the dataset")

# Replace invalid or missing data before calculations
nhl_data = nhl_data.replace([np.inf, -np.inf], np.nan)
nhl_data = nhl_data.dropna(subset=['Win_Pct_real', 'GF', 'GA'])

# Ensure valid values for calculations
nhl_data = nhl_data[(nhl_data['Win_Pct_real'] > 0) & (nhl_data['Win_Pct_real'] < 1)]

# Log-likelihood and implied exponent calculations
nhl_data['log_likelihood_real'] = np.log(nhl_data['Win_Pct_real'] / (1 - nhl_data['Win_Pct_real']))
nhl_data['log_goals_real'] = np.log(nhl_data['GF'] / nhl_data['GA'])
nhl_data['implied_exponent'] = nhl_data['log_likelihood_real'] / nhl_data['log_goals_real']
nhl_data["implied_exponent"] = nhl_data["implied_exponent"].replace([np.inf, -np.inf], np.nan).dropna()
nhl_data = nhl_data.dropna(subset=["implied_exponent"])

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(nhl_data['implied_exponent'], bins=np.arange(-10, 10, 0.2), kde=True, color='black', fill=True, kde_kws={"bw_adjust": 0.3}, ax=ax)
ax.set_xlim(-10, 10)
ax.set_title("Pythagorean Linear Regression (1917-2024): Implied Exponents")
ax.set_xlabel("Implied Exponent")
ax.set_ylabel("Frequency")

# Display the histogram
st.pyplot(fig)

implied_exponent = nhl_data['implied_exponent']
st.write(f"**Median:** {np.median(implied_exponent):.4f}")
st.write(f"**Mean:** {np.mean(implied_exponent):.4f}")

nhl_data['Y_mean'] = nhl_data['GF'] ** np.mean(implied_exponent) / (nhl_data['GF'] ** np.mean(implied_exponent) + nhl_data['GA'] ** np.mean(implied_exponent))

st.markdown("The mean and median end up on either side of two so it's likely two is not a bad guess, but let's try our regression again with the mean.")
# Linear regression plot
st.subheader("Linear Regression: Win_Pct vs Y")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Y_mean', y='Win_Pct_real', data=nhl_data, ax=ax)
sns.regplot(x='Y_mean', y='Win_Pct_real', data=nhl_data, scatter=False, color='red', ax=ax)
ax.set_title("Pythagorean Linear Regression (1917-2024 NHL seasons): Exponent = Mean")
ax.set_xlabel("Expected Pts Pct")
ax.set_ylabel("Actual Pts Pct")
st.pyplot(fig)

st.markdown("Not much improvement can be made on the original model, but it certainly would be preferrable to use observed data, so we will move forward utilizing the implied gamma calculated from the data.")

st.subheader("Stanley Cup Champions")
st.markdown("It would also be important to check with the observed implied gammas of each season's eventual champion to see if this equation has any bearing on what NHL franchise cares about the most: winning the Stanley Cup.")

# Process Cup data
cup['Win_Pct_cup'] = (cup['PTS'] / cup['GP']) / 2
cup['log_likelihood_cup'] = np.log(cup['Win_Pct_cup'] / (1 - cup['Win_Pct_cup']))
cup['log_goals_cup'] = np.log(cup['GF'] / cup['GA'])
cup['implied_exponent_cup'] = cup['log_likelihood_cup'] / cup['log_goals_cup']

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(
    cup['implied_exponent_cup'], 
    bins=np.arange(-10, 10, 0.05), 
    kde=True, 
    color='blue', 
    fill=True,
    kde_kws={"bw_adjust": 0.3},
    ax=ax
)
ax.axvline(x=2.333209, color='red', linestyle='dashed', linewidth=1)
ax.set_xlim(-10, 10)
ax.set_title("(1917-2024) Implied Exponents of Cup Champions")
ax.set_xlabel("Implied Exponent")
ax.set_ylabel("Frequency")

# Display the histogram in Streamlit
st.pyplot(fig)

st.markdown("Based on the cup champions also converging around a similar mean as the full dataset we can infer that it is important for NHL teams to be doing this level of analysis for their own team as it will help them understand and predict the quality of their team as it pertains to the most important trophy in the game. It is also worth noting that the luckiest Cup champion (the spike near the -4 implied exponent) is the last time the Toronto Maple Leafs won the Stanley Cup which is all the more fitting for the beleagured franchise.")
