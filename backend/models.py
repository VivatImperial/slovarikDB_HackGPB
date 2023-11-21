import numpy as np
import pandas as pd


class Model:

    def __init__(self, encoder, model_):
        self.columns = None
        self.encoder = encoder
        self.model = model_

    def create_columns(self, data):
        if self.columns:
            return

        res = []
        for column in data.columns:
            if type(column) == int:
                res.append(str(column))
            else:
                res.append(column)

        self.columns = res

    def __call__(self, data):
        encoded = pd.DataFrame(self.encoder.transform(data[['closest_station', 'address_type']]))
        encoded = pd.concat([data.drop(columns=['closest_station', 'address_type']), pd.DataFrame(encoded)], axis=1)

        self.create_columns(encoded)

        encoded.columns = self.columns
        result = self.model.predict(encoded)

        return pd.DataFrame(data={'predictions': np.exp(result)})
