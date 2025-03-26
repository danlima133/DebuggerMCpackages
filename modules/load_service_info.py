import modules.json_config as json_config

class ServiceInfo:
    def __init__(self, name, version, description):
        self.name = name
        self.version = version
        self.description = description
    
    def get_version(self):
        return f"v{self.version[0]}.{self.version[1]}.{self.version[2]}"

def load_info(path):
    try:
        service_config = json_config.JsonConfig(path)
        service_name = service_config.get_attr("name")
        service_version = service_config.get_attr("version")
        service_description = service_config.get_attr("description")
        return ServiceInfo(service_name, service_version, service_description)
    except FileNotFoundError as err:
        print(f"Arquivo not found: '{err.filename}'")