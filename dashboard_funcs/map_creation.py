import streamlit as st


def map_creation(map_df, city):

    if city == 'spb':
        output = 'СПБ'
    else:
        output = 'МСК'

    with st.container():
        st.header(f'Карта расположения квартир в {output}')
        st.map(map_df)
