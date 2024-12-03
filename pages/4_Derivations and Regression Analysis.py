import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

st.title("Deriving the Implied Exponent for Each Season")
st.markdown("To derive the implied exponent from our dataset utilizing our pythagorean wins equation we first take the natural logarithm of a team's odds ratio:")
st.latex(r"""
\ln\left(\frac{\text{Win\%}}{1 - \text{Win\%}}\right)
""")
st.markdown("Then the same to our goal ratio")
st.latex(r"""
\ln\left(\frac{\text{Goals For}}{\text{Goals Against}}\right)
""")
st.markdown("And finally the ratio of these two logarithmic functions is our implied exponent equation:")
st.latex(r"""
{\gamma }_{\text{implied}} := \frac{\ln\left(\frac{\text{Win\%}}{1 - \text{Win\%}}\right)}{\ln\left(\frac{\text{Goals For}}{\text{Goals Against}}\right)}
""")

st.title("Regression Analysis")

nhl_data = pd.read_csv('https://github.com/JLarabee32/CMSE830/raw/refs/heads/main/NHLResults.csv', encoding='iso-8859-1')
cup = pd.read_csv('https://raw.githubusercontent.com/JLarabee32/CMSE830/refs/heads/main/Champs.csv')
nhl_data['Season'] = nhl_data['Season'] // 10000
nhl_data['Win_Pct_real'] = (nhl_data['P'] / nhl_data['GP']) / 2
nhl_data['Y_mean'] = nhl_data['GF'] ** 2.2787 / (nhl_data['GF'] ** 2.2787 + nhl_data['GA'] ** 2.2787)
correlation = nhl_data['Win_Pct_real'].corr(nhl_data['Y_mean'])
X = nhl_data[['Y_mean']]
y = nhl_data['Win_Pct_real']
model = sm.OLS(y, X).fit()
summary = model.summary().as_text()

st.markdown("The following are the regression results from the pythagorean model utilizing the mean implied gamma from the observed data")
st.code(summary, language='text')
st.markdown("The most compelling piece of evidence here that our pythagorean model is a significant predictor of team performance is our R-Squared value. 0.99 is an impeccable correlation and a very strong indicator we are on to something here")

