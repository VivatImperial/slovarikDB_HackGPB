import re

import numpy as np
import pandas as pd


class Degrees:

    def __init__(self, string):
        if re.match(r'[-0-9]+[/.,][-0-9]+$', string):
            string.replace(',', '.')
            self.value = float(string)
        else:
            raise ValueError('not in degrees format (angle as a float)')


class StationComputer:

    def __init__(self, metro_stations_link):
        self.stations = pd.read_csv(metro_stations_link)
        self.coefficient = 40000 / 360

    def compute_closest(self, lat: Degrees, lng: Degrees):
        lat = lat.value
        lng = lng.value

        lat_array = np.array(self.stations['lat'])
        lon_array = np.array(self.stations['lng'])
        station_dct = {index: station for index, station in enumerate(self.stations['station'])}

        distances = (lat_array - lat) ** 2 + (lon_array - lng) ** 2
        index = np.argmin(distances)
        return station_dct[index], np.sqrt(distances[index] * self.coefficient)


class AddressTranslator:

    def __init__(self, translator):
        self.possible_types = translator

    def give_address_type(self, address_):

        address_ = address_.lower().replace('улица', 'ул.').replace('проспект', 'просп.').replace('шоссе',
                                                                                                  'ш.').replace(
            'посёлок', 'пос.').replace(
            'пр-кт', 'просп.').replace('пр.', 'просп.').replace('пр-т', 'просп.').replace('переулок', 'пер.').replace(
            'бульвар', 'бул.').replace('наб.', 'набережная').replace('проспект ', 'просп. ')

        for word in address_.split():
            if word in self.possible_types:
                return word
        return 'другое'
