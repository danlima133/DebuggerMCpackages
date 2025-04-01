import services.platformtools.service as platformtools
import rich.console as console
import services.manager as manager
import os

console_obj = console.Console()

console_obj.rule("Anvaliable Services")

services = manager.get_all_services()

for service in services:
    console_obj.log(str(service))
