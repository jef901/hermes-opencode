# Panel de Control Local

App web de control de sistemas con métricas en tiempo real.

## Arquitectura
- **Estado del Sistema**: Utiliza `psutil` configurado con `/host/proc` para leer métricas reales de CPU y RAM desde el anfitrión.
- **Servicios**: Consulta servicios activos (`.service`) de `systemd` mediante el socket D-Bus del anfitrión (`/run/dbus/system_bus_socket`).
- **Persistencia**: Las tareas se guardan en una base de datos SQLite en `./data/tasks.db` utilizando volúmenes Docker.

## Despliegue
```bash
docker compose up -d --build
# Abrir http://localhost:8080
```
