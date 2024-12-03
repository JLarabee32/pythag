import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

st.title("Has This Connection Changed With Time?")

st.markdown("Hockey has changed quite a lot since the first NHL game was played, it wouldn't be surprising to learn that the connection between goal scoring and winning has also changed.")

# Load data
nhl_data = pd.read_csv('https://github.com/JLarabee32/CMSE830/raw/refs/heads/main/NHLResults.csv', encoding='iso-8859-1')
cup = pd.read_csv('https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Champs.csv')
nhl_data['Season'] = nhl_data['Season'] // 10000
# Calculate Win Percentage and Y
nhl_data['Win_Pct_real'] = (nhl_data['P'] / nhl_data['GP']) / 2
nhl_data['Y'] = nhl_data['GF'] ** 2 / (nhl_data['GF'] ** 2 + nhl_data['GA'] ** 2)

# Replace invalid or missing data before calculations
nhl_data = nhl_data.replace([np.inf, -np.inf], np.nan)  # Replace infinities with NaN
nhl_data = nhl_data.dropna(subset=['Win_Pct_real', 'GF', 'GA'])  # Drop rows with missing data

# Ensure valid values for calculations
nhl_data = nhl_data[(nhl_data['Win_Pct_real'] > 0) & (nhl_data['Win_Pct_real'] < 1)]  # Remove invalid percentages

# Log-likelihood and implied exponent calculations
nhl_data['log_likelihood_real'] = np.log(nhl_data['Win_Pct_real'] / (1 - nhl_data['Win_Pct_real']))
nhl_data['log_goals_real'] = np.log(nhl_data['GF'] / nhl_data['GA'])
nhl_data['implied_exponent'] = nhl_data['log_likelihood_real'] / nhl_data['log_goals_real']
nhl_data["implied_exponent"] = nhl_data["implied_exponent"].replace([np.inf, -np.inf], np.nan).dropna()
nhl_data = nhl_data.dropna(subset=["implied_exponent"])

# Calculate exp.mean and cumulative.mean
exp_mean = (
    nhl_data.groupby('Season')['implied_exponent']
    .mean()
    .reset_index(name='exp.mean')
)
exp_mean['cumulative.mean'] = exp_mean['exp.mean'].cumsum() / np.arange(1, len(exp_mean) + 1)

# Calculate exp.medians and cumulative.median
exp_medians = (
    nhl_data.groupby('Season')['implied_exponent']
    .median()
    .reset_index(name='exp.medians')
)
exp_medians['cumulative.median'] = exp_medians['exp.medians'].cumsum() / np.arange(1, len(exp_medians) + 1)

reg = LinearRegression()
X = exp_medians[['Season']]
y = exp_medians['exp.medians']
reg.fit(X, y)
predicted = reg.predict(X)

# Plot time series median
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(exp_medians['Season'], exp_medians['exp.medians'], label='Median Implied Exponent')
ax.plot(exp_medians['Season'], predicted, color='blue', label='Regression')
ax.axhline(y=nhl_data['implied_exponent'].median(), color='red', linestyle='--', label='Overall Median')
ax.set_xlabel("Season")
ax.set_ylabel("Median Implied Exponent")
ax.set_title("Yearly Median Implied Exponent, NHL 1917-2024")
ax.set_ylim(0.5, 4)
ax.legend()

st.pyplot(fig)
st.write(f"**Slope of the regression line:** {reg.coef_[0]:.4f}")
st.markdown(
    f"Running some simple time series analysis on each season's median implied exponent shows that there is plenty of noise in the dataset. However, a simple regression over that seems to imply that the observed implied exponent is increasing year over year by **{reg.coef_[0]:.4f}**."
)

fig, ax = plt.subplots(figsize=(10, 5))

# Plot cumulative median
ax.plot(exp_medians['Season'], exp_medians['cumulative.median'], label='Cumulative Median')

# Add horizontal and vertical lines
ax.axhline(y=nhl_data['implied_exponent'].median(), color='red', linestyle='--', label='Overall Median')
ax.axvline(x=1994, color='orange', linestyle='--')
ax.axvline(x=2004, color='orange', linestyle='--', label='Dead Puck Era')
ax.set_xlabel("Season")
ax.set_ylabel("Cumulative Median Implied Exponent")
ax.set_title("Cumulative Median Implied Exponent, NHL 1917-2024")
ax.set_ylim(1.5, 2.5)
ax.legend()
st.pyplot(fig)

st.markdown("When plotting the cumulative median of all seasons combined some interesting trends start to emerge. First is that the growth in implied exponent from the previous regression line still emerges, starting at the minimum point in the 1940 season and growing steadily since. The second is that the so-called 'Dead Puck Era' emerges rather strongly as the yearly implied exponent stagnated in the era defined by the Neutral Zone Trap and the overperformance of less talented teams. But if the years were defense reigned supreme cause this growth to plateu, is it possible that offense is the reason for the growth?")

# Goals per game
nhl_data['G_per_game'] = nhl_data['GF'] / nhl_data['GP']

fig, ax = plt.subplots(figsize=(10, 6))

pre_1940 = nhl_data[nhl_data['Season'] < 1940]
post_1940 = nhl_data[nhl_data['Season'] >= 1940]
# Plot for post-1940
ax.scatter(
    post_1940['implied_exponent'], 
    post_1940['G_per_game'], 
    facecolors='none',
    edgecolors='blue',
    label='1940 and later'
)

# Plot for pre-1940
ax.scatter(
    pre_1940['implied_exponent'], 
    pre_1940['G_per_game'], 
    color='red', 
    label='Pre-1940'
)

# Add labels, legend, and limits
ax.set_xlabel('Implied Exponent')
ax.set_ylabel('Goals For Per Game')
ax.set_xlim(-10, 10)
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("Examining each team's implied exponent compared to their goals scored per game would suggest that offense is definitely connected to the increase in implied exponent as the seasons below the minimum implied exponent all cluster near the bottom, while the seasons after 1940 cluster up and to the right.")