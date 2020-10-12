# WaveletThings IoT Gateway  

小波物联平台网关

### Gateway features

Waveletthings IoT Gateway provides following features:  

 - [**OPC-UA** connector] 从OPC-UA服务器收集数据。
 - [**OPC-DA** connector] 从OPC-DA服务器收集数据。
 - [**PLC** connector] 从PLC(西门子,欧姆龙,施耐德,三菱,罗克威尔)收集数据。
 - [**MQTT** connector] 收集发布到外部MQTT代理的数据。 
 - [**Modbus** connector] 从Modbus服务器和从服务器收集数据。
 - [**BLE** connector] 从BLE设备收集数据.
 - [**Request** connector]从HTTP API收集数据。
 - [**CAN** connector] 使用CAN协议收集数据。
 - [**BACnet** connector] 使用BACnet协议从设备收集数据。
 - [**ODBC** connector] 从ODBC数据库收集数据。
 - [**Custom** connector] 从自定义协议收集数据。
 - **持久性** 保证在网络和硬件故障时数据的传输。
 - **自动重新连接** Waveletthings集群。
 - **映射输入的消息到统一的格式**.
  
## instructions

### config # 配置文件
### connectors # 连接器
### extensions # 扩展连接器
### gateway # 网关类
### storage # 持久化类
### wt_client # 客户端和网关基类
### wt_utility # 工具类

## use

### 1.修改服务器地址和token。

打开config/wt_gateway.yaml文件
wthings.host 修改为服务器地址(默认为things.xiaobodata.com)
wthings.port 修改为服务器端口(默认为1883)
wthings.security.accessToken 修改为网关访问令牌

### 2.启动网关

运行wt_gateway.py的main函数启动网关。

### 3.添加连接器

3.1 选定要连接的设备,然后在config里添加连接器文件
3.2 然后在config/wt_gateway.yaml里添加连接器配置

例如:
```
connectors:
- {configuratimon: AlarmLed.json, nae: AlarmLed, type: modbus}
```
