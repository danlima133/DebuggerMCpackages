import services.platformtools.service as platformtools
import rich.console as console
import services.manager as manager
import os

console_obj = console.Console()

console_obj.rule("Anvaliable Services")

services = manager.get_all_services()

for service in services:
    console_obj.log(str(service))

s_platformtools = manager.get_service("platformtools")

console_obj.rule(f"Run [green]{s_platformtools.name}[/green] - {s_platformtools.get_version()}")

if not platformtools.has_platform_tools():
    console_obj.log("Vamos instalar o platformtools para voce")
    platformtools.get_platform_tools()
else:
    console_obj.log("[red]Já instalado!")
    os.system("platform-tools/adb version")
