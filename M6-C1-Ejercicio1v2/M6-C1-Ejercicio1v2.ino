/*
 MQTT Pub/Sub code
Connect Wifi
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DallasTemperature.h>  //Sensor Tº
#include <OneWire.h>            //Protocolo COM
//#include <ArduinoJson.h>

#define DallasT D5
#define MSG_BUFFER_SIZE	(100)

OneWire OneWire(DallasT);
DallasTemperature sensors(&OneWire);

float Temp;
// Update these with values suitable for your network.

char* ssid = "DEPTO 410";
char* password = "123581321DLyEG";

//const char* mqtt_server = "broker.mqtt-dashboard.com";
const char* mqtt_server = "test.mosquitto.org";
int port = 1883;
//const char* susTopic = "Prueba/IoT/Stgo";
const char* PubTopic = "pucv/iot/m6/p2/g10";
const char* SusTopic = "Prueba/IoT/Stgo";

//StaticJsonDocument<200> jsonbuffer;       //Revisar Json
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

char msg[MSG_BUFFER_SIZE];
int value = 0;
time_t tValue;
int timeDelay = 5000;

//Conectar Wifi Local
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(350);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();                     //Inicia connect Wifi
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  sensors.begin();
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //Temperatura
  sensors.requestTemperatures();
  Temp = sensors.getTempCByIndex(0);

  unsigned long now = millis();

  if (now - lastMsg > timeDelay) {
    lastMsg = now;
    snprintf (msg, MSG_BUFFER_SIZE, "{ \"ID\": \"Sens1\",\"Sensor\": \"DS18B20\",\"Temperatura\": %.2f }", Temp);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(PubTopic, msg);
  }
  client.subscribe(SusTopic);
}
