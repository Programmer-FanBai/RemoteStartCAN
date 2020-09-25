#!/usr/bin/python
# encoding:utf-8


"""
    @author Liberty
    @file   wt_expand_parse.py
    @time   2020/7/22 13:08
"""
from base64 import b64encode, b64decode
from simplejson import dumps, loads
from logging import getLogger

LOG = getLogger("service")


class Expand(object):
    def __init__(self, id):
        self.id = id


class ModbusExpand(Expand):
    modbus = None

    def __init__(self, modbus_config, id):
        super(ModbusExpand, self).__init__(id)
        for n, m in enumerate(modbus_config):
            type = "serial" if m["transport"]["type"] == "rtu" else m["transport"]["type"]
            devices = m["devices"]
            for device in devices:
                if not device["attributes"]:
                    device.pop("attributes")
                if not device["timeseries"]:
                    device.pop("timeseries")
            name = self.id
            if type == "serial":
                self.modbus = {
                    "name": name,
                    "config": {
                        "server": {
                            "name": name,
                            "type": type,
                            "method": m["transport"]["encoding"],
                            "port": m["transport"]["portName"],
                            "baudrate": m["transport"]["baudRate"],
                            "timeout": m["transport"]["timeout"]/1000,
                            "devices": devices
                        }
                    }
                }
            elif type == "tcp":
                self.modbus = {
                    "name": name,
                    "config": {
                        "server": {
                            "name": name,
                            "type": type,
                            "host": m["transport"]["host"],
                            "port": m["transport"]["port"],
                            "method": "socket",
                            "timeout": m["transport"]["timeout"]/1000,
                            "devices": devices
                        }
                    }
                }
            self.connectors = {
                "name": name,
                "type": "modbus",
                "configuration": name+".json"
            }
        print("self.modbus=", self.modbus)

    def get_expand(self):
        return self.modbus

    def get_connectors(self):
        return self.connectors


class OpcDAExpand(Expand):
    opcda = None

    def __init__(self, opcda_config, id):
        super(OpcDAExpand, self).__init__(id)
        for n, m in enumerate(opcda_config):
            name = self.id
            self.opcda = {
                "name": name,
                "config": {
                    "server": {
                        "opcProxyIp": m["host"],
                        "opcProxyPort": m["port"],
                        "opcServer": m["applicationOpcServer"],
                        "separator": m["separator"],
                        "collectInterval": m["scanPeriodInSeconds"],
                        "timeout": m["timeoutInMillis"],
                        "devices": m["mapping"]
                    }
                }
            }
            self.connectors = {
                "name": name,
                "type": "opcda",
                "configuration": "%s.json" % (name, )
            }
        print("self.opcda=", self.opcda)

    def get_expand(self):
        return self.opcda

    def get_connectors(self):
        return self.connectors


class PLCSiemensS7Expand(Expand):
    plc_s7 = None

    def __init__(self, plc_s7_config, id):
        super(PLCSiemensS7Expand, self).__init__(id)
        for n, m in enumerate(plc_s7_config):
            name = self.id
            self.plc_s7 = {
                "name": name,
                "config": {
                    "host": m["host"],
                    "port": m["port"],
                    "scanPeriodInMillis": m["scanPeriodInSeconds"],
                    "slot": m["slot"],
                    "rack": m["rack"],
                    "plc_cpu": m["cpuType"],
                    "timeoutInMillis": m["timeoutInMillis"],
                    "devices": m["mapping"]
                }
            }
            self.connectors = {
                "name": name,
                "type": "plc",
                "configuration": "%s.json" % (name, )
            }
        print("self.plc_s7=", self.plc_s7)

    def get_expand(self):
        return self.plc_s7

    def get_connectors(self):
        return self.connectors


class PLCOmronExpand(Expand):
    omron = None

    def __init__(self, omron_config, id):
        super(PLCOmronExpand, self).__init__(id)
        for n, m in enumerate(omron_config):
            name = self.id
            self.omron = {
                "name": name,
                "config": {
                    "host": m["host"],
                    "port": m["port"],
                    "scanPeriodInMillis": m["scanPeriodInSeconds"],
                    "unitNo": m["unitNo"],
                    "plc_cpu": m["cpuType"],
                    "timeoutInMillis": m["timeoutInMillis"],
                    "devices": m["mapping"]
                }
            }
            self.connectors = {
                "name": name,
                "type": "plc",
                "configuration": "%s.json" % (name, )
            }
        print("self.omron=", self.omron)

    def get_expand(self):
        return self.omron

    def get_connectors(self):
        return self.connectors


