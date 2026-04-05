import subprocess
import sys, os, re
import keyboard, time
import pyautogui

SERVICIOS = [
    "ZeroTierOneService",
    "client32",
    "PCIGateway",
    "AnyDesk",
    "OpenVPNService",
    "OpenVPNServiceInteractive"
]

procesos = []
ProcesosActivos = []

def limpiar():
    subprocess.run("cls", shell=True)
    sys.stdout.write("\r \r")
    sys.stdout.flush()

# def limpiar_terminal4():
#     if sys.platform == "win32":  # Si estamos en Windows
#         os.system("cls")
#     else:  # Si estamos en macOS o Linux
#         os.system("clear")

# def limpiar_terminal():
#     print("\033[2J\033[H", end="")

# def limpiar_terminal2():
#     cmd = "cls" if sys.platform == "win32" else "clear"
#     subprocess.run(cmd, shell=True)

# def limpiar_terminal3():
#     if sys.platform == "win32":
#         subprocess.run("cls", shell=True)
#     else:
#         subprocess.run("clear")

# def borra_linea():
#     print("\033[F\033[K", end="")
    
# def borrar_lineas(n):
#     for _ in range(n):
#         print("\033[F\033[K", end="")

# def elimina():
#     #time.sleep(3)
#     #keyboard.send("shift+alt+l")
#     keyboard.send("shift+alt+l", do_press=True, do_release=True)

# def ejecutar(cmd):
#    return subprocess.run(cmd, capture_output=True, text=True).stdout

def ejecutar(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="cp1252",
            errors="ignore"
        )
        return result.stdout or ""
    except Exception as e:
        print(f"Error ejecutando {cmd}: {e}")
        return ""


def obtener_pid(servicio):
    salida = ejecutar(["sc", "queryex", servicio])
    for linea in salida.splitlines():
        if "PID" in linea:
            return linea.split(":")[1].strip()
    return "0"


def obtener_estado(servicio):
    salida = ejecutar(["sc", "query", servicio])
    for linea in salida.splitlines():
        # print(linea)
        if "ESTADO" in linea:
            if "RUNNING" in linea:
                return "EN EJECUCIÓN"
            elif "STOPPED" in linea:
                return "DETENIDO"
    return "DESCONOCIDO"


def obtener_proceso(pid):
    if pid == "0":
        return None

    salida = ejecutar(["tasklist", "/FI", f"PID eq {pid}"])
    lineas = salida.splitlines()

    if len(lineas) > 3:
        return lineas[3].split()[0]

    return None

# def obtener_exe_servicio2(servicio):
#     todos_proccesos = set()
#     salida = ejecutar(["sc", "qc", servicio])

#     for linea in salida.splitlines():
#         if "NOMBRE_RUTA_BINARIO" in linea:
#             ruta = linea.split(":", 1)[1].strip()
#             match = re.search(r'([^\\]+\.exe)', ruta, re.IGNORECASE)
#             if match:
#                 #print(match.group(1))
#                 todos_proccesos.add(match.group(1))
#                 print(list(todos_proccesos))
#                 #return match.group(1)
#             #print(ruta)
#             #todos_proccesos.add(ruta.split("\\")[-1])
#             #print(list(todos_proccesos))
#             #time.sleep(1)
#             #return ruta.split("\\")[-1]  # solo el .exe
#     return list(todos_proccesos), menu_post()

#     #return None

def obtener_exe_servicio(servicio):
    salida = ejecutar(["sc", "qc", servicio])

    if not salida:
        return []

    resultados = set()

    for linea in salida.splitlines():
        if "NOMBRE_RUTA_BINARIO" in linea:
            ruta = linea.split(":", 1)[1].strip()

            matches = re.findall(r'([^\\]+\.exe)', ruta, re.IGNORECASE)
            for m in matches:
                resultados.add(m)

    return list(resultados)

# def obtener_procesos_desde_servicios2(servicios):
#     todos_procesos = set()

#     for s in servicios:
#         exe = obtener_exe_servicio(s)
#         print(exe)

#         if not exe:
#             continue

#         #exe = exe.lower()

#         # ignorar procesos genéricos de Windows
#         if exe == "svchost.exe":
#             continue

#         relacionados = buscar_relacionados(exe)

#         for p in relacionados:
#             todos_procesos.add(p)

#     return sorted(todos_procesos)

def obtener_procesos_desde_servicios(servicios):
    todos_procesos = set()
    print("==============================")
    print("PROCESOS")
    print("==============================")

    for s in servicios:
        exes = obtener_exe_servicio(s)
        print(f"Proceso: {exes}")

        if not exes:
            continue

        # 👇 manejar lista
        if isinstance(exes, str):
            exes = [exes]

        for exe in exes:
            exe = exe.lower()

            if exe == "svchost.exe":
                continue

            relacionados = buscar_relacionados(exe)

            for p in relacionados:
                todos_procesos.add(p.lower())

    return sorted(todos_procesos), menu_post()

def buscar_relacionados(nombre):
    prefijo = nombre[:5].lower()
    salida = ejecutar(["tasklist"])

    procesos = set()

    for linea in salida.splitlines():
        if prefijo in linea.lower():
            procesos.add(linea.split()[0])

    return list(procesos)


# def mostrar_servicios2():
#     todos_procesos = set()

#     print("==============================")
#     print(" ESTADO DE SERVICIOS")
#     print("==============================")

#     for s in SERVICIOS:
#         estado = obtener_estado(s)
#         pid = obtener_pid(s)
#         proceso = obtener_proceso(pid)
#         print(s)

#         print(f"Servicio: {s}")
#         print(f"Estado: {estado}")
#         print(f"PID: {pid}")

