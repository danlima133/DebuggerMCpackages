import modules.json_config as json_config

class ServiceInfo:
    def __init__(self, name, version, description, service_id):
        self.name = name
        self.version = version
        self.description = description
        self.service_id = service_id
    
    def get_version(self):
        return f"v{self.version[0]}.{self.version[1]}.{self.version[2]}"
    
    def service_is(self, service_id):
        return self.service_id == service_id
    
    def __str__(self):
        return f"{self.name}, {self.get_version()}, {self.description}"

def load_info(path):
    try:
        service_config = json_config.JsonConfig(path)
        _names = path.split("/")
        service_id = _names[len(_names) - 2]
        service_name = service_config.get_attr("name")
        service_version = service_config.get_attr("version")
        service_description = service_config.get_attr("description")
        return ServiceInfo(service_name, service_version, service_description, service_id)
    except FileNotFoundError as err:
        raise FileNotFoundError(path)