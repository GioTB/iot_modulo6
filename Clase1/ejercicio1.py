from paho.mqtt import client as mqtt_client
import time
import json

broker = "test.mosquitto.org"
port = 1883
topic = "pucv/iot/casa"

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

def publish(client):
    counter = 0
    while True:
        time.sleep(3)
        msg = json.dumps({ "counter": counter, "source": "los profes", "temp": 30.1, "sensor_id": "WemosD1_23423" })
        result = client.publish(topic, msg)
        status = result[0]

        if status == 0:
            print("Mensaje enviado")
        else:
            print("error al enviar")
        counter += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
