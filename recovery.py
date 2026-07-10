import subprocess
import datetime
import sys
import time


def registrar(mensaje, nivel="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{nivel}] {mensaje}")


def verificar_servicio(host, puerto):
    resultado = subprocess.run(
        ["nc", "-zv", host, str(puerto)],
        capture_output=True, text=True, timeout=5
    )
    return resultado.returncode == 0


def verificar_bd(host="servidor-bd", puerto=5432):
    registrar("Comprobando disponibilidad de la base de datos...")
    if verificar_servicio(host, puerto):
        registrar(f"Base de datos disponible en {host}:{puerto}")
        return True
    else:
        registrar(f"Base de datos NO disponible en {host}:{puerto}", "ERROR")
        return False


def reiniciar_erp(host="servidor-erp", puerto=8080):
    registrar("Intentando reinicio del servicio ERP...")
    resultado = subprocess.run(
        ["ssh", host, "sudo systemctl restart erp.service"],
        capture_output=True, text=True, timeout=30
    )
    if resultado.returncode == 0:
        registrar("Servicio ERP reiniciado correctamente")
        return True
    else:
        registrar(f"Error al reiniciar ERP: {resultado.stderr}", "ERROR")
        return False


def verificar_erp(host="servidor-erp", puerto=8080):
    registrar("Verificando disponibilidad del sistema ERP...")
    if verificar_servicio(host, puerto):
        registrar(f"Sistema ERP disponible en {host}:{puerto}")
        return True
    else:
        registrar(f"Sistema ERP NO disponible en {host}:{puerto}", "ERROR")
        return False


def procedimiento_recuperacion_erp():
    registrar("=== INICIO PROCEDIMIENTO DE RECUPERACIÓN ERP ===")
    inicio = datetime.datetime.now()

    if not verificar_bd():
        registrar(
            "CRÍTICO: Base de datos no disponible. "
            "Activar procedimiento de recuperación de BD antes de continuar.",
            "CRÍTICO"
        )
        sys.exit(1)

    if not verificar_erp():
        registrar("ERP no responde. Iniciando proceso de reinicio...")
        if reiniciar_erp():
            time.sleep(30)
            if verificar_erp():
                registrar("Recuperación completada mediante reinicio de servicio")
            else:
                registrar(
                    "El reinicio no ha restaurado el servicio. "
                    "Activar recuperación desde snapshot o backup.",
                    "ADVERTENCIA"
                )
        else:
            registrar(
                "No es posible reiniciar el servicio remotamente. "
                "Intervención manual requerida.",
                "CRÍTICO"
            )
    else:
        registrar("Sistema ERP operativo. No se requiere intervención.")

    fin = datetime.datetime.now()
    duracion = (fin - inicio).seconds
    registrar(f"=== FIN DEL PROCEDIMIENTO. Duración: {duracion} segundos ===")


if __name__ == "__main__":
    procedimiento_recuperacion_erp()
