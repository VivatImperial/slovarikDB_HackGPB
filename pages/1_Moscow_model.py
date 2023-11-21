from pickle import load
import streamlit as st
import time

import xgboost as xgb

from backend.preprocessing import *

encoder = load(open('backend/moscow_models/encoder_cb.pkl', 'rb'))

model = xgb.Booster()
model.load_model("backend/moscow_models/modelxg.pkl")git pull origin master

station_computer = StationComputer('stations/moscow_stations.csv')
address_translator = AddressTranslator(['ул.', 'пер.', 'просп.', 'поселение', 'жк', 'проезд', 'ш.', 'наб.',
                                        'мкр', 'другое', 'пос.', 'кв-л', 'парк'])

st.set_page_config(page_title="Prediction", page_icon="👋")
st.write('# Оценка залоговой стоимости квартиры в городе Москва')
st.write('## Параметры квартиры для оценки:')
st.sidebar.header('Введите параметры оцениваемой квартиры:')

uploaded_file = st.sidebar.file_uploader('Вставьте свой CSV файл', type='csv')

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    area = st.sidebar.slider('**Площадь жилья** в метрах квадратных', 10, 250, 10)
    area_live = st.sidebar.slider('**Площадь жилого помещения** в метрах квадратных', 2, area, 2)
    number_of_rooms = st.sidebar.slider('**Количество комнат**', 1, 10, 1, 1)

    number_of_floors = st.sidebar.slider('**Количество этажей**', 1, 200, 1, 1)

    if number_of_floors == 1:
        floor = 1
    else:
        floor = st.sidebar.slider('**Номер этажа**', 1, number_of_floors, 1, 1)

    kitchen_area = st.sidebar.slider('**Площадь кухни** в метрах квадратных', 2, 100, 2)
    address = st.sidebar.text_input('**Адрес жилья**', value='Улица Пушкина, дом 2')

    st.sidebar.write('## **Координаты следует вводить как число с плавающей точкой**')

    try:
        latitude = Degrees(st.sidebar.text_input('**Введите широту**', value='55.752'))
    except ValueError:
        st.sidebar.write('Неправильный формат: вводите широту как десятичную дробь (55.752 для широты Москвы)')
        latitude = Degrees('55.752')
        st.write('Широта не введена')
    try:
        longitude = Degrees(st.sidebar.text_input('**Введите долготу**', value='37.615'))
    except ValueError:
        st.sidebar.write('Неправильный формат: вводите долготу как десятичную дробь (37.615 для долготы Москвы)')
        longitude = Degrees('37.615')
        st.write('Долгота не введена')

    is_new = st.sidebar.radio('Является ли дом новостроем?', ['Да', 'Нет'])

    closest_station, station_distance = station_computer.compute_closest(latitude, longitude)

    input_df = pd.DataFrame(data={'is_new': [is_new == 'Да'],
                                  'rooms': [number_of_rooms],
                                  'area': [area],
                                  'area_live': [area_live],
                                  'kitchen_area': [kitchen_area],
                                  'floor_': [floor],
                                  'floors': [number_of_floors],
                                  'closest_station': [closest_station],
                                  'dist_to_station': [station_distance],
                                  'time': [int(time.time())],
                                  'address_type': [address_translator.give_address_type(address)]})

    st.write(input_df)

pred = model.predict(xgb.DMatrix(encoder.transform(input_df)))

if len(pred) == 1:
    st.write(f'### Прогнозируемая стоимость квартиры находится в диапазоне между {int(pred[0]) *0.92:.0f} и {int(pred[0]) * 1.02:.0f} рублей')
else:
    st.write('Предсказания:')
    st.write(pd.DataFrame(pred))


    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(pd.DataFrame(pred))

    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )
