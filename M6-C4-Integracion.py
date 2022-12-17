from paho.mqtt import client as mqtt_client
from datetime import datetime
import json
# --- InfluxDB
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- Broker MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "pucv/iot/m6/p2/g10"

# --- DB Influx E.Galdames
urlEG = "https://eastus-1.azure.cloud2.influxdata.com"
orgEG = "e.galdames.j@gmail.com"
tokenEG = "jl-092_-dWC5jK5W98f5sGmDhLLJNF_rJzV6FMEnZ4QvGxdgfxD5oD9hBwvCzxsiEn1T_3MOad_PcNG4gFV6GA=="

#conectarse al cliente InfluxDB
client = influxdb_client.InfluxDBClient(url=urlEG, token=tokenEG, org=orgEG)
write_api = client.write_api(write_options=SYNCHRONOUS)
bucketEG = "db_iot"

def connect_mqtt():
    def on_connect(client, userdata, flags, return_code):
        if return_code == 0:
            print("Conectado a MQTT broker! :)")
        else:
            print("Error, codigo %d\n", return_code)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        data = msg.payload
        info = json.loads(data)
        #print( json.loads(data) )      #mensaje Wemos -> Broker
        if info['ID'] == 'Sens1':
            ubi = "Santiago"
            point1 = Point("Sensor DS18B20").field("temp", info["Temperatura"]).tag("Ubicación",ubi)
        if info['ID'] == 'Sens2':
            ubi = "Concepción"
            point1 = Point("Sensor DS18B20").field("temp", info["Temperatura"]).tag("Ubicación",ubi)
        if info['ID'] == 'Sens3':
            ubi = "Valdivia"
            point1 = Point("Sensor DS18B20").field("temp", info["Temperatura"]).tag("Ubicación",ubi)
        print("Temperatura Actual: {}, Ubicación: {}, Tiempo {}".format(info["Temperatura"],ubi,datetime.now()))
        write_api.write(bucket=bucketEG, org=orgEG, record=point1)
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()