import streamlit as st
import pandas as pd

st.write("Hello World")

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
