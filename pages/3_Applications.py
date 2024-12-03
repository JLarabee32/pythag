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
nhl_data['Y'] = nhl_data['GF'] ** 2 / (nhl_data['GF'] ** 2 + nhl_data['GA'] ** 2)

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

implied_exponent = nhl_data['implied_exponent']

st.title("Applications for Pythagorean Wins")

st.subheader("Input a Goals For and Goals Against value in the boxes below and this app will calculate an expected points for you")

Goals_for = st.number_input(label="Goals For", min_value=0, step=1, format="%d")
Goals_against = st.number_input(label="Goals Against", min_value=0, step=1, format="%d")

def pythag_wins(gf, ga):
    gamma = np.mean(implied_exponent)
    Y = (gf**gamma) / (gf**gamma + ga**gamma)
    Points = round(Y * 164)
    return int(Points)

if Goals_for > 0 and Goals_against > 0:
    st.write(f"**Expected Points:** {pythag_wins(Goals_for, Goals_against)}")
else:
    st.write("Please input a value for Goals For and Goals Against")


st.subheader("Marginal Revenue and Player Value")

st.write("Our value for pythagorean wins can also be used to calculate a player's value to their team to assist with contract valuations. Input a marginal revenue value for each extra team win, how many points the team got last season, and a player's value for how many goals for and against per game they contribute to and this app will calculate their value to the team in dollars.")

def MRP(mr, gf, ga, pts):
    pct = pts/164
    gamma = np.mean(implied_exponent)
    mrp = mr*pct*(1-pct)*(gf-ga)*82
    return round(mrp, 2)

GF = st.number_input(label="Goals For per Game")
GA = st.number_input(label="Goals Against per Game")
MR = st.number_input(label="Marginal Revenue for Each Win", min_value=0, step=1, format="%d")
PTS = st.number_input(label="Standings Points", min_value=0, step=1, format="%d")

if GF != 0 and GA != 0 and MR != 0 and PTS != 0:
    st.write(f"**Player's Marginal Value: $** {MRP(MR, GF, GA, PTS):,.2f}")
else:
    st.write("Please input a value for all inputs")

