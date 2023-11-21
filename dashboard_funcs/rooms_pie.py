import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px



def rooms_pie_creation(df):

    # df = df.replace(0, 'студия')

    st.header('Круговая диаграмма распределения количества комнат')

    rooms_unique = df.value_counts()

    new_df = pd.concat([rooms_unique], axis=1)

    new_df = new_df.reset_index(drop=False)

    new_df = new_df.replace(0, 'студия')

    # fig, ax = plt.subplots()
    #
    # ax.pie(new_df['count'], labels=new_df['rooms'], autopct='%1.2f%%')
    #
    # st.pyplot(fig)


    fig = px.pie(new_df, values=new_df['count'], names=new_df['rooms'])

    st.plotly_chart(fig)