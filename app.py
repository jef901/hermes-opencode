"""Panel de Control Local.
"""

from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Any
from uuid import uuid4

import psutil
from dbus_next.aio import MessageBus
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Configurar psutil para leer métricas reales del host
if os.path.exists("/host/proc"):
    psutil.PROCFS_PATH = "/host/proc"

app = FastAPI(title="Panel de Control Local", version="1.0.0")

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

@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    import pathlib
    return HTMLResponse(pathlib.Path("index.html").read_text(encoding="utf-8"))
