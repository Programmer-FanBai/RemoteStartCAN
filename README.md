# WaveletThings IoT Gateway  

The Waveletthings **IoT Gateway** is an open-source solution that allows you to integrate devices connected to legacy and third-party systems with Waveletthings.  

Waveletthings is an open-source IoT platform for data collection, processing, visualization, and device management. See [**What is Waveletthings?**](https://wthings.io/docs/getting-started-guides/what-is-wthings/) if you are new platform user.  

[**What is WaveletThings IoT Gateway?**](https://wthings.io/docs/iot-gateway/what-is-iot-gateway/)  
[**Getting started with WaveletThings IoT Gateway**](https://wthings.io/docs/iot-gateway/getting-started/)

[![**What is WaveletThings IoT Gateway?**](https://wthings.io/images/gateway/python-gateway-animd-ab-ff.svg)](https://wthings.io/docs/iot-gateway/what-is-iot-gateway/)

### Gateway features

Waveletthings IoT Gateway provides following features:  

 - [**OPC-UA** connector](https://wthings.io/docs/iot-gateway/config/opc-ua/) to collect data from devices that are connected to OPC-UA servers.
 - [**MQTT** connector](https://wthings.io/docs/iot-gateway/config/mqtt/) to collect data that is published to external MQTT brokers. 
 - [**Modbus** connector](https://wthings.io/docs/iot-gateway/config/modbus/) to collect data from Modbus servers and slaves.
 - [**BLE** connector](https://wthings.io/docs/iot-gateway/config/ble/) to collect data from BLE devices.
 - [**Request** connector](https://wthings.io/docs/iot-gateway/config/request/) to collect data from HTTP API.
 - [**CAN** connector](https://wthings.io/docs/iot-gateway/config/can/) to collect data using CAN protocol.
 - [**BACnet** connector](https://wthings.io/docs/iot-gateway/config/bacnet/) to collect data from devices using BACnet protocol.
 - [**ODBC** connector](https://wthings.io/docs/iot-gateway/config/odbc/) to collect data from ODBC databases.
 - [**Custom** connector](https://wthings.io/docs/iot-gateway/custom/) to collect data from custom protocols.
 - **Persistence** of collected data to guarantee data delivery in case of network and hardware failures.
 - **Automatic reconnect** to Waveletthings cluster.
 - Simple yet powerful **mapping** of incoming data and messages **to unified format**.
 - [Remote logging feature](https://wthings.io/docs/iot-gateway/guides/how-to-enable-remote-logging/) to monitor the gateway status through the WaveletThings WEB interface.
 - [RPC gateway methods](https://wthings.io/docs/iot-gateway/guides/how-to-use-gateway-rpc-methods/) to control and get information from the gateway through WaveletThings WEB interface.
  
### Architecture  

The IoT Gateway is built on top of **Python**, however is different from similar projects that leverage OSGi technology.
The idea is distantly similar to microservices architecture.  
The gateway supports custom connectors to connect to new devices or servers and custom converters for processing data from devices.  
Especially, when we are talking about language APIs and existing libraries to work with serial ports, GPIOs, I2C, and new modules and sensors that are released every day.  

The Gateway provides simple integration APIs, and encapsulates common Waveletthings related tasks: device provisioning, local data persistence and delivery, message converters and other.  
For processing data from devices you also can write custom converter, it will receive information from device and send it to converter to convert to unified format before sending it to the WaveletThings cluster.  

## Support

 - [Community chat](https://gitter.im/wthings/chat)
 - [Q&A forum](https://groups.google.com/forum/#!forum/wthings)
 - [Stackoverflow](http://stackoverflow.com/questions/tagged/wthings)
 
**Don't forget to star the repository to show your ❤️ and support.**

## Licenses

This project is released under [Apache 2.0 License](./LICENSE).
