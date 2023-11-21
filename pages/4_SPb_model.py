import time
from pickle import load
import streamlit as st

from backend.models import *
from backend.preprocessing import *

model = Model(load(open('backend/encoder.pickle', 'rb')), load(open('backend/model.pickle', 'rb')))
station_computer = StationComputer('stations/spb_stations.csv')
address_translator = AddressTranslator(['другое', 'просп.', 'ул.', 'ш.', 'пос.', 'район', 'жк', 'бул.',
                                        'набережная', 'парк', 'мо', 'территория'])

st.set_page_config(page_title="Prediction", page_icon="👋")
st.write('# Оценка залоговой стоимости квартиры в городе Санкт-Петербург')
st.write('## Параметры квартиры для оценки:')
st.sidebar.header('Введите параметры оцениваемой квартиры:')

uploaded_file = st.sidebar.file_uploader('Вставьте свой CSV файл', type='csv')

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    area = st.sidebar.slider('**Площадь жилья** в метрах квадратных', 10, 250, 10)
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
        latitude = Degrees(st.sidebar.text_input('**Введите широту**', value='59.938'))
    except ValueError:
        st.sidebar.write('Неправильный формат: вводите широту как float (59.938 для широты Санкт-Петербурга)')
        latitude = Degrees('59.938')
        st.write('Широта не введена')
    try:
        longitude = Degrees(st.sidebar.text_input('**Введите долготу**', value='30.314'))
    except ValueError:
        st.sidebar.write('Неправильный формат: вводите долготу как float (30.314 для долготы Санкт-Петербурга)')
        longitude = Degrees('30.314')
        st.write('Долгота не введена')

    is_new = st.sidebar.radio('Является ли дом новым?', ['Да', 'Нет'])

    closest_station, station_distance = station_computer.compute_closest(latitude, longitude)

    input_df = pd.DataFrame(data={'floor_': [floor],
                                  'floors': [number_of_floors],
                                  'area': [area],
                                  'lat': [latitude.value],
                                  'lng': [longitude.value],
                                  'is_new': [is_new == 'Да'],
                                  'closest_station': [closest_station],
                                  'dist_to_station': [station_distance],
                                  'rooms': [number_of_rooms],
                                  'updated': [int(time.time())],
                                  'address_type': [address_translator.give_address_type(address)]})

st.write(input_df)

pred = model(input_df)

if len(pred) == 1:
    st.write(f'###  Прогнозируемая стоимость квартиры находится в диапазоне между {int(pred.iloc[0, 0])*0.9:.0f} и {int(pred.iloc[0, 0])*1.05:.0f} рублей')
else:
    st.write('Предсказания:')
    st.write(pred)


    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(pred)

    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )

