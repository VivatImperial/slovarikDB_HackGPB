import streamlit as st

from PostgreS.connection import load_data

from dashboard_funcs.map_creation import map_creation
from dashboard_funcs.rooms_pie import rooms_pie_creation
from dashboard_funcs.prices import prices_creation
from dashboard_funcs.floors_num import floors_num_creation
from dashboard_funcs.rooms_hist import rooms_hist_creation

st.set_page_config(
    page_title="DB_MSC",
    page_icon="DB",
)

st.header('Дэшборд')
st.write('Тут будет представлена основная статистика по МСК')
st.write('Загрузка данных может занять некоторое время')

search_city = 'moscow'

map_df, pie_df, floors_df, prices_df = load_data(city=search_city)

map_creation(map_df, search_city)
rooms_pie_creation(pie_df)
rooms_hist_creation(pie_df)
floors_num_creation(floors_df)