#         if proceso:
#             print(f"Proceso: {proceso}")
#             relacionados = buscar_relacionados(proceso)

#             for p in relacionados:
#                 print(f"  -> {p}")
#                 todos_procesos.add(p)

#         print("-" * 30)

#     return list(todos_procesos), menu_post()

def mostrar_servicios():
    todos_procesos = set()

    print("==============================")
    print(" ESTADO DE SERVICIOS")
    print("==============================")

    for s in SERVICIOS:
        estado = obtener_estado(s)
        pid = obtener_pid(s)
        proceso = obtener_proceso(pid)

        print(f"Servicio: {s}")
        print(f"Estado: {estado}")
        print(f"PID: {pid}")

        if proceso:
            print(f"Proceso: {proceso}")
            relacionados = buscar_relacionados(proceso)

            for p in relacionados:
                print(f"  -> {p}")
                todos_procesos.add(p)

        print("-" * 30)

    # 👇 NUEVO BLOQUE
    print("==============================")
    print(" PROCESOS DETECTADOS")
    print("==============================")

    for p in todos_procesos:
        print(f"- {p}")

    return list(todos_procesos), menu_post()

# def mostrar_procesos(lista):
#     print("==============================")
#     print(" LISTA DE PROCESOS")
#     print("==============================")

#     if not lista:
#         print("No hay procesos cargados")
#     else:
#         for p in lista:
#             print(f"- {p}")

#     return menu_post()

# def detener_procesos2(lista):
#     for p in lista:
#         print(f"Deteniendo {p}...")
#         subprocess.run(["taskkill", "/F", "/IM", p],
#                        #stdout=subprocess.DEVNULL,
#                        stderr=subprocess.DEVNULL)
        
def detener_procesos(lista):
    #print(lista)
    # import subprocess

    for p in lista:
        print(f"Deteniendo {p}...", end=" ")

        result = subprocess.run(
            ["taskkill", "/F", "/IM", p],
            # stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print("[✔]")
        else:
            print("[✖]")

    #input("\nPresioná ENTER para continuar...")
    return menu_post()
        
# def servicio_accion2(servicios, accion):
#     for s in servicios:
#         print(s)
#         try:
#             if accion == "restart":
#                 subprocess.run(["net", "stop", s],
#                                stdout=subprocess.DEVNULL,
#                                stderr=subprocess.DEVNULL)
#                 result = subprocess.run(["net", "start", s],
#                                         stdout=subprocess.DEVNULL,
#                                         stderr=subprocess.DEVNULL)
#             else:
#                 cmd = ["net", "start" if accion == "start" else "net", "stop", s]
#                 result = subprocess.run(
#                     ["net", accion, s],
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL
#                 )

#             if result.returncode == 0:
#                 print(f"[✔] {s} OK")
#             else:
#                 print(f"[✖] {s} ERROR")

#         except Exception as e:
#             print(f"[!] {s} -> {e}")

def servicio_accion(servicios, accion):
    for s in servicios:
        print(s)
        try:
            if accion == "restart":
                subprocess.run(["net", "stop", s],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                result = subprocess.run(["net", "start", s],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
            else:
                result = subprocess.run(
                    ["net", accion, s],
                    #stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            if result.returncode == 0:
                print(f"[✔] {s} OK")
            else:
                print(f"[✖] {s} ERROR")

        except Exception as e:
            print(f"[!] {s} -> {e}")

    # 👇 MENÚ FINAL
    return menu_post()

def menu_post():
    while True:
        print("======================")
        print("1 - Volver al menú principal")
        print("2 - Limpiar pantalla")
        print("3 - Salir")
        print("======================")

        opcion = input("Opción: ")

        if opcion == "1":
            limpiar()
            return "menu"

        elif opcion == "2":
            limpiar()

        elif opcion == "3":
            limpiar()
            return "salir"

def menu():
    while True:
        global procesos, ProcesosActivos
        #muestra()
        # procesos = mostrar_servicios()

        print("==============================")
        print("             MENÚ             ")
        print("==============================")
        #print("MENU")
        print("0 - Mostrar Servicios")
        print("00 - Mostrar Procesos")
        print("1 - Iniciar Servicios")
        print("2 - Detener Servicios")
        print("3 - Reiniciar Servicios")
        print("4 - Detener procesos")
        print("5 - Limpiar")
        print(f"6 - Salir", flush=True)

        opcion = input("Opción: ")
        limpiar()

        if opcion == "0":
            limpiar()
            procesos, resultado = mostrar_servicios()
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
        elif opcion == "00":
            limpiar()
            #resultado = mostrar_procesos(procesos)
            #resultado = obtener_exe_servicio(procesos)
            ProcesosActivos, resultado = obtener_procesos_desde_servicios(SERVICIOS)
            # for p in ProcesosActivos:
            #     print(f"- {p}")
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
        elif opcion == "1":
            limpiar()
            resultado = servicio_accion(SERVICIOS, "start")
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
            #print(procesos)
        elif opcion == "2":
            limpiar()
            #servicio_accion(SERVICIOS, "stop")
            resultado = servicio_accion(SERVICIOS, "stop")
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
        elif opcion == "3":
            limpiar()
            resultado = servicio_accion(SERVICIOS, "restart")
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
        elif opcion == "4":
            limpiar()
            #print(ProcesosActivos)
            resultado = detener_procesos(ProcesosActivos)
            if resultado == "menu":
                continue
            elif resultado == "salir":
                break
        elif opcion == "5":
            limpiar()
        elif opcion == "6":
            limpiar()
            break

if __name__ == "__main__":
    menu()