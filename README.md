# Home-Metrics V1.beta


## Hardware

### Devices Info

  - Board for ESP-WROOM-32 - `ESP DEV MODULE`
  - Arduino Nano

### Stuff:

  - Ethernet: `W5500`
  - Temp/Humid: `SHT2x`


# Docs ESP


### Pinouts

## STh2x
```
3v3   -   +
GND   -   -
22    -   SCL
21    -   SDA
```

# ESP Firmware Configs

### Config:
```c++
// Initialization Door Sensor's Pins
const byte sensor_1 = 4;
const byte sensor_2 = 5;

// MQTT Broker Config
const char * broker = "broker.domain.com";

// Wifi Settings
const char* ssid = "SSID";
const char* ssid_password = "PASSWORD";

/*********
Next needs to use [topic_root + "endpoint"]
IMPORTANT, For HM Project use fist path as "hm/..."
*********/

/*********
For HM last paths:
Temperature: ".../temp"
Humidity: ".../humid"
Sensor: ".../sensor<number>"
*********/
const String topic_root = "path/to/end";
const char * deviceid = "DEVICE_ID";

// Credentials for Auth in Broker
const char * username = "USER";
const char * password = "SOME_PASSWORD";

// If need custom port, and add to
// 154:   client.begin(broker, net);
// int port = 1883;

```
