from flask import Flask
from Arduino import Arduino
from ArduinoDAO import ArduinoDAO
import pandas as pd

app = Flask(__name__)


@app.route("/<t>/<p>/<l>")
def envio (t,p,l):
    a = "temp: "+t+"\n pres: "+p+"\n lumi: "+l
    t = float(t)
    p = int(p)
    l = int(l)

    ard= Arduino()
    ard.t = t
    ard.p = p
    ard.l = l

    df2 = pd.read_csv("Arduino.csv") #import
    
    dao = ArduinoDAO()
    dao.erros(ard)
    dao.create(ard)

    return str(a)

app.run(host="0.0.0.0", port="8000")