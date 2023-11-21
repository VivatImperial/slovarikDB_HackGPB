import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Прогноз по стоимости недвижимости в городе Санкт-Петербург на 2023 год",
    page_icon="👋",
)

st.write('# Обзор объявлений на рынке недвижимости города Санкт-Петербург')

for name in 'студий', '1', '2', '3', '4 и более':
    data = pd.read_csv(f'time_series_data/spb/spb_prepared_live_ap_{name}.csv')

    fig = px.line(data, x="date", y="price", title=f'Стоимость {name}' + '-комнатных квартир' * (name != 'студий'))

    st.write(f'предсказание средней стоимости {name}' + '-комнатных квартир' * (name != 'студий'))
    st.plotly_chart(fig)
