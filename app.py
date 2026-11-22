"""Panel de Control Local.
"""

from __future__ import annotations

import re
import sqlite3
import os
import subprocess
import time
from datetime import datetime
from typing import Any
from uuid import uuid4

import psutil
from dbus_next.aio import MessageBus
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Configurar psutil para leer métricas reales del host
if os.path.exists("/host/proc"):
    psutil.PROCFS_PATH = "/host/proc"

app = FastAPI(title="Panel de Control Local", version="1.0.0")

# DB Setup
def get_db():
    conn = sqlite3.connect("/app/data/tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT)")
    return conn

STATS_INTERVAL = 3.0
_cached_stats: dict[str, float] = {}
_last_stats_time = 0.0

def _get_real_stats() -> dict[str, float]:
    global _cached_stats, _last_stats_time
    ahora = time.monotonic()
    if ahora - _last_stats_time < STATS_INTERVAL:
        return _cached_stats
    
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    
    _cached_stats = {"cpu": cpu, "ram": mem}
    _last_stats_time = ahora
    return _cached_stats

@app.get("/api/status")
def get_status() -> dict[str, Any]:
    hora = datetime.now()
    stats = _get_real_stats()
    return {
        "hora": hora.strftime("%H:%M:%S"),
        "fecha": hora.strftime("%Y-%m-%d"),
        "saludo": "¡Hola!",
        "cpu": stats["cpu"],
        "ram": stats["ram"],
    }

async def _list_systemd_services() -> list[str]:
    try:
        bus = await MessageBus(bus_address='unix:path=/run/dbus/system_bus_socket').connect()
        introspection = await bus.introspect("org.freedesktop.systemd1", "/org/freedesktop/systemd1")
        obj = bus.get_proxy_object("org.freedesktop.systemd1", "/org/freedesktop/systemd1", introspection)
        manager = obj.get_interface("org.freedesktop.systemd1.Manager")
        units = await manager.call_list_units()
        services = [unit[0] for unit in units if unit[3] == 'active' and unit[0].endswith('.service')]
        return services
    except Exception as e:
        return [f"Error: {e}"]

@app.get("/api/services")
async def get_services() -> dict[str, Any]:
    svcs = await _list_systemd_services()
    return {
        "services": svcs,
        "total": len(svcs),
        "fuente": "systemd-dbus"
    }

# Valida el nombre de la unidad antes de pasarlo a journalctl (evita inyección de argumentos)
SERVICE_NAME_RE = re.compile(r"^[a-zA-Z0-9_@.-]+\.service$")
JOURNAL_LINES = 30

@app.get("/api/services/{service_name}/logs")
def get_service_logs(service_name: str) -> JSONResponse:
    if not SERVICE_NAME_RE.match(service_name):
        return JSONResponse(
            status_code=400,
            content={
                "service": service_name,
                "logs": [],
                "error": (
                    "Nombre de servicio no válido: debe empezar por letras, dígitos o "
                    "_ @ . - y terminar en '.service'."
                ),
            },
        )

    try:
        proc = subprocess.run(
            ["journalctl", "-u", service_name, "-n", str(JOURNAL_LINES), "--no-pager"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=15,
        )
    except FileNotFoundError:
        return JSONResponse(
            status_code=501,
            content={
                "service": service_name,
                "logs": [],
                "error": "journalctl no está disponible en esta imagen. Instala 'systemd'.",
            },
        )
    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=504,
            content={
                "service": service_name,
                "logs": [],
                "error": f"journalctl tardó demasiado al leer los logs de {service_name}.",
            },
        )
    except OSError as e:
        return JSONResponse(
            status_code=500,
            content={
                "service": service_name,
                "logs": [],
                "error": f"No se pudo ejecutar journalctl: {e}",
            },
        )

    if proc.returncode != 0:
        detalle = (proc.stderr or proc.stdout or "").strip()
        bajo_permisos = any(
            marca in detalle.lower()
            for marca in ("permission denied", "access denied", "no journal files", "failed to open")
        )
        mensaje = (
            f"No hay permisos para leer los logs de '{service_name}'. "
            "Comprueba los volúmenes del journal y los privilegios del contenedor"
        )
        if not bajo_permisos:
            mensaje = f"No se pudieron leer los logs de '{service_name}'."
        if detalle:
            mensaje = f"{mensaje}. Detalle: {detalle.splitlines()[-1]}"
        return JSONResponse(
            status_code=403 if bajo_permisos else 500,
            content={"service": service_name, "logs": [], "error": mensaje},
        )

    lineas = proc.stdout.splitlines()
    return JSONResponse(
        content={
            "service": service_name,
            "logs": lineas,
            "total": len(lineas),
            "fuente": "journalctl",
        }
    )

@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    import pathlib
    return HTMLResponse(pathlib.Path("index.html").read_text(encoding="utf-8"))
