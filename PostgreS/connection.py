import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd
import plotly.express as px



def hist_creation(df):

    fig = px.histogram(df)
    st.plotly_chart(fig)


@st.cache_data
def load_data(city):

    try:
        connection = psycopg2.connect(user="postgres",
                                          password="3p5t5X10BL4QpH7vPHZS",
                                          host="containers-us-west-188.railway.app",
                                          port="7857",
                                          database="railway"
                                      )


        with connection.cursor() as cursor:

            col1, col2 = st.columns(2)

            stmt_base_info_1 = sql.SQL('SELECT COUNT(*) FROM {}').format(
                sql.Identifier(city)
            )

            if city == 'spb':
                stmt_base_info_2 = sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'spb';")
                columns = [
                    'time', 'address', 'floor_', 'floors',
                    'area', 'price', 'lat', 'lng', 'material',
                    'is_new', 'closest_station', 'dist_to_station',
                    'rooms', 'updated', 'address_type'
                ]

            else:
                stmt_base_info_2 = sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'moscow';")

                columns = [
                   'updated', 'price', 'is_new', 'rooms',
                   'area', 'area_live', 'area_kitchen', 'floor_',
                   'floors', 'lat', 'lng', 'address', 'city',
                   'closest_station', 'dist_to_station', 'idk'
                ]


            stmt_DF_info_1 = sql.SQL('SELECT * FROM {}').format(
                sql.Identifier(city)
            )


            with col1:

                cursor.execute(stmt_base_info_1)

                st.header('Записи')

                for row in cursor:
                    st.write(f'Количество записей: {row[0]}')

                cursor.execute(stmt_base_info_2)

                df = pd.DataFrame(
                    cursor,
                    columns=('Название столбца', 'Тип')
                )

                st.write('Стобцы и типы данных:')
                st.dataframe(df)


            with col2:



                cursor.execute(stmt_DF_info_1)

                current_df = pd.DataFrame(
                    cursor,
                    columns=columns
                )

                st.header('Общая информация о квартирах из DF')

                avg_price = int(current_df['price'].mean())
                avg_area = round(current_df['area'].mean(), 2)

                st.write(f' Средняя цена квартир: {avg_price}')
                st.write(f' Средний размер квартир: {avg_area}')

            st.header('Средние параметры квартир, отличных по кол-ву комнат')
            with st.container():

                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                col5, col6 = st.columns(2)
                col7, col8 = st.columns(2)
                col9, col10 = st.columns(2)
                col11, col12 = st.columns(2)

                studio_price = int(current_df.loc[current_df['rooms'] == 0]['price'].mean())
                one_room_price = int(current_df.loc[current_df['rooms'] == 1]['price'].mean())
                two_rooms_price = int(current_df.loc[current_df['rooms'] == 2]['price'].mean())
                three_rooms_price = int(current_df.loc[current_df['rooms'] == 3]['price'].mean())
                four_rooms_price = int(current_df.loc[current_df['rooms'] == 4]['price'].mean())
                five_rooms_price = current_df.loc[current_df['rooms'] == 5]['price'].mean()

                studio_square = int(current_df.loc[current_df['rooms'] == 0]['area'].mean())
                one_room_square = int(current_df.loc[current_df['rooms'] == 1]['area'].mean())
                two_rooms_square = int(current_df.loc[current_df['rooms'] == 2]['area'].mean())
                three_rooms_square = int(current_df.loc[current_df['rooms'] == 3]['area'].mean())
                four_rooms_square = int(current_df.loc[current_df['rooms'] == 4]['area'].mean())
                five_rooms_square = current_df.loc[current_df['rooms'] == 5]['area'].mean()

                studio_prices_for_hist = current_df.loc[current_df['rooms'] == 0]['price']
                one_room_prices_for_hist = current_df.loc[current_df['rooms'] == 1]['price']
                two_rooms_prices_for_hist = current_df.loc[current_df['rooms'] == 2]['price']
                three_rooms_prices_for_hist = current_df.loc[current_df['rooms'] == 3]['price']
                four_rooms_prices_for_hist = current_df.loc[current_df['rooms'] == 4]['price']
                five_rooms_prices_for_hist = current_df.loc[current_df['rooms'] == 5]['price']



                with col1:
                    st.subheader('Информация о студиях')
                    st.write(f'Средняя цена: {studio_price}')
                    st.write(f'Средняя площадь: {studio_square}')

                with col2:
                    st.subheader('Гистограмма распределения цен')
                    df = studio_prices_for_hist.loc[studio_prices_for_hist < 25_000_000]
                    hist_creation(df)


                with col3:
                    st.subheader('Информация об однокомнатных квартирах')
                    st.write(f'Средняя цена: {one_room_price}')
                    st.write(f'Средняя площадь: {one_room_square}')

                with col4:
                    st.subheader('Гистограмма распределения цен')
                    df = one_room_prices_for_hist.loc[one_room_prices_for_hist < 30_000_000]
                    hist_creation(df)


                with col5:
                    st.subheader('Информация о двухкомнатных квартирах')
                    st.write(f'Средняя цена: {two_rooms_price}')
                    st.write(f'Средняя площадь: {two_rooms_square}')

                with col6:
                    st.subheader('Гистограмма распределения цен')
                    df = two_rooms_prices_for_hist.loc[two_rooms_prices_for_hist < 50_000_000]
                    hist_creation(df)


                with col7:
                    st.subheader('Информация о трехкомнатных квартирах')
                    st.write(f'Средняя цена: {three_rooms_price}')
                    st.write(f'Средняя площадь: {three_rooms_square}')

                with col8:
                    st.subheader('Гистограмма распределения цен')
                    df = three_rooms_prices_for_hist.loc[three_rooms_prices_for_hist < 100_000_000]
                    hist_creation(df)

                with col9:
                    st.subheader('Информация о четырехкомнатных квартирах')
                    st.write(f'Средняя цена: {four_rooms_price}')
                    st.write(f'Средняя площадь: {four_rooms_square}')

                with col10:
                    st.subheader('Гистограмма распределения цен')
                    df = four_rooms_prices_for_hist.loc[four_rooms_prices_for_hist < 200_000_000]
                    hist_creation(df)

                with col11:
                    st.subheader('Информация о пятикомнатных квартирах')
                    if city != 'spb':
                        st.write(f'Средняя цена: {int(five_rooms_price)}')
                        st.write(f'Средняя цена: {int(five_rooms_square)}')
                        with col12:
                            st.subheader('Гистограмма распределения цен')
                            df = five_rooms_prices_for_hist.loc[five_rooms_prices_for_hist < 500_000_000]
                            hist_creation(df)
                    else:
                        st.write('Пятикомнатных квартир нет среди объявлений')




            df_for_map = current_df.reindex(columns=['lat', 'lng'])

            df_for_map.columns = ['lat', 'lon']

            df_for_map['lat'] = df_for_map['lat'].astype(float)
            df_for_map['lon'] = df_for_map['lon'].astype(float)


            df_for_rooms_pie = current_df['rooms']

            df_for_floors_num = current_df['floors']

            df_for_prices = current_df['price']


        return df_for_map, df_for_rooms_pie, df_for_floors_num, df_for_prices


    except Exception as e:
        st.error('ОЙ, видимо, на сервере возникла ошибка')
        st.write(e)
