#include <WiFi.h>
#include <PubSubClient.h>

#define Subirpista 17
#define Bajarpista 16
//#define Detener 4

int tiempo = 10000;
// Update these with values suitable for your network.

const char* ssid = "LUIS_ALVARADO";
const char* password = "LEAC_2022";
const char* mqtt_server = "broker.mqtt-dashboard.com";
const char* outTopic = "Primero";
const char* inTopic = "Segundo";

String _topic;
String _payload;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
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
    Serial.println((char)payload[i]);
  }
//////////////////////////////////////////////////////////////////
  Serial.println();
  digitalWrite(D5, HIGH);
  delay(100);
  digitalWrite(D5, LOW);

  if((char)payload[0] == '1'){
    digitalWrite(D6, HIGH);
    }else{
      digitalWrite(D6, LOW);
      }
///////////////////////////////////////////////////////////////////
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
       // Conexion con los nodos nombre exactos..........
      client.subscribe(outTopic);
      client.subscribe(inTopic);
      client.publish(outTopic, "Hola Edu");
      
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
  pinMode(D3, INPUT);
  pinMode(D5, OUTPUT);
  pinMode(D6, OUTPUT);
  pinMode(D7, OUTPUT);

  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  if(!client.connected()){
    reconnect();
    }
    digitalWrite(D5, LOW)
    digitalWrite(D6, LOW)
    digitalWrite(D7, LOW)
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  digitalWrite(D0, HIGH);
  
  unsigned long now=millis();
  if(now - lastMsg > 5000){
    lastMsg = now;
    ++value;
    snprintf(msg, MSG_BUFFER_SIZE, "hoLAluisalVARADO #%ld", value);
    Serial.print(now);
    Serial.print("Mensaje publicado: ");
    Serial.println(msg);
    client.publish(outTopic, msg);
    
    }
}
