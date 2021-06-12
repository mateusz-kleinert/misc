import xml.etree.ElementTree as ET


class Config:
    def __init__(self, port, version):
        self.version = version
        self.port = port

    @staticmethod
    def from_string(text):
        root = ET.fromstring(text)
        config = {element.tag: element.text for element in root.getchildren()}
        return Config(**config)


with open("config.xml", "r") as f:
    config = Config.from_string(f.read())
    print("Port: %s\nVersion: %s" % (config.port, config.version))
