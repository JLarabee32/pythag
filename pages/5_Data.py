import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Load data
nhl_data = pd.read_csv('https://github.com/JLarabee32/CMSE830/raw/refs/heads/main/NHLResults.csv', encoding='iso-8859-1')
cup = pd.read_csv('https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Champs.csv')
nhl_data['Season'] = nhl_data['Season'] // 10000
# Calculate Win Percentage and Y
nhl_data['Win_Pct_real'] = (nhl_data['P'] / nhl_data['GP']) / 2

# Log-likelihood and implied exponent calculations
nhl_data['log_likelihood_real'] = np.log(nhl_data['Win_Pct_real'] / (1 - nhl_data['Win_Pct_real']))
nhl_data['log_goals_real'] = np.log(nhl_data['GF'] / nhl_data['GA'])
nhl_data['implied_exponent'] = nhl_data['log_likelihood_real'] / nhl_data['log_goals_real']
nhl_data['Y_mean'] = nhl_data['GF'] ** np.mean(implied_exponent) / (nhl_data['GF'] ** np.mean(implied_exponent) + nhl_data['GA'] ** np.mean(implied_exponent))
# Process Cup data
cup['Win_Pct_cup'] = (cup['PTS'] / cup['GP']) / 2
cup['log_likelihood_cup'] = np.log(cup['Win_Pct_cup'] / (1 - cup['Win_Pct_cup']))
cup['log_goals_cup'] = np.log(cup['GF'] / cup['GA'])
cup['implied_exponent_cup'] = cup['log_likelihood_cup'] / cup['log_goals_cup']

st.title("Data Exploration")

st.markdown("The following are the two datasets used for this research. The first, labeled NHL Results, is downloaded from the NHL's website and located in the github repo for this app. It is a season by season account of all the results in NHL history and also includes a few of the necessary calculations from the rest of the project. These include win percentage, or the percentage of possible points that each team won, the two logarithmic values used in the implied gamma equation, and the implied gamma. The second dataset, labeled Cup Results, is the results of every Stanley Cup champion's regular season results from each season. It is pulled from Wikipedia and stored in the github repo for this app. It also includes the same calculations from the first dataset.")
st.subheader("NHL Results")
st.write(nhl_data)

st.subheader("Cup Results")
st.write(cup)
