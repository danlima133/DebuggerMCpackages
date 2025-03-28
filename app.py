# import os
# import adb.tools.adbserch as adbserch

# from modules.app_config import get_prop
# import utils.runtime as runtime

# if adbserch.has_platform_tools():
#     print("Platform tools já instalado")
#     os.system(f"{get_prop(adbserch.SECTION, adbserch.KEY_PATH)}/adb version")
# else:
#     print("Platform tools não instalado, desja instalar agora?")
#     res = input("Sim/Não: ")
#     if res.lower() == "s" or "sim":
#         adbserch.get_platform_tools()
#         print("Platform tools instalado com exito")
#     elif res.lower() == "n" or "nao" or "não":
#         print("Platform tools não instalado")

import services.platformtools.service as platformtools
import modules.load_service_info as service_info
import rich.console as console
import services.manager as manager
import utils.runtime as runtime
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
