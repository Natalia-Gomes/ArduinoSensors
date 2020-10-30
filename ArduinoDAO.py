import pandas as pd
from Arduino import Arduino

class ArduinoDAO():

    def open(self):
        df = pd.read_csv("Arduino.csv")
        return df
    def save(self, df):
        df.to_csv("Arduino.csv", index=False)
    def create(self, ard):
        df = self.open()
        new_id = self.get_new_id(df)
        ard.id = new_id
        new_row = pd.DataFrame(data=[[
                                    ard.id, ard.t,ard.p,ard.l,ard.e
                                    ]],
                                    columns = df.columns)
        df = df.append(new_row)
        self.save(df)
    def get_new_id(self, df):
        if len(df)== 0:
            id = 1
        else:
            last = df.tail(1)
            id = last.id.values[0]+1
        return id

    def read(self,id):
        df = self.open()
        i = self.get_index(id, df)
        ard = Arduino()
        ard.id = id
        ard.t = df.iloc[i].t
        ard.p = df.iloc[i].p
        ard.l = df.iloc[i].l
        return ard

    def get_index(self, id, df):
        index = df.loc[df.id == id, :].index
        index = df.loc[df.id == id, :].index[0]
        return index
    def erros(self,ard):
        ard.e = "sem erros"
        if ard.t <= -55 or ard.t >= 125:  # Ds18b20 -55/125 ou -10/85ºC
            ard.e = "erro de medida"
        if ard.p != 0 and ard.p != 1:
            ard.e = "erro de medida"
        if ard.l < 1 or ard.l > 40000:  # TSL2561 1/40000lx, so funciona entre -30 e 70ºC
            ard.e = "erro de medida"

        return ard.e
