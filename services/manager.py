import modules.load_service_info as load_service_info
import utils.runtime as runtime
from pathlib import Path

SERVICES = runtime.get_safe_path("services/")

def get_service(service_id):
    path = Path(SERVICES + service_id)
    if path.exists():
        path = Path(str(path) + "/" + "service.info.json")
        try:
            service_info = load_service_info.load_info(str(path))
            return service_info
        except FileNotFoundError:
            return "Not found 'service.info.json'"
    return "Unvaliable"

def get_all_services():
    path = Path(SERVICES)
    services = []
    for file in path.iterdir():
        if file.is_dir():
            service_id = str(file).replace(SERVICES, "")
            service_info = get_service(service_id)
            if type(service_info) is load_service_info.ServiceInfo:
                services.append(service_info)
    return services
        