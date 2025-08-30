# 📍 coords2gmaps.py

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

```
 ██████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗██████╗  ██████╗ ███╗   ███╗ █████╗ ██████╗ ███████╗   ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝╚════██╗██╔════╝ ████╗ ████║██╔══██╗██╔══██╗██╔════╝   ██╔══██╗╚██╗ ██╔╝
██║     ██║   ██║██║   ██║██████╔╝██║  ██║███████╗ █████╔╝██║  ███╗██╔████╔██║███████║██████╔╝███████╗   ██████╔╝ ╚████╔╝ 
██║     ██║   ██║██║   ██║██╔══██╗██║  ██║╚════██║██╔═══╝ ██║   ██║██║╚██╔╝██║██╔══██║██╔═══╝ ╚════██║   ██╔═══╝   ╚██╔╝  
╚██████╗╚██████╔╝╚██████╔╝██║  ██║██████╔╝███████║███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██║     ███████║██╗██║        ██║   
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝╚═╝        ╚═╝   
                                                                                                                          
```

Una herramienta CLI para convertir coordenadas en múltiples formatos a enlaces directos de mapas. Ideal para profesionales de ciberseguridad, investigadores OSINT y analistas.

## 🌟 Características Destacadas

- 🎯 **Soporte multi-formato**: Decimal, DMS, y extracción automática desde texto
- 📁 **Procesamiento por lotes**: Maneja archivos CSV, TXT y logs
- 🗺️ **Multiplataforma**: Google Maps y OpenStreetMap
- 🌐 **Integración directa**: Abre enlaces automáticamente en tu navegador
- 💾 **Exportación flexible**: Guarda resultados en archivos de texto

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/rodrigo47363/coords2gmaps.git
cd coords2gmaps

# Hacer ejecutable el script
chmod +x coords2gmaps.py

# Instalar globalmente (opcional)
sudo ln -s $(pwd)/coords2gmaps.py /usr/local/bin/coords2gmaps
```

## 💡 Uso Avanzado

### Conversión Básica
```bash
# Coordenadas decimales
coords2gmaps.py 25.4099998474 -101.019996643

# Formato DMS
coords2gmaps.py "25°24'36.0\"N" "101°1'12.0\"W"
```

### Extracción desde Texto
```bash
# Desde archivo
coords2gmaps.py --extract < informe.txt

# Desde output de otros comandos
nmap -sP 192.168.1.0/24 | coords2gmaps.py --extract
```

### Procesamiento por Lotes
```bash
# Archivo CSV con separador personalizado
coords2gmaps.py --file coordenadas.csv --sep ";"

# Exportar resultados
coords2gmaps.py --file datos.txt --output resultados.txt
```

### Integración con Navegador
```bash
# Abrir automáticamente en navegador
coords2gmaps.py 25.41 -101.02 --open

# Generar enlaces para ambos servicios
coords2gmaps.py 25.41 -101.02 --osm --open
```

## 🛠️ Opciones Completas

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `POSITIONAL` | Coordenadas directas | `25.41 -101.02` |
| `-f, --file` | Archivo de entrada | `--file datos.csv` |
| `-s, --sep` | Separador personalizado | `--sep ";"` |
| `-e, --extract` | Modo extracción | `--extract` |
| `-o, --open` | Abrir en navegador | `--open` |
| `--osm` | Incluir OpenStreetMap | `--osm` |
| `--output` | Archivo de salida | `--output urls.txt` |
| `-v, --verbose` | Modo verbose | `-v` |

## 📊 Ejemplos Prácticos

### Caso 1: Análisis Forense
```bash
# Extraer coordenadas de logs y generar mapa
cat access.log | grep "location" | coords2gmaps.py --extract --output suspicious_locations.txt
```

### Caso 2: Investigación OSINT
```bash
# Procesar lista de coordenadas y abrir en navegador
coords2gmaps.py --file coordinates_list.txt --open --osm
```

### Caso 3: Automatización con Scripts
```bash
#!/bin/bash
# Script para monitoreo continuo
tail -f gps_data.stream | while read line; do
    echo "$line" | coords2gmaps.py --extract --open
done
```

## 🗺️ Roadmap

- [ ] **Exportación GeoJSON** - Para integración con herramientas SIG
- [ ] **Soporte GPX/NMEA** - Importación desde dispositivos GPS
- [ ] **API REST** - Versión servidor para integraciones
- [ ] **Interfaz Web** - Versión navegador con mapa interactivo
- [ ] **Plugin Wireshark** - Extracción directa desde paquetes

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request



Aquí tienes la sección **corregida y pulida** para que se vea totalmente profesional en tu README. Le di coherencia en estilo, mejoré el copywriting, añadí llamadas a la acción y corregí pequeños detalles (como el correo).

---

## 👨‍💻 Author

**Rodrigo**

[![GitHub](https://img.shields.io/badge/GitHub-rodrigo47363-181717?style=flat\&logo=github)](https://github.com/rodrigo47363)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rodrigo_V-0A66C2?style=flat\&logo=linkedin)](https://www.linkedin.com/in/rodrigo-v-695728215/)
[![Twitter](https://img.shields.io/badge/Twitter-@rodrigo47363-1DA1F2?style=flat\&logo=twitter)](https://twitter.com/rodrigo47363)
[![Email](https://img.shields.io/badge/Email-rodrigovil@proton.me-D14836?style=flat\&logo=protonmail)](mailto:rodrigovil@proton.me)

---

### 🛠️ Areas of Expertise

* 🔐 Ethical Hacking & Professional Pentesting
* 🕵️ OSINT & Geolocation Analysis
* 🤖 Automation & CLI Tools Development
* 🐧 Linux Systems & Open Source Advocacy

---

### 📂 Contributions & Projects

* Security Research & Vulnerability Assessment
* Open Source Tool Development
* Technical Writing & Knowledge Sharing
* Community Mentorship

---

💡 **Need assistance with a project or want to collaborate?**
Reach out through any of the platforms above, or open an issue in this repository for technical discussions.

⭐ **If you find this project useful, don’t forget to give it a star on GitHub!**

---

*Professional connections and collaboration opportunities are always welcome.*

---
