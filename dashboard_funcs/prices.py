"""
НЕ ЗАКОНЧЕНО
"""

import plotly.express as px
import streamlit as st
import pandas as pd


def prices_creation(df):

    st.header('Гистограмма распределения цен')

    st.dataframe(df)

    # df = df.value_counts()
    #
    # df = pd.concat([df], axis=1)
    #
    # df = df.reset_index(drop=False)

    fig = px.histogram(df, nbins=5)
    fig.update_layout(bargap=0.2)

    st.plotly_chart(fig)