import plotly.express as px
import streamlit as st
import pandas as pd


def floors_num_creation(df):
    st.header('Гистограмма распределения этажности зданий в объявлениях')

    df = df.value_counts()

    df = pd.concat([df], axis=1)

    df = df.reset_index(drop=False)

    df = df.loc[df['floors'] < 100]

    fig = px.histogram(df, x='floors', y='count', nbins=100, labels=dict(
        floors='Число этажей в доме',
        count=' flats'
    ))
    fig.update_layout(bargap=0.2)

    st.plotly_chart(fig)
