from wthings_gateway.connectors.converter import Converter, log


class PlcUplinkConverter(Converter):
    def __init__(self, config):
        self.__config = config
        self.result_dict = {
            'deviceName': config.get('deviceName', 'plcDevice'),
            'deviceType': config.get('deviceType', 'default'),
            'attributes': [],
            'telemetry': []
        }

    def convert(self, config, data):
        # keys = ['attributes', 'timeseries']
        information_types = {"attributes": "attributes", "timeseries": "telemetry"}
        for key in information_types:
            self.result_dict[information_types[key]] = []
            if self.__config.get(key) is not None:
                for config_object in self.__config.get(key):
                    value_key = config_object['key']
                    value = data[key].get(value_key, None)
                    if value != None:
                        self.result_dict[information_types[key]].append({value_key: value})
        return self.result_dict

if __name__ == '__main__':
    pass