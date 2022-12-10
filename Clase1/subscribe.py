from paho.mqtt import client as mqtt_client
import time
import json

broker = "test.mosquitto.org"
port = 1883
topic = "pucv/iot/m6/p2/g9"
temp_avg = 0.0
temp_max = -128.0
temp_min = 300.0
temperatures = []


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
        parsed_json = json.loads(data)
        temperatures.append(float(parsed_json["temp"]))
        temp_max = max(temperatures)
        temp_min = min(temperatures)
        temp_avg = sum(temperatures) / len(temperatures)

        print("Temperature:", temperatures[-1], ",average:",
              temp_avg, ",Min:", temp_min, ",Max:", temp_max, "| Messages Received: ", len(temperatures))

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
