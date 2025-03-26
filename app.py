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
import os
import utils.runtime as runtime

console_obj = console.Console()

console_obj.rule("Anvaliable Services")

pathservice = ""

if runtime.run_as_build():
    pathservice = os.path.join(runtime.INTERNAL, "infos", "service.info.json")
else:
    pathservice = "./services/platformtools/service.info.json"

info = service_info.load_info(pathservice)

console_obj.log("Service name: " + info.name)
console_obj.log("Service description: " + info.description)
console_obj.log("Service Version: " + info.get_version())

console_obj.rule("Verify Service")

if not platformtools.has_platform_tools():
    platformtools.get_platform_tools()
else:
    console_obj.log("[red]Já instalado!")
    os.system("platform-tools/adb version")