class PLCAllenBradleyExpand(Expand):
    allenbradley = None

    def __init__(self, allenbradley_config, id):
        super(PLCAllenBradleyExpand, self).__init__(id)
        for n, m in enumerate(allenbradley_config):
            name = self.id
            self.omron = {
                "name": name,
                "config": {
                    "host": m["host"],
                    "port": m["port"],
                    "scanPeriodInMillis": m["scanPeriodInSeconds"],
                    "unitNo": m["unitNo"],
                    "plc_cpu": m["cpuType"],
                    "timeoutInMillis": m["timeoutInMillis"],
                    "devices": m["mapping"]
                }
            }
            self.connectors = {
                "name": name,
                "type": "plc",
                "configuration": "%s.json" % (name, )
            }
        print("self.omron=", self.omron)

    def get_expand(self):
        return self.omron

    def get_connectors(self):
        return self.connectors


class PLCMelsecExpand(Expand):
    melsec = None

    def __init__(self, melsec_config, id):
        super(PLCMelsecExpand, self).__init__(id)
        for n, m in enumerate(melsec_config):
            name = self.id
            self.melsec = {
                "name": name,
                "config": {
                    "host": m["host"],
                    "port": m["port"],
                    "scanPeriodInMillis": m["scanPeriodInSeconds"],
                    "type": m["cpuType"],
                    "timeoutInMillis": m["timeoutInMillis"],
                    "devices": m["mapping"]
                }
            }
            self.connectors = {
                "name": name,
                "type": "plc",
                "configuration": "%s.json" % (name, )
            }
        print("self.melsec=", self.melsec)

    def get_expand(self):
        return self.melsec

    def get_connectors(self):
        return self.connectors


class PLCAllenBradleyExpand(Expand):
    allenbradley = None

    def __init__(self, allenbradley_config, id):
        super(PLCAllenBradleyExpand, self).__init__(id)
        for n, m in enumerate(allenbradley_config):
            name = self.id
            self.allenbradley = {
                "name": name,
                "config": {
                    "host": m["host"],
                    "port": m["port"],
                    "scanPeriodInMillis": m["scanPeriodInSeconds"],
                    "type": m["cpuType"],
                    "slot": m["slot"],
                    "timeoutInMillis": m["timeoutInMillis"],
                    "devices": m["mapping"]
                }
            }
            self.connectors = {
                "name": name,
                "type": "plc",
                "configuration": "%s.json" % (name, )
            }
        print("self.allenbradley=", self.allenbradley)

    def get_expand(self):
        return self.allenbradley

    def get_connectors(self):
        return self.connectors


def format_mapping(mapping, n=None, hastype=False):
    for i, v in enumerate(mapping):
        if n:
            v["serverId"] = n
        # 遍历mapping，获取每个设备属性映射
        device_attributes = v["attributes"]
        device_timeseries = v["timeseries"]
        for n, m in enumerate(device_attributes):
            if "type" in m:
                if not hastype:
                    m.pop("type")
                else:
                    if m.get("type") and m["type"] == "long":
                        m["type"] = "int"
                m["path"] = m.pop("value")
        for n, m in enumerate(device_timeseries):
            if "type" in m:
                if not hastype:
                    m.pop("type")
                else:
                    if m.get("type") and m["type"] == "long":
                        m["type"] = "int"
                m["path"] = m.pop("value")
    return mapping

def process_extend(configuration, old_general_configuration_file, old_logs_configuration):
    # 最新代码
    # 适配现有服务器网关扩展
    conf = {"wthings": old_general_configuration_file}
    conf["wthings"]["logs"] = b64encode(old_logs_configuration.replace('\n', '}}').encode("UTF-8"))
    # conf = {"wthings": {
    #     "wthings": {
    #         "host": "things.xiaobodata.com",
    #         "port": 1883,
    #         "remoteConfiguration": True,
    #         "security": {
    #             "accessToken": "rknoNpDksmYbMeIt0PRN"
    #         }
    #     },
    #     "storage": {
    #         "type": "memory",
    #         "read_records_count": 100,
    #         "max_records_count": 100000
    #     },
    #     "logs": "W2xvZ2dlcnNdfX1rZXlzPXJvb3QsIHNlcnZpY2UsIGNvbm5lY3RvciwgY29udmVydGVyLCB0Yl9jb25uZWN0aW9uLCBzdG9yYWdlLCBleHRlbnNpb259fVtoYW5kbGVyc119fWtleXM9Y29uc29sZUhhbmRsZXIsIHNlcnZpY2VIYW5kbGVyLCBjb25uZWN0b3JIYW5kbGVyLCBjb252ZXJ0ZXJIYW5kbGVyLCB0Yl9jb25uZWN0aW9uSGFuZGxlciwgc3RvcmFnZUhhbmRsZXIsIGV4dGVuc2lvbkhhbmRsZXJ9fVtmb3JtYXR0ZXJzXX19a2V5cz1Mb2dGb3JtYXR0ZXJ9fVtsb2dnZXJfcm9vdF19fWxldmVsPUVSUk9SfX1oYW5kbGVycz1jb25zb2xlSGFuZGxlcn19W2xvZ2dlcl9jb25uZWN0b3JdfX1sZXZlbD1JTkZPfX1oYW5kbGVycz1jb25uZWN0b3JIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1xdWFsbmFtZT1jb25uZWN0b3J9fVtsb2dnZXJfc3RvcmFnZV19fWxldmVsPUlORk99fWhhbmRsZXJzPXN0b3JhZ2VIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1xdWFsbmFtZT1zdG9yYWdlfX1bbG9nZ2VyX3RiX2Nvbm5lY3Rpb25dfX1sZXZlbD1JTkZPfX1oYW5kbGVycz10Yl9jb25uZWN0aW9uSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19cXVhbG5hbWU9dGJfY29ubmVjdGlvbn19W2xvZ2dlcl9zZXJ2aWNlXX19bGV2ZWw9SU5GT319aGFuZGxlcnM9c2VydmljZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fXF1YWxuYW1lPXNlcnZpY2V9fVtsb2dnZXJfY29udmVydGVyXX19bGV2ZWw9SU5GT319aGFuZGxlcnM9Y29ubmVjdG9ySGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19cXVhbG5hbWU9Y29udmVydGVyfX1bbG9nZ2VyX2V4dGVuc2lvbl19fWxldmVsPUlORk99fWhhbmRsZXJzPWNvbm5lY3RvckhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fXF1YWxuYW1lPWV4dGVuc2lvbn19W2hhbmRsZXJfY29uc29sZUhhbmRsZXJdfX1jbGFzcz1TdHJlYW1IYW5kbGVyfX1sZXZlbD1JTkZPfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1hcmdzPShzeXMuc3Rkb3V0LCl9fVtoYW5kbGVyX2Nvbm5lY3RvckhhbmRsZXJdfX1sZXZlbD1JTkZPfX1jbGFzcz1sb2dnaW5nLmhhbmRsZXJzLlRpbWVkUm90YXRpbmdGaWxlSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19YXJncz0oIi4vbG9ncy9jb25uZWN0b3IubG9nIiwgImQiLCAxLCA3LCl9fVtoYW5kbGVyX3N0b3JhZ2VIYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3Mvc3RvcmFnZS5sb2ciLCAiZCIsIDEsIDcsKX19W2hhbmRsZXJfc2VydmljZUhhbmRsZXJdfX1sZXZlbD1JTkZPfX1jbGFzcz1sb2dnaW5nLmhhbmRsZXJzLlRpbWVkUm90YXRpbmdGaWxlSGFuZGxlcn19Zm9ybWF0dGVyPUxvZ0Zvcm1hdHRlcn19YXJncz0oIi4vbG9ncy9zZXJ2aWNlLmxvZyIsICJkIiwgMSwgNywpfX1baGFuZGxlcl9jb252ZXJ0ZXJIYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3MvY29udmVydGVyLmxvZyIsICJkIiwgMSwgMywpfX1baGFuZGxlcl9leHRlbnNpb25IYW5kbGVyXX19bGV2ZWw9SU5GT319Y2xhc3M9bG9nZ2luZy5oYW5kbGVycy5UaW1lZFJvdGF0aW5nRmlsZUhhbmRsZXJ9fWZvcm1hdHRlcj1Mb2dGb3JtYXR0ZXJ9fWFyZ3M9KCIuL2xvZ3MvZXh0ZW5zaW9uLmxvZyIsICJkIiwgMSwgMywpfX1baGFuZGxlcl90Yl9jb25uZWN0aW9uSGFuZGxlcl19fWxldmVsPUlORk99fWNsYXNzPWxvZ2dpbmcuaGFuZGxlcnMuVGltZWRSb3RhdGluZ0ZpbGVIYW5kbGVyfX1mb3JtYXR0ZXI9TG9nRm9ybWF0dGVyfX1hcmdzPSgiLi9sb2dzL3RiX2Nvbm5lY3Rpb24ubG9nIiwgImQiLCAxLCAzLCl9fVtmb3JtYXR0ZXJfTG9nRm9ybWF0dGVyXX19Zm9ybWF0PSIlKGFzY3RpbWUpcyAtICUobGV2ZWxuYW1lKXMgLSBbJShmaWxlbmFtZSlzXSAtICUobW9kdWxlKXMgLSAlKGxpbmVubylkIC0gJShtZXNzYWdlKXMiIH19ZGF0ZWZtdD0iJVktJW0tJWQgJUg6JU06JVMifX19fX19fX19fX19fX19fX19"
    # }}
    configuration = loads(configuration)
    # configuration = [
    #     {
    #         "type": "OPC DA",
    #         "configuration": {
    #             "servers": [
    #                 {
    #                     "applicationName": "OPC-DA client",
    #                     "applicationOpcServer": "Matrikon.OPC.Simulation",
    #                     "host": "localhost",
    #                     "port": 7766,
    #                     "scanPeriodInSeconds": 10,
    #                     "timeoutInMillis": 5000,
    #                     "mapping": [
    #                         {
    #                             "deviceName": "TEST",
    #                             "devicePath": "Random",
    #                             "attributes": [
    #                                 {
    #                                     "key": "Tag1",
    #                                     "type": "string",
    #                                     "value": "Int4"
    #                                 }
    #                             ],
    #                             "timeseries": []
    #                         }
    #                     ]
    #                 }
    #             ]
    #         },
    #         "id": "TEST"
    #     }
    # ]
    opcuas = []
    modbus = []
    opcdas = []
    plcs = []
    sockets = []
    connectors = []
    print("configuration=", configuration)
    for i, v in enumerate(configuration):
        if v["type"] == "OPC UA":
            for n, m in enumerate(v["configuration"]["servers"]):
                url = "admin@%s:%s%s" % (m["host"], m["port"], m["applicationUri"])
                applicationName = m["applicationName"]
                opcuas.append({
                    "name": applicationName,
                    "config": {
                        "server": {
                            "name": applicationName,
                            "url": url,
                            "scanPeriodInMillis": m["scanPeriodInSeconds"] * 1000,
                            "timeoutInMillis": m["timeoutInMillis"],
                            "security": "Basic128Rsa15",
                            "showMap": False,
                            "identity": {
                                "type": "anonymous"
                            },
                            "mapping": format_mapping(m["mapping"])
                        },
                        "name": applicationName
                    }
                })
                connectors.append({
                    "name": applicationName,
                    "type": "opcua",
                    "configuration": "%s.json" % (applicationName, )
                })
        if v["type"] == "MODBUS":
            modbus_expand = ModbusExpand(v["configuration"]["servers"], v["id"])
            modbus.append(modbus_expand.get_expand())
            connectors.append(modbus_expand.get_connectors())
        if v["type"] == "OPC DA":
            opcda_expand = OpcDAExpand(v["configuration"]["servers"], v["id"])
            opcdas.append(opcda_expand.get_expand())
            connectors.append(opcda_expand.get_connectors())
        if v["type"] == "PLC-SIEMENS":
            plc_siemens_s7 = PLCSiemensS7Expand(v["configuration"]["servers"], v["id"])
            plcs.append(plc_siemens_s7.get_expand())
            connectors.append(plc_siemens_s7.get_connectors())
        if v["type"] == "PLC-OMRON":
            plc_omron = PLCOmronExpand(v["configuration"]["servers"], v["id"])
            plcs.append(plc_omron.get_expand())
            connectors.append(plc_omron.get_connectors())
        if v["type"] == "PLC-MELSEC":
            plc_melsec = PLCMelsecExpand(v["configuration"]["servers"], v["id"])
            plcs.append(plc_melsec.get_expand())
            connectors.append(plc_melsec.get_connectors())
        if v["type"] == "PLC-AB":
            plc_melsec = PLCMelsecExpand(v["configuration"]["servers"], v["id"])
            plcs.append(plc_melsec.get_expand())
            connectors.append(plc_melsec.get_connectors())
        if v["type"] == "SOCKET":
            for n, m in enumerate(v["configuration"]["servers"]):
                applicationName = m["applicationName"]
                sockets.append({
                    "name": applicationName,
                    "config": {
                        "name": applicationName,
                        "host": m["host"],
                        "port": m["port"],
                        "type": m["type"],
                        "timeoutInMillis": m["timeoutInMillis"]
                    }
                })
                connectors.append({
                    "name": applicationName,
                    "type": "socket",
                    "configuration": "%s.json" % (applicationName, )
                })
    # conf[type] 是相当于解析json文件到字典里
    conf["opcua"] = opcuas
    conf["modbus"] = modbus
    conf["opcda"] = opcdas
    conf["plc"] = plcs
    conf["socket"] = sockets
    # conf["wthings"]["connectors"] 是配置文件
    conf["wthings"]["connectors"] = connectors
    return conf


if __name__ == '__main__':
    pass