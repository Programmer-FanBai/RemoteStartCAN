from wthings_gateway.connectors.converter import Converter, log


class CustomOpcdaUplinkConverter(Converter):
    def __init__(self, config):
        self.tag_list = []  # 需要查询的tag列表
        self.__config = config
        self.full_path_key_map = {}
        devicePath = self.__config["devicePath"]
        separator = self.__config.get("separator", ".")
        if self.__config.get("attributes") is not None:
            for attribute in self.__config["attributes"]:
                attribute_full_path = "%s%s%s" % (devicePath, separator, attribute["path"])
                self.full_path_key_map[attribute_full_path] = {"key": attribute["key"], "uploadType": "attributes", "type": attribute["type"]}
                self.tag_list.append(attribute_full_path)
        if self.__config.get("timeseries") is not None:
            for timeserie in self.__config["timeseries"]:
                timeserie_full_path = "%s%s%s" % (devicePath, separator, timeserie["path"])
                self.full_path_key_map[timeserie_full_path] = {"key": timeserie["key"], "uploadType": "telemetry", "type": timeserie["type"]}
                self.tag_list.append(timeserie_full_path)
        self.deviceName = self.__config.get('deviceName', 'CustomSerialDevice')
        self.deviceType = self.__config.get('deviceType', 'default')
        self.devicePath = self.__config["devicePath"]
        self.result_dict = {
            'deviceName': self.deviceName,
            'deviceType': self.deviceType,
            'attributes': [],
            'telemetry': []
        }

    def get_tag_list(self):
        return self.tag_list

    def convert(self, config, data):
        self.result_dict["attributes"] = []
        self.result_dict["telemetry"] = []
        for i, v in enumerate(data):
            (name, val, qual, time) = v
            things_type_key = self.full_path_key_map.get(name, None)
            if things_type_key:
                type = things_type_key["type"]
                if type == "string":
                    pass
                elif type == "bit":
                    pass
                elif type == "short":
                    pass
                elif type == "int":
                    pass
                elif type == "long":
                    pass
                elif type == "double":
                    pass
                elif type == "float":
                    pass
                self.result_dict[things_type_key["uploadType"]].append({things_type_key["key"]: val})
        return self.result_dict

