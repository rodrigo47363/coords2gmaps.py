#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coords2gmaps.py — Convierte coordenadas a enlaces de Google Maps.
Soporta: grados decimales, DMS (° ' "), N/S/E/W, texto crudo, archivos CSV.
Uso básico:
  python coords2gmaps.py 25.40999984741211 -101.0199966430664
  python coords2gmaps.py "25°24'36\"N" "101°01'12\"W"
  echo "Latitude: 25.4099998474\nLongitude: -101.019996643" | python coords2gmaps.py --extract
  python coords2gmaps.py --file apuntos.csv --sep "," --open
"""

import argparse, re, sys, webbrowser
from typing import Optional, Tuple, Iterable, List

# ---------------------------
# Parsing de coordenadas
# ---------------------------

DMS_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<deg>-?\d+(?:\.\d+)?)      # grados
    (?:\D+(?P<min>\d+(?:\.\d+)?))? # minutos opcionales
    (?:\D+(?P<sec>\d+(?:\.\d+)?))? # segundos opcionales
    \s*(?P<hem>[NSEW])?            # hemisferio opcional
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE
)

# Busca "Latitude: X" / "Longitude: Y" o pares sueltos "X, Y"
LAT_LABELS = r"(lat|latitude|latitud)"
LON_LABELS = r"(lon|long|longitud|longitude)"

LabeledCoord = re.compile(
    rf"(?P<label>{LAT_LABELS}|{LON_LABELS})\s*[:=]\s*(?P<val>[-+]?\d+(?:\.\d+)?)",
    re.IGNORECASE
)

PairFloat = re.compile(
    r"(?P<lat>[-+]?\d+(?:\.\d+)?)\s*[,;\s]\s*(?P<lon>[-+]?\d+(?:\.\d+)?)"
)

def dms_to_decimal(deg: float, minutes: float = 0.0, seconds: float = 0.0, hemi: Optional[str] = None) -> float:
    val = abs(deg) + (minutes or 0)/60.0 + (seconds or 0)/3600.0
    if deg < 0:
        val = -val
    if hemi:
        hemi = hemi.upper()
        if hemi in ("S", "W"):
            val = -abs(val)
        elif hemi in ("N", "E"):
            val = abs(val)
    return val

def parse_single_coord(token: str) -> Optional[float]:
    """
    Intenta parsear un único valor de coordenada (decimal o DMS).
    """
    s = token.strip().replace(",", ".")  # por si viene con coma decimal
    # 1) Intento decimal puro
    try:
        return float(s)
    except ValueError:
        pass
    # 2) Intento DMS (permite símbolos o espacios como separadores)
    m = DMS_PATTERN.match(s.replace("°", " ").replace("'", " ").replace("’", " ").replace('"', " "))
    if m:
        deg = float(m.group("deg"))
        minutes = float(m.group("min")) if m.group("min") else 0.0
        seconds = float(m.group("sec")) if m.group("sec") else 0.0
        hemi = m.group("hem")
        return dms_to_decimal(deg, minutes, seconds, hemi)
    return None

def parse_coord_pair(a: str, b: str) -> Optional[Tuple[float, float]]:
    lat = parse_single_coord(a)
    lon = parse_single_coord(b)
    if lat is None or lon is None:
        return None
    # Saneamiento rápido de rangos
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return None
    return (lat, lon)

def extract_from_text(text: str) -> List[Tuple[float, float]]:
    """
    Extrae coordenadas de texto libre.
    Prioriza claves Lat/Long; si no, intenta pares flotantes.
    """
    results = []

    # 1) Buscar etiquetas específicas
    labeled = list(LabeledCoord.finditer(text))
    if labeled:
        lat_val = None
        lon_val = None
        for m in labeled:
            label = m.group("label").lower()
            val = float(m.group("val"))
            if re.fullmatch(LAT_LABELS, label, re.IGNORECASE):
                lat_val = val
            elif re.fullmatch(LON_LABELS, label, re.IGNORECASE):
                lon_val = val
        if lat_val is not None and lon_val is not None:
            results.append((lat_val, lon_val))

    # 2) Buscar pares decimales sueltos lat,lon
    for m in PairFloat.finditer(text):
        lat = float(m.group("lat"))
        lon = float(m.group("lon"))
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            pair = (lat, lon)
            if pair not in results:
                results.append(pair)

    return results

# ---------------------------
# Generadores de enlaces
# ---------------------------

def gmaps_url(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

def osm_url(lat: float, lon: float) -> str:
    return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"

# ---------------------------
# I/O y CLI
# ---------------------------

def read_pairs_from_file(path: str, sep: str = ",") -> Iterable[Tuple[float, float]]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Intento por separador
            if sep in line:
                parts = [p.strip() for p in line.split(sep)]
            else:
                # fallback: espacios
                parts = line.split()
            if len(parts) < 2:
                # prueba extracción libre por si es texto
                for p in extract_from_text(line):
                    yield p
                continue
            pair = parse_coord_pair(parts[0], parts[1])
            if pair:
                yield pair

def main():
    ap = argparse.ArgumentParser(description="Convierte coordenadas a enlaces de Google Maps/OpenStreetMap.")
    ap.add_argument("lat", nargs="?", help="Latitud (decimal o DMS). Opcional si usas --file o --extract.")
    ap.add_argument("lon", nargs="?", help="Longitud (decimal o DMS).")
    ap.add_argument("--file", "-f", help="Archivo con lat,lon por línea (o texto crudo).")
    ap.add_argument("--sep", default=",", help="Separador de columnas (por defecto ',').")
    ap.add_argument("--extract", action="store_true", help="Extraer coordenadas desde texto crudo (stdin o --file).")
    ap.add_argument("--open", action="store_true", help="Abrir enlaces en el navegador.")
    ap.add_argument("--osm", action="store_true", help="Además del enlace de Google Maps, genera enlace OSM.")
    ap.add_argument("--output", "-o", help="Guardar enlaces en un archivo.")
    args = ap.parse_args()

    pairs: List[Tuple[float, float]] = []

    # Entrada por argumentos directos
    if args.lat and args.lon:
        pair = parse_coord_pair(args.lat, args.lon)
        if not pair:
            sys.exit("[-] Error: no pude interpretar lat/lon proporcionadas.")
        pairs.append(pair)

    # Entrada por archivo
    if args.file:
        content = None
        try:
            if args.extract:
                with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                pairs.extend(extract_from_text(content))
            else:
                pairs.extend(list(read_pairs_from_file(args.file, sep=args.sep)))
        except FileNotFoundError:
            sys.exit(f"[-] Archivo no encontrado: {args.file}")

    # Entrada por STDIN (piping), útil con --extract
    if not pairs and args.extract and not sys.stdin.isatty():
        text = sys.stdin.read()
        pairs.extend(extract_from_text(text))

    if not pairs:
        ap.print_help(sys.stderr)
        sys.exit("\n[-] No se encontraron coordenadas para procesar.")

    out_lines = []
    for (lat, lon) in pairs:
        gm = gmaps_url(lat, lon)
        line = gm
        if args.osm:
            line += "    |    " + osm_url(lat, lon)
        out_lines.append(line)
        print(line)
        if args.open:
            try:
                webbrowser.open(gm)
            except Exception as e:
                print(f"[!] No se pudo abrir el navegador: {e}", file=sys.stderr)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("\n".join(out_lines) + "\n")
        except Exception as e:
            sys.exit(f"[-] No pude escribir en {args.output}: {e}")

if __name__ == "__main__":
    main()
