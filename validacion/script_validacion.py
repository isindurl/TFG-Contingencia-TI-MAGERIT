import subprocess
import datetime
import sys


def registrar(mensaje, nivel="INFO"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{nivel}] {mensaje}")


def verificar_servicio(host, puerto):
    resultado = subprocess.run(
        ["nc", "-zv", host, str(puerto)],
        capture_output=True, text=True, timeout=5
    )
    return resultado.returncode == 0


def verificar_bd(host="localhost", puerto=5432):
    registrar("Verificando disponibilidad de la base de datos...")
    if verificar_servicio(host, puerto):
        registrar(f"Base de datos disponible en {host}:{puerto}")
        return True
    registrar(f"Base de datos NO disponible en {host}:{puerto}", "ERROR")
    return False


def verificar_erp(host="localhost", puerto=8080):
    registrar("Verificando disponibilidad del sistema ERP...")
    if verificar_servicio(host, puerto):
        registrar(f"Sistema ERP disponible en {host}:{puerto}")
        return True
    registrar(f"Sistema ERP NO disponible en {host}:{puerto}", "ERROR")
    return False


def procedimiento_recuperacion():
    registrar("=" * 55)
    registrar("INICIO DEL PROCEDIMIENTO DE VALIDACIÓN")
    registrar("Escenario: caída del servidor de virtualización")
    registrar("=" * 55)
    inicio = datetime.datetime.now()

    servicios = [
        ("Red corporativa",    "localhost", 80),
        ("Base de datos",      "localhost", 5432),
        ("Sistema ERP",        "localhost", 8080),
        ("Servidor archivos",  "localhost", 445),
    ]

    resultados = []
    for nombre, host, puerto in servicios:
        registrar(f"Verificando: {nombre}...")
        disponible = verificar_servicio(host, puerto)
        estado = "DISPONIBLE" if disponible else "NO DISPONIBLE"
        registrar(f"{nombre}: {estado}",
                  "INFO" if disponible else "ERROR")
        resultados.append((nombre, disponible))

    fin = datetime.datetime.now()
    duracion = (fin - inicio).seconds

    registrar("=" * 55)
    registrar("RESUMEN DE VALIDACIÓN")
    registrar("=" * 55)
    for nombre, ok in resultados:
        simbolo = "OK" if ok else "FALLO"
        registrar(f"  [{simbolo}] {nombre}")

    registrar(f"Duración total: {duracion} segundos")
    registrar("FIN DEL PROCEDIMIENTO DE VALIDACIÓN")

    fallos = sum(1 for _, ok in resultados if not ok)
    sys.exit(fallos)


if __name__ == "__main__":
    procedimiento_recuperacion()
