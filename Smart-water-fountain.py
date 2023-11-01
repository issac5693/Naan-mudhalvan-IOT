import WiFi # library for wifi
import PubSubClient # library for MQTT
from Ultrasonic import Ultrasonic

ultrasonic = Ultrasonic(2, 4)
distance = 0.0

def callback(subscribetopic, payload, payloadLength):
    pass

# -------credentials of IBM Accounts------

ORG = "6yocvj" # IBM ORGANIZATION ID
DEVICE_TYPE = "smartdustbin" # Device type mentioned in IBM Watson IoT Platform
DEVICE_ID = "12345" # Device ID mentioned in IBM Watson IoT Platform
TOKEN = "12345678" # Token
data3 = ""

# -------- Customise the above values --------
server = ORG + ".messaging.internetofthings.ibmcloud.com" # Server Name
publishTopic = "iot-2/evt/Data/fmt/json" # topic name and type of event perform and format in which data to be sent
subscribetopic = "iot-2/cmd/test/fmt/String" # cmd REPRESENT command type AND COMMAND IS TEST OF FORMAT STRING
authMethod = "use-token-auth" # authentication method
token = TOKEN
clientId = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID # client id

# -----------------------------------------
wifiClient = WiFiClient() # creating the instance for wifi client
client = PubSubClient(server, 1883, callback, wifiClient) # calling the predefined client id by passing parameters like server id, port, and wifi credential

def setup(): # configuring the ESP32
    Serial.begin(115200)
    delay(10)
    Serial.println()
    wificonnect()
    mqttconnect()

def loop(): # Recursive Function
    distance = ultrasonic.read(CM)
    Serial.print("Distance in CM: ")
    Serial.println(distance)
    delay(1000)
    PublishData(distance)
    delay(1000)
    if not client.loop():
        mqttconnect()

# .....................................retrieving to Cloud...............................

def PublishData(distance):
    mqttconnect() # function call for connecting to IBM
    """
    creating the String in in form JSON to update the data to IBM cloud
    """
    payload = "{\"distance\":" + str(distance) + "}"
    Serial.print("Sending payload: ")
    Serial.println(payload)
    if client.publish(publishTopic, payload):
        Serial.println("Publish ok") # if it successfully uploads data on the cloud then it will print publish ok in Serial monitor or else it will print publish failed
    else:
        Serial.println("Publish failed")

def mqttconnect():
    if not client.connected():
        Serial.print("Reconnecting client to ")
        Serial.println(server)
        while not client.connect(clientId, authMethod, token):
            Serial.print(".")
            delay(500)
        initManagedDevice()
        Serial.println()

def wificonnect(): # function definition for wificonnect
    Serial.println()
    Serial.print("Connecting to ")
    WiFi.begin("Wokwi-GUEST", "", 6) # passing the wifi credentials to establish the connection
    while WiFi.status() != WL_CONNECTED:
        delay(500)
        Serial.print(".")
    Serial.println("")
    Serial.println("WiFi connected")
    Serial.println("IP address: ")
    Serial.println(WiFi.localIP())

def initManagedDevice():
    if client.subscribe(subscribetopic):
        Serial.println(subscribetopic)
        Serial.println("subscribe to cmd OK")
    else:
        Serial.println("subscribe to cmd FAILED")

def callback(subscribetopic, payload, payloadLength):
    Serial.print("callback invoked for topic: ")
    Serial.println(subscribetopic)
    for i in range(payloadLength):
        # Serial.print((char)payload[i])
        data3 += chr(payload[i])
    Serial.println("data: " + data3)
    data3 = ""
