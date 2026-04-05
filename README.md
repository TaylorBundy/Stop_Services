# 🖥️ Administrador de Servicios y Procesos (Windows)

Herramienta desarrollada en **Python** para la gestión avanzada de servicios y procesos en sistemas Windows.

Permite visualizar el estado de servicios, identificar sus procesos asociados (incluso cuando están detenidos) y ejecutar acciones como iniciar, detener o reiniciar servicios, así como finalizar procesos relacionados.

---

## 🚀 Funcionalidades

- 🔍 Consulta del estado de servicios
- 🧠 Detección automática del ejecutable (`.exe`) de cada servicio
- 🔗 Búsqueda de procesos relacionados
- ⚙️ Gestión de servicios:
  - Iniciar
  - Detener
  - Reiniciar
- 💀 Finalización de procesos
- 📋 Lista de procesos sin duplicados
- 🖥️ Menú interactivo en consola
- 🧹 Limpieza de terminal
- 🎯 Submenús después de cada acción

---

## 🛠️ Tecnologías

- Python 3
- subprocess
- re (regex)
- Comandos de Windows:
  - sc
  - tasklist
  - taskkill
  - net start / stop

---

## ⚠️ Requisitos

- Windows
- Python 3.10+
- Ejecutar como Administrador

---

## ▶️ Uso

```bash
python app.py
```

---

## 📷 Ejemplo

```
==============================
 ESTADO DE SERVICIOS
==============================

Servicio: OpenVPNService
Estado: EN EJECUCIÓN
PID: 1234
Proceso: openvpn.exe

MENU
1 - Mostrar procesos
2 - Detener procesos
3 - Salir
```

---

## 🔮 Futuras mejoras

- Interfaz gráfica (GUI)
- Exportación de logs
- Monitor en tiempo real
- Filtros avanzados

---

## 👨‍💻 Autor

Taylor Bundy
