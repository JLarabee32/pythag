import streamlit as st
st.title("Pythagoras's Puck")
st.subheader("Applying the Pythagorean Theorem to Predict NHL Seasons")
st.markdown("By Joey Larabee")

st.image("https://i.ytimg.com/vi/YKYd2Osu0nQ/maxresdefault.jpg")

st.markdown("Bill James first introduced the world to Pythagorean Wins, the concept that taking an MLB team's runs scored squared divided by their runs surrended squared as an equation to predict their likely win percentage. He found doing this method was a better indicator of their wins for the next season than the actual wins from the current season. The Oakland A's and Michael Lewis's book Moneyball helped introduce the idea of using Pythagorean wins in terms of roster construction to predict how well your team will do based on how many runs you project to score or surrender in a given year. Through further research many have found that the theory holds up rather well, however solving for the exponent from historic seasons reveals that the real exponent is likely slightly larger than 2. But now it is time to do the same work for hockey. In this project I will search through every season of NHL hockey to see the relationship between the ratio of goals scored and given up to winning, how this relationship has evolved over time, and how this solution can be applied to every day front ofice tasks. The equation below will be the foundation of this work.")

st.latex(r"""
\text{Win\%} = \frac{\text{Goals For}^\gamma}{\text{Goals For}^\gamma + \text{Goals Against}^\gamma}
""")
