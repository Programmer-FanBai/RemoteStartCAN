"""Import libraries"""

import serial
import datetime
import time
from threading import Thread
from random import choice
from string import ascii_lowercase
from wthings_gateway.connectors.connector import Connector, log  # Import base class for connector and logger
from wthings_gateway.wt_utility.wt_utility import WTUtility
from wthings_gateway.extensions.plc.plc_converter import PlcUplinkConverter
from wthings_gateway.wt_utility.wt_communication import SiemensS7Net, SiemensPLCS, OmronFinsNet, MelsecMcNet, MelsecMcAsciiNet, MelsecA1ENet, AllenBradleyNet


class PLCConnector(Thread, Connector):  # Define a connector class, it should inherit from "Connector" class.
    plc_net = {"s7-300", SiemensS7Net}
    def __init__(self, gateway, config, connector_type):
        super().__init__()  # Initialize parents classes
        self.statistics = {'MessagesReceived': 0,
                           'MessagesSent': 0}  # Dictionary, will save information about count received and sent messages.
        self.__config = config  # Save configuration from the configuration file.
        self.__gateway = gateway  # Save gateway object, we will use some gateway methods for adding devices and saving data from them.
        self.__connector_type = connector_type  # Saving type for connector, need for loading converter
        self.setName(self.__config.get("name",
                                       "%s connector " % self.get_name() + ''.join(choice(ascii_lowercase) for _ in
                                                                                   range(
                                                                                       5))))  # get from the configuration or create name for logs.
        log.info("Starting %s connector", self.get_name())  # Send message to logger
        self.daemon = True  # Set self thread as daemon
        self.__stopped = False  # Service variable for check state
        self.connected = False  # Service variable for check connection to device
        self.plc = None
        self.devices = {}  # Dictionary with devices, will contain devices configurations, converters for devices and serial port objects
        self.load_converters()  # Call function to load converters and save it into devices dictionary
        self.load_device()
        log.info('connector %s initialization success.', self.get_name())  # Message to logger
        log.info("Devices in configuration file found: %s ",
                 '\n'.join(device for device in self.devices))  # Message to logger

    def __connect_to_server(self):  # Function for opening connection and connecting to server
        try:  # Start error handler
            host = self.__config.get('host', '127.0.0.1')
            port = self.__config.get('port', 102)
            plc_cpu = self.__config.get('plc_cpu', "s7-1200")
            if self.__config.get('name',None) == 'plc-melses':
                if "melsec-mc-binary" == self.__config.get("type",None):
                    plc_cpu = "melsec-mc-binary"
                elif "melsec-mc-ascii" == self.__config.get("type",None):
                    plc_cpu = "melsec-mc-ascii"
                elif "melsec-a1e" == self.__config.get("type",None):
                    plc_cpu = "melsec-a1e"
            elif self.__config.get('name',None) == 'plc-ab':
                plc_cpu = "allenbradley-logix-tcp"
            # omron-fins-tcp 欧姆龙 fins tcp
            #
            if plc_cpu == "s7-200":
                plc = SiemensS7Net(siemens=5, ipAddress=host, port=port)
            elif plc_cpu == "s7-300":
                plc = SiemensS7Net(siemens=SiemensPLCS.S300, ipAddress=host, port=port)
            elif plc_cpu == "s7-400":
                plc = SiemensS7Net(siemens=SiemensPLCS.S400, ipAddress=host, port=port)
            elif plc_cpu == "s7-1200":
                plc = SiemensS7Net(siemens=SiemensPLCS.S1200, ipAddress=host, port=port)
            elif plc_cpu == "s7-1500":
                plc = SiemensS7Net(siemens=SiemensPLCS.S1500, ipAddress=host, port=port)
            elif plc_cpu == "s7-200smart":
                plc = SiemensS7Net(siemens=SiemensPLCS.S200Smart, ipAddress=host, port=port)
            elif plc_cpu == "omron-fins-tcp":
                 plc = OmronFinsNet(ipAddress=host, port=port)
            elif plc_cpu == "melsec-mc-binary":
                plc = MelsecMcNet(ipAddress=host, port=port)
            elif plc_cpu == "melsec-mc-ascii":
                plc = MelsecMcAsciiNet(ipAddress=host, port=port)
            elif plc_cpu == "melsec-a1e":
                plc = MelsecA1ENet(ipAddress=host, port=port)
            elif plc_cpu == "allenbradley-logix-tcp":
                plc = AllenBradleyNet(ipAddress=host, port=port)
            if isinstance(plc, SiemensS7Net):
                plc.SetSlotAndRack(self.__config.get('rack', 0), self.__config.get('slot', 0))
            if isinstance(plc, OmronFinsNet):
                plc.SetSA1(self.__config.get('unitNo', 0))
            if isinstance(plc, AllenBradleyNet):
                plc.SetSlot(self.__config.get('slot', 0))
            log.info('connecting  %s %s:%s', self.get_name(), host, port)
            result = plc.ConnectServer()
        except Exception as e:
            log.exception(e)
            time.sleep(10)
        else:  # if no exception handled - add device and change connection state
            if result.IsSuccess:
                # self.__gateway.add_device(self.devices[device]["device_config"]["name"], {"connector": self},
                #                           self.devices[device]["device_config"]["type"])
                self.connected = True
                self.plc = plc
                self.__available_functions = {
                    "bit": self.plc.ReadBool,
                    "short": self.plc.ReadInt16,
                    "int": self.plc.ReadInt32,
                    "long": self.plc.ReadInt64,
                    "float": self.plc.ReadFloat,
                    "double": self.plc.ReadDouble,
                    "string": self.plc.ReadString,
                }
                log.info('connetct success %s', self.get_name())
            else:
                self.connected = False
                self.plc = None
                self.__available_functions = None
                log.error('connetct fail %s %s:%s message:%s', self.get_name(), host, port, result.Message)
                time.sleep(10)

    def load_device(self):
        pass

    def open(self):  # Function called by gateway on start
        self.__stopped = False
        self.start()

    def get_name(self):  # Function used for logging, sending data and statistic
        return self.name

    def is_connected(self):  # Function for checking connection state
        return self.connected

    def load_converters(self):  # Function for search a converter and save it.
        devices_config = self.__config.get('devices')
        try:
            if devices_config:
                for device_config in devices_config:
                    if device_config.get('converter'):
                        converter = WTUtility.check_and_import(self.__connector_type, device_config['converter'])
                        self.devices[device_config['deviceName']] = {'converter': converter(device_config),
                                                               'device_config': device_config}
                    else:
                        converter = PlcUplinkConverter(device_config)
                        self.devices[device_config['deviceName']] = {'converter': converter,
                                                                     'device_config': device_config}
            else:
                log.error('Section "devices" in the configuration not found. A custom connector %s has being stoppe'
                          'd.', self.get_name())
                self.close()
        except Exception as e:
            log.exception(e)

    def run(self):  # Main loop of thread
        while not self.__stopped:
            try:
                if not self.is_connected():
                    self.__connect_to_server()
                if self.is_connected():
                    ping_result = self.plc.GetAvailableSocket()
                    if ping_result.IsSuccess:
                        start_ts = time.time()
                        for device in self.devices:
                            try:
                                device_config = self.devices[device]['device_config']
                                data_from_device = {"timeseries": {},
                                                    "attributes": {}}
                                for n, m in enumerate(data_from_device):
                                    for i, j in enumerate(device_config[m]):
                                        result = self.__available_functions.get(j.get("type"), self.plc.ReadInt16)(j["path"])
                                        if result.IsSuccess:
                                            #print(self.name, self.getName(), "start-----------", datetime.datetime.now())
                                            data_from_device[m][j["key"]] = result.Content
                                converted_data = self.devices[device]['converter'].convert(self.devices[device]['device_config'], data_from_device)
                                if self.__gateway:
                                    self.__gateway.send_to_storage(self.get_name(), converted_data)
                            except Exception as e:
                                log.exception(e)
                                raise e
                        #print(self.name, self.getName(), "end-----------", datetime.datetime.now(), int((time.time()-start_ts)*1000))
                        time.sleep(self.__config.get('scanPeriodInMillis', 5000)/1000)
                    else:
                        self.connected = False
                        log.info('disconnetct connector %s', self.get_name())
            except Exception as e:
                log.exception(e)
                self.close()

    def close(self):  # Close connect function, usually used if exception handled in gateway main loop or in connector main loop
        self.__stopped = True
        log.info("Stopped %s connector", self.get_name())  # Send message to logger
        if self.plc:
            self.plc.ConnectClose()

    def on_attributes_update(self, content):  # Function used for processing attribute update requests from WThings
        log.debug(content)
        if self.devices.get(content["device"]) is not None:
            device_config = self.devices[content["device"]].get("device_config")
            if device_config is not None:
                log.debug(device_config)
                if device_config.get("attributeUpdates") is not None:
                    requests = device_config["attributeUpdates"]
                    for request in requests:
                        attribute = request.get("attributeOnWThings")
                        log.debug(attribute)
                        if attribute is not None and attribute in content["data"]:
                            try:
                                value = content["data"][attribute]
                                str_to_send = str(
                                    request["stringToDevice"].replace("${" + attribute + "}", str(value))).encode(
                                    "UTF-8")
                                self.devices[content["device"]]["serial"].write(str_to_send)
                                log.debug("Attribute update request to device %s : %s", content["device"], str_to_send)
                                time.sleep(.01)
                            except Exception as e:
                                log.exception(e)

    def server_side_rpc_handler(self, content):
        pass

if __name__ == '__main__':
    # plc_1500 = SiemensS7Net(SiemensPLCS.S1500, "114.115.152.144", 20102)
    # result = plc_1500.ConnectServer()
    # if result.IsSuccess:
    #     print("连接成功")
    #     sensor_exit_h = plc_1500.ReadInt16("DB1320.2")
    #     print(sensor_exit_h.ErrorCode)
    #     print(sensor_exit_h.Message)
    #     print(sensor_exit_h.Content)
    # else:
    #     print("连接失败")
    print(b'\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\xb2\x00j\x00\xcc\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00SB1021\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.hex())
    print(b'f\x00z\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.hex())