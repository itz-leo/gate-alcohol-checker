from conexionBD import * 
from peso import *
# --- Mapeo tolerante de nombres de aerolínea en caso de variaciones en entrada ---
_AIRLINE_ALIAS = {
    "patovuelos": "PatoVuelo",
    "patovuelo": "PatoVuelo",
    "pato vuelo": "PatoVuelo",
    "esenciavuelos": "EsenciaVuelos",
    "esencia vuelos": "EsenciaVuelos",
    "esencia vuelo": "EsenciaVuelos",
    "aguilavuelo": "AguilaVuelo",
    "aguila vuelo": "AguilaVuelo",
    "aguilavuelos": "AguilaVuelo",
}

def _normalize_airline(name: str) -> str:
    if not name:
        return name
    key = name.replace(" ", "").lower()
    return _AIRLINE_ALIAS.get(key, name)

# --- Helpers para normalizar entradas ---
def _is_scale_value(v):
    return isinstance(v, int) and v in (1,2,3)

def _is_percentage_value(v):
    try:
        return isinstance(v, (int, float)) and (0 <= v <= 100)
    except:
        return False

def _to_int_safe(v):
    try:
        return int(v)
    except:
        return None

# Convierte un porcentaje real -> escala 3/2/1 usando la política de la aerolínea
def _percentage_to_scale(actual_pct: float, min_policy_pct: int) -> int:
    """
    Regla (configurable):
      - escala 3: actual_pct >= min_policy_pct
      - escala 2: min_policy_pct - 15 <= actual_pct < min_policy_pct
      - escala 1: actual_pct < min_policy_pct - 15
    """
    if actual_pct is None:
        return 1
    if actual_pct >= min_policy_pct:
        return 3
    if actual_pct >= max(0, min_policy_pct - 15):
        return 2
    return 1

# Obtiene la escala 1-3 para PORCENTAJE_CONTENIDO:
def _resolve_porcentaje_scale(value, aerolinea_normalizada):
    # 1) Si ya es escala 1-3:
    if _is_scale_value(value):
        return int(value)
    # 2) Si es porcentaje numérico 0-100:
    if _is_percentage_value(value):
        try:
            policy_min = int(obtener_politica(aerolinea_normalizada))
        except Exception:
            policy_min = 70
        return _percentage_to_scale(float(value), policy_min)
    # 3) Si no trae porcentaje, intentamos calcularlo con la báscula / DB:
    try:
        actual_pct = determinar_porcentaje(aerolinea_normalizada)
        policy_min = int(obtener_politica(aerolinea_normalizada))
        return _percentage_to_scale(float(actual_pct), policy_min)
    except Exception:
        return 1

# Normaliza sello/etiqueta/limpieza: si vienen como escala 1-3, perfecto.
# Si vienen como texto no manejado, intentar inferir por palabra clave simple.
def _resolve_simple_scale(value):
    if _is_scale_value(value):
        return int(value)
    if isinstance(value, str):
        v = value.strip().lower()
        
        # --- Nivel 3 (Excelente / OK) ---
        if v in ("excelente", "excelente ", "bueno", "intacto", "sellado", "resellado", "nuevo",
                 "excellent", "good", "intact", "sealed"):
            return 3
            
        # --- Nivel 2 (Aceptable / Medio) ---
        if v in ("aceptable", "ligero daño", "poco desgastada", "good", "ok", "resealed",
                 "fair", "slightly damaged"):
            return 2
            
        # --- Nivel 1 (Pobre / Malo) ---
        if v in ("pobre", "mal estado", "alto daño", "muy desgastada", "abierto", "damaged",
                 "poor", "opened", "heavily damaged"):
            return 1
            
        # si es numérico en string
        try:
            n = int(v)
            if n in (1,2,3):
                return n
        except:
            pass
            
    return 1

def decidir_accion(datos: dict, aerolinea: str) -> str:
    """
    datos: dict con llaves:
      - 'ESTATUS_SELLO' (int 1-3 o texto)
      - 'ESTATUS_ETIQUETA' (int 1-3 o texto)
      - 'LIMPIEZA' (int 1-3 o texto)
      - 'PORCENTAJE_CONTENIDO' (int 1-3, o porcentaje 0-100, o None para calcular desde báscula)

    aerolinea: nombre de la aerolinea (ej: "PatoVuelos", "EsenciaVuelos", "AguilaVuelos")
    Retorna: una de las cadenas EXACTAS: 'KEEP', 'REFILL', 'REPLACE', 'DISCARD'
    """
    
    # Normalizar aerolínea para coincidir con tu tabla SLA
    aerolinea_norm = _normalize_airline(aerolinea)

    # Resolver valores
    sello = _resolve_simple_scale(datos.get("ESTATUS_SELLO"))
    etiqueta = _resolve_simple_scale(datos.get("ESTATUS_ETIQUETA"))
    limpieza = _resolve_simple_scale(datos.get("LIMPIEZA"))
    porcentaje_scale = _resolve_porcentaje_scale(datos.get("PORCENTAJE_CONTENIDO"), aerolinea_norm)

    # Reglas (priorizadas y deterministas)
    # 1) Si hay combinación muy mala -> DISCARD
    if limpieza == 1 and (sello == 1 or etiqueta == 1 or porcentaje_scale == 1):
        return "DISCARD"

    # 2) Si porcentaje es críticamente bajo y limpieza mala -> DISCARD
    if porcentaje_scale == 1 and limpieza == 1:
        return "DISCARD"

    # 3) Si sello está roto/abierto (muy malo) -> REPLACE (o DISCARD si además limpieza lo requiere)
    if sello == 1:
        # si además porcentaje muy bajo y etiqueta mala -> DISCARD
        if porcentaje_scale == 1 and etiqueta == 1:
            return "DISCARD"
        return "REPLACE"

    # 4) Si etiqueta o limpieza muy dañadas -> REPLACE
    if etiqueta == 1 or limpieza == 1:
        return "REPLACE"

    # 5) Si porcentaje por debajo de política (scale==1) -> REPLACE
    if porcentaje_scale == 1:
        return "REPLACE"

    # 6) Si porcentaje en rango medio (scale==2) y resto OK -> REFILL
    if porcentaje_scale == 2 and limpieza >= 2 and sello >= 2 and etiqueta >= 2:
        return "REFILL"

    # 7) Si todo está bien -> KEEP
    if sello >= 2 and etiqueta >= 2 and limpieza >= 2 and porcentaje_scale == 3:
        return "KEEP"

    # 8) Casos intermedios -> REFILL preferente, salvo si hay un 1 ya cubierto
    # (por ejemplo: etiqueta=2, limpieza=2, sello=2, porcentaje=2 -> REFILL)
    return "REFILL"

if __name__ == "__main__":

    datos1 = {
        "ESTATUS_SELLO": 3,
        "ESTATUS_ETIQUETA": 1,
        "LIMPIEZA": 2,
        "PORCENTAJE_CONTENIDO": 3  # ya en escala -> interpreta como "bueno"
    }
    print(decidir_accion(datos1, "PatoVuelos"))  

