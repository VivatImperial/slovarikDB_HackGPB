import plotly.express as px
import streamlit as st
import pandas as pd


def rooms_hist_creation(df):

    st.header('Гистограмма распределения количества комнат в квартирах из объявлений')

    rooms_unique = df.value_counts()

    new_df = pd.concat([rooms_unique], axis=1)

    new_df = new_df.reset_index(drop=False)

    fig = px.histogram(new_df, x='rooms', y='count', nbins=10, labels=dict(
        rooms='Число комнат',
        count=' flats'
    ))
    fig.update_layout(bargap=0.2)

    st.plotly_chart(fig)