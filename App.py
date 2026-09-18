import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# ============================================================
#  SISTEMA DE REGISTRO DE MANTENIMIENTO - SAN MIGUEL
#  Identidad visual corporativa
# ============================================================

st.set_page_config(
    page_title="Mantenimiento | San Miguel",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
#  RECURSOS GRÁFICOS
#  Dejá estas dos imágenes en la MISMA carpeta que App.py
# ------------------------------------------------------------
ARCHIVO_LOGO = "logo.jpg"
ARCHIVO_PLANTA = "foto_de_la_empresa_vista_aerea.jpg"


@st.cache_data
def imagen_base64(ruta):
    """Devuelve la imagen como data-URI para poder usarla dentro del CSS."""
    candidatos = [ruta, ruta.replace("_", " ")]
    for c in candidatos:
        if os.path.exists(c):
            with open(c, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ext = "png" if c.lower().endswith(".png") else "jpeg"
            return f"data:image/{ext};base64,{b64}"
    return ""


def _ancho_total():
    """Compatibilidad entre versiones de Streamlit para los elementos a ancho completo."""
    try:
        v = tuple(int(p) for p in st.__version__.split(".")[:2])
    except Exception:
        v = (0, 0)
    return {"width": "stretch"} if v >= (1, 50) else {"use_container_width": True}


ANCHO = _ancho_total()


def _kw_placeholder(texto):
    """Agrega placeholder sólo si la versión de Streamlit lo admite."""
    try:
        import inspect
        if "placeholder" in inspect.signature(st.multiselect).parameters:
            return {"placeholder": texto}
    except Exception:
        pass
    return {}

LOGO = imagen_base64(ARCHIVO_LOGO)
PLANTA = imagen_base64(ARCHIVO_PLANTA)

# Fondos: si falta la imagen, se usa un degradado verde como respaldo
FONDO_PLANTA = f"url('{PLANTA}')" if PLANTA else "linear-gradient(135deg,#1F4620,#6BA82E)"
FONDO_LOGO = f"url('{LOGO}')" if LOGO else "linear-gradient(135deg,#6BA82E,#8CC63F)"

# ------------------------------------------------------------
#  PALETA Y ESTILOS
# ------------------------------------------------------------
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Nunito+Sans:wght@400;600;700&display=swap');
:root {{
    --sm-verde:        #6BA82E;
    --sm-verde-claro:  #8CC63F;
    --sm-verde-hondo:  #1F4620;
    --sm-verde-humo:   #E8F1DF;
    --sm-limon:        #F4C430;
    --sm-tinta:        #26302A;
    --sm-gris:         #6E7A70;
    --sm-papel:        #F1F4EE;
    --sm-linea:        #DCE4D6;
}}

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp {{
    font-family: 'Nunito Sans', 'Segoe UI', system-ui, sans-serif;
    color: var(--sm-tinta);
}}

/* Foto de planta como fondo permanente, atenuada para no molestar la lectura */
.stApp {{
    background-image:
        linear-gradient(rgba(241,244,238,0.94), rgba(241,244,238,0.97)),
        {FONDO_PLANTA};
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
}}

h1, h2, h3, h4 {{
    font-family: 'Nunito', 'Segoe UI', sans-serif;
    font-weight: 800;
    letter-spacing: -0.01em;
    color: var(--sm-verde-hondo);
}}

#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1500px; }}

/* ---------- Portada ---------- */
.sm-hero {{
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    min-height: 230px;
    display: flex;
    align-items: flex-end;
    background-image:
        linear-gradient(100deg, rgba(31,70,32,0.94) 0%, rgba(31,70,32,0.72) 42%, rgba(31,70,32,0.15) 100%),
        {FONDO_PLANTA};
    background-size: cover;
    background-position: center 38%;
    box-shadow: 0 18px 38px -22px rgba(31,70,32,0.75);
    border-bottom: 6px solid var(--sm-verde-claro);
}}
.sm-hero-txt {{ padding: 30px 38px 28px; }}
.sm-hero-marca {{
    display: inline-block;
    font-family: 'Nunito', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    background: rgba(140,198,63,0.85);
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 14px;
}}
.sm-hero-txt h1 {{
    color: #ffffff;
    font-size: 40px;
    line-height: 1.05;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 14px rgba(0,0,0,0.35);
}}
.sm-hero-txt p {{
    color: rgba(255,255,255,0.9);
    font-size: 16px;
    margin: 0;
    max-width: 60ch;
}}

/* ---------- Barra lateral ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--sm-verde-hondo) 0%, #14301a 100%);
    border-right: 4px solid var(--sm-verde-claro);
}}
section[data-testid="stSidebar"] * {{ color: #EAF3E3 !important; }}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{ color: #ffffff !important; }}
.sm-logo-lateral {{
    height: 92px;
    border-radius: 12px;
    background-image: {FONDO_LOGO};
    background-size: cover;
    background-position: center;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px -10px rgba(0,0,0,0.6);
}}
.sm-nota {{
    background: rgba(255,255,255,0.08);
    border-left: 3px solid var(--sm-verde-claro);
    border-radius: 0 10px 10px 0;
    padding: 12px 14px;
    font-size: 14px;
    line-height: 1.5;
}}
.sm-dato {{ display: flex; justify-content: space-between; padding: 9px 2px; border-bottom: 1px solid rgba(255,255,255,0.12); font-size: 14px; }}
.sm-dato b {{ color: var(--sm-verde-claro) !important; font-size: 16px; }}

/* ---------- Solapas ---------- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: #ffffff;
    padding: 7px;
    border-radius: 14px;
    border: 1px solid var(--sm-linea);
}}
.stTabs [data-baseweb="tab"] {{
    height: 46px;
    border-radius: 10px;
    padding: 0 22px;
    font-weight: 700;
    font-size: 15px;
    color: var(--sm-gris);
    background: transparent;
}}
.stTabs [aria-selected="true"] {{
    background: var(--sm-verde) !important;
    color: #ffffff !important;
}}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* ---------- Tarjetas y formulario ---------- */
div[data-testid="stForm"] {{
    background: #ffffff;
    padding: 26px 28px;
    border-radius: 16px;
    border: 1px solid var(--sm-linea);
    border-top: 5px solid var(--sm-verde);
    box-shadow: 0 14px 30px -26px rgba(31,70,32,0.55);
}}
.sm-panel {{
    background: #ffffff;
    border: 1px solid var(--sm-linea);
    border-left: 5px solid var(--sm-verde-claro);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 18px;
}}
.sm-titulo {{
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 19px;
    color: var(--sm-verde-hondo);
    margin: 4px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.sm-titulo::before {{
    content: "";
    width: 6px; height: 22px;
    background: var(--sm-verde-claro);
    border-radius: 3px;
}}

/* ---------- Campos ---------- */
div[data-baseweb="select"] > div,
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {{
    border-radius: 10px !important;
    border: 1.5px solid var(--sm-linea) !important;
    background: #FBFCFA !important;
}}
div[data-baseweb="select"] > div:focus-within,
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: var(--sm-verde) !important;
    box-shadow: 0 0 0 3px rgba(107,168,46,0.18) !important;
}}
label, .stMarkdown p {{ font-size: 14.5px; }}
div[data-testid="stWidgetLabel"] label p {{ font-weight: 700; color: var(--sm-verde-hondo); }}
span[data-baseweb="tag"] {{ background: var(--sm-verde) !important; border-radius: 8px !important; }}

/* ---------- Botones ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
    background: var(--sm-verde);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 11px 26px;
    font-weight: 700;
    font-size: 15px;
    transition: background .15s ease, transform .1s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
    background: var(--sm-verde-hondo);
    color: #ffffff;
    transform: translateY(-1px);
}}
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible {{
    outline: 3px solid var(--sm-limon);
    outline-offset: 2px;
}}

/* ---------- Indicadores ---------- */
div[data-testid="stMetric"] {{
    background: #ffffff;
    border: 1px solid var(--sm-linea);
    border-radius: 14px;
    padding: 16px 18px;
    border-bottom: 4px solid var(--sm-verde-claro);
}}
div[data-testid="stMetricValue"] {{ color: var(--sm-verde-hondo); font-weight: 800; }}
div[data-testid="stMetricLabel"] p {{ color: var(--sm-gris); font-weight: 700; font-size: 13px; }}

/* ---------- Tabla y avisos ---------- */
div[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; border: 1px solid var(--sm-linea); }}
div[data-testid="stAlert"] {{ border-radius: 12px; }}
hr {{ border-color: var(--sm-linea); }}

/* ---------- Pantalla de acceso ---------- */
.sm-acceso {{
    border-radius: 18px;
    overflow: hidden;
    height: 210px;
    background-image: {FONDO_LOGO};
    background-size: cover;
    background-position: center;
    margin: 12px 0 26px 0;
    border-bottom: 6px solid var(--sm-verde-claro);
    box-shadow: 0 18px 38px -24px rgba(31,70,32,0.7);
}}
.sm-acceso-txt {{ text-align: center; margin-bottom: 18px; }}
.sm-acceso-txt h2 {{ font-size: 28px; margin: 0 0 4px 0; }}
.sm-acceso-txt p {{ color: var(--sm-gris); margin: 0 0 6px 0; font-size: 15px; }}

/* ---------- Ajustes finales de solapas y gráficos ---------- */
.stTabs [data-baseweb="tab-list"] {{
    background: #ffffff !important;
    border: 1px solid var(--sm-linea) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    box-shadow: 0 10px 24px -22px rgba(31,70,32,0.6);
}}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    background-color: transparent !important;
    height: 0 !important;
    display: none !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ background: var(--sm-verde-humo); color: var(--sm-verde-hondo); }}

/* Solapas en versiones nuevas de Streamlit (react-aria) */
.stTabs [role="tablist"] {{
    background: #ffffff !important;
    border: 1px solid var(--sm-linea) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 6px;
    display: flex;
    box-shadow: 0 10px 24px -22px rgba(31,70,32,0.6);
}}
.stTabs [data-orientation="horizontal"] {{ border-bottom: none !important; }}
.stTabs [data-testid="stTab"] {{
    height: 44px;
    display: flex;
    align-items: center;
    border-radius: 10px;
    padding: 0 20px;
}}
.stTabs [data-testid="stTab"] p {{ font-weight: 700; font-size: 15px; color: var(--sm-gris); margin: 0; }}
.stTabs [data-testid="stTab"]:hover {{ background: var(--sm-verde-humo); }}
.stTabs [data-testid="stTab"][aria-selected="true"] {{ background: var(--sm-verde) !important; }}
.stTabs [data-testid="stTab"][aria-selected="true"] p {{ color: #ffffff !important; }}
.stTabs .react-aria-SelectionIndicator {{ display: none !important; background: transparent !important; }}

div[data-testid="stVegaLiteChart"], .stVegaLiteChart {{
    background: #ffffff;
    border: 1px solid var(--sm-linea);
    border-radius: 14px;
    padding: 12px;
}}

@media (max-width: 640px) {{
    .sm-hero-txt h1 {{ font-size: 27px; }}
    .sm-hero-txt {{ padding: 22px; }}
}}
@media (prefers-reduced-motion: reduce) {{
    * {{ transition: none !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
#  ACCESO
# ------------------------------------------------------------
PASSWORD_CORRECTA = "mantenimiento2026"


def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown('<div class="sm-acceso"></div>', unsafe_allow_html=True)

        izq, centro, der = st.columns([1, 1.5, 1])
        with centro:
            st.markdown("""
                <div class="sm-acceso-txt">
                    <h2>Sistema de mantenimiento</h2>
                    <p>Registro de tareas técnicas de planta</p>
                </div>
            """, unsafe_allow_html=True)

            with st.form("form_acceso"):
                clave = st.text_input("Contraseña", type="password", label_visibility="collapsed",
                                      placeholder="Contraseña de acceso")
                entrar = st.form_submit_button("Entrar al sistema", **ANCHO)

            if entrar:
                if clave == PASSWORD_CORRECTA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("La contraseña no coincide. Revisala y probá de nuevo.")
        return False
    return True


if not verificar_password():
    st.stop()


# ------------------------------------------------------------
#  SECTORES, EQUIPOS Y LISTAS MAESTRAS
# ------------------------------------------------------------
SECTORES_EQUIPOS = {
    "APV": [
        "1ER EFECTO", "2DO EFECTO", "3ER EFECTO", "APV BBA DEL DESAREADOR", "BBA CHICA DE PRODUCTO",
        "BBA DE AGUA N°1", "BBA DE J25", "BBA DE J26", "BBA DE RECUPERACION DE CONDENSADO",
        "BBA DE TANQUE BALANZA", "BBA DEL DESAIREADOR DE 1 CUERPO", "BBA GRANDE DE PRODUCTO",
        "BBA PRINCIPAL DE AGUA TORRE DE ENFRIAMIENTO", "BBA SALIDA DE PRODUCTO", "BBA VERTICAL DE AGUA DE MANIOBRA",
        "BBA. DEL TK", "BBA. DEL TQ", "BOMBA DE SALIDA DE LODO , CENTRIFUGA 300", "BOMBA SALIDA - BACK UP",
        "CALDERIN", "CAÑERIA", "CENTRIFUGA 300", "CENTRIFUGA 617", "CENTRIFUGA 717", "CONCENTRADOR",
        "CONDENSADOR CHICO", "CUADRO DE VAPOR", "OTRO (SIN CLASIFICAR)", "PASTEURIZADOR", "PAZTEURIZADOR",
        "PLACA DE INTERCAMBIADORES", "TABLERO", "TASTE N5", "TORRE DE ENFRIAMIENTO", "TORRE DEL APV",
        "TORRE NORTE", "TORRE SUR", "VALVULA", "VALVULA DE SODA Y DE AGUA", "VENTILADOR"
    ],
    "ASEPTICO": [
        "ASEPTICO", "BBA ALFA LAVAL", "BBA DE AGUA", "BBA DEL CIP DE LIMPIEZA", "BBA GRUNFUS DE ALTA Y BAJA PRESION",
        "BBA. DE FOSA", "BBA. SUMERGIBLE DE CAMARA", "BBA. T 5", "BOMBA DE ENFRIAMIENTO", "BOMBA LOBULAR",
        "CABINA ALERGENO", "CAÑERIA", "CAUDALIMETRO", "CINTA A RODILLOS", "ENVASADORA", "HOLDING",
        "LLENADORA ASEPTICA", "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "BAJO EXTRACTORAS": [
        "BBA ALIMENTACION A DESTILADOR CONTINUO", "BBA DE CASCARA JUGOS ESPECIALES", "BBA DE DESTILADOR CONTINUO",
        "BBA DEL J20", "BBA DEL J22", "BBA DEL J23", "BBA PUMA AUXILIAR DE LINEA 1", "BOMBA WUASKEHSA DEL PASTEURIZADOR",
        "CAÑERIA", "CAUDALIMETRO", "CINTA SALIDA DE ELEVADOR LINIA N1", "FINISHER DE JUGO ESPECIAL", "FINISHER OLLEJO",
        "J23", "OTRO (SIN CLASIFICAR)", "SINFIN BAJO EXTRACTORA", "SINFIN COLECTOR DE CASCARA", "SINFIN DE BASURA BAJO DE ESPARCIDORA",
        "SINFIN DE CASCARA DE L1", "SINFIN DE CASCARA L2", "SINFÍN DE EMULSION L. 1", "SINFIN DE INTESA 1 Y 2 BAJO EXTRACTORA",
        "SINFIN DE OLLEJO DE LA LINEA 3", "SINFIN DE PULPA", "SINFIN DE QUIEBRE DE L2", "SINFIN PEEL",
        "SINFIN SALIDA EXTRACTORA LINEA 2", "SINFINES", "TABLERO", "TANQUE DE LAVADO DE FINISHERS", "TK AGUA DE LAVADO DE FINISHER"
    ],
    "BALANZA CAMIONES": [
        "BALANZA NORTE", "BALANZA OESTE", "BALANZA SUR", "OTRO (SIN CLASIFICAR)", "TAPA"
    ],
    "BAÑOS": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "BOLCADORA DE BINES": [
        "BOLCADORA"
    ],
    "BROWN": [
        "BOE 1", "BOE 10", "BOE 2", "BOE 3", "BOE 4", "BOE 5", "BOE 6", "BOE 7", "BOE 8", "BOE 9", "TABLERO"
    ],
    "CALDERAS": [
        "BBA ALIMETACION A CALDERA", "BBA POZO 4", "BOMBA 1 CALDERA 1", "BOMBA 1 CALDERA 2", "BOMBA 1 CALDERA 3",
        "BOMBA 1 CALDERA 4", "BOMBA 2 CALDERA 1", "BOMBA 2 CALDERA 2", "BOMBA 2 CALDERA 3", "BOMBA 2 CALDERA 4",
        "CALDERA 1", "CALDERA 2", "CALDERA 3", "CALDERA 4", "CAÑERIA", "CAUDALIMETROS", "ECONOMIZADOR",
        "OTRO (SIN CLASIFICAR)", "TABLERO", "TABLERO DE CALDERA N°1", "TABLERO DE CALDERA N°2", "TABLERO DE CALDERA N°3",
        "TABLERO DE CALDERA N°4", "VTF CALDERA N°1", "VTF CALDERA N°2", "VTF CALDERA N°3", "VTF CALDERA N°4"
    ],
    "CALDERIN": [
        "AGITADOR DE LABORATORIO"
    ],
    "CAMARA DE FRIO": [
        "CAMARA N°1", "CAMARA N°2", "CAMARA N°3", "FORZADORES DE AIRE", "PUERTA CAMARA 1", "PUERTA CAMARA 2",
        "PUERTA CAMARA 3", "TABLERO", "VENTILADORES"
    ],
    "CENTRIFUGA": [
        "BOMBA ALFA LAVAL", "BOMBA DE CIP DE SODA", "CAÑERIA", "CENTRIFUGA 100", "CENTRIFUGA 130 N°1",
        "CENTRIFUGA 130 N°2", "CENTRIFUGA 130 N°3", "CENTRIFUGA 130 P", "CENTRIFUGA 15037 N°1", "CENTRIFUGA 15037 N°2",
        "CENTRIFUGA 1900 N°1", "CENTRIFUGA 1900 N°2", "CENTRIFUGA 20 - Nº1", "CENTRIFUGA 20 - Nº2", "CENTRIFUGA 20 - Nº3",
        "CENTRIFUGA 207", "CENTRIFUGA 230 N°1", "CENTRIFUGA 230 N°2", "CENTRIFUGA 230 N°3", "CENTRIFUGA 230 N°4",
        "CENTRIFUGA 230 N°5", "CENTRIFUGA 314 N°1", "CENTRIFUGA 314 N°2", "CENTRIFUGA Nº4 - 714", "CENTRIFUGA Nº5 - 714",
        "CENTRIFUGA Nº6 - 714 - C/T", "CENTRIFUGA Nº6- 714 (lavalle)", "OTRO (SIN CLASIFICAR)"
    ],
    "CIP CENTRAL": [
        "BBA DE TANQUE MADRE", "BOMBA DE SODA", "CAÑERIA", "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "CIP DE BOE": [
        "AUTOMATISMO DE TANQUE DE AGUA", "BBA DE AGUA N°1", "BBA DE AGUA N1", "BBA DE SODA", "BBA N 2 DE AGUA",
        "BBA N1 DE AGUA", "CIP EBOE", "TANQUE DE AGUA", "TANQUE SODA"
    ],
    "CIP DE FABRICA": [
        "TK DE SODA Y AGUA"
    ],
    "CIP DE LIMPIEZA": [
        "BOMBA DE SODA"
    ],
    "CIP DE SODA": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "CLARIFICADO": [
        "AGITADOR DE ACIDO", "AGITADOR J4", "ARRIBA DE CERAMICO 2", "BBA 1 TK A30", "BBA 2 TK A30", "BBA AGUA",
        "BBA ALFLO 2\"", "BBA COLUMNAS", "BBA DE ÁCIDO CLORHÍDRICO", "BBA DE AGUA", "BBA DE CONDESADO",
        "BBA DE JUGO DE J2", "BBA DE RECHASO DE OSMOSIS A DESCARGA LATERAL", "BBA DE SODA", "BBA DEL CALENTADOR DE AGUA DURA",
        "BBA DEL CIP DECSODA", "BBA DOSIFICADORA DE ACIDO", "BBA J22", "BBA LAVADO COLUMNA 14", "BBA PREPARACION DE SODA",
        "BBA RECHASO PLANTA OSMOSIS A MOLINO", "BBA RECIRCULACIÓN DE SODA", "BBA RECUPERACION A SECADERO",
        "BBA RECUPERACION DE AGUA CONDESADO", "BBA RECUPERACION POR CENTRIFUGA", "BBA SALIDA DE TK 2", "BBA SODA COLUMNAS",
        "BBA TANQUE MADRE SODA", "BBA TK A11", "BBA. DE ACIDO CITRICO", "BBA. DE ACIDO FOSFORICO", "BBA. DE AUXILIO",
        "BBA. DE CIP DE SODA", "BBA. DE CLARIFICADO A MOLINO", "CAÑERIA", "CERÁMICO 2 BOMBA DE ALIMENTACIÓN",
        "CERAMICO N°1", "CERAMICO N°2", "CIP DE SODA", "CIP SODA - TANQUE S1", "CIP SODA - TANQUE S2",
        "COLUMNA N°1", "COLUMNA N°10", "COLUMNA N°11", "COLUMNA N°12", "COLUMNA N°13", "COLUMNA N°14",
        "COLUMNA N°15", "COLUMNA N°16", "COLUMNA N°17", "COLUMNA N°2", "COLUMNA N°3", "COLUMNA N°4",
        "COLUMNA N°5", "COLUMNA N°6", "COLUMNA N°7", "COLUMNA N°8", "COLUMNA N°9", "OTRO (SIN CLASIFICAR)",
        "PASTEURIZADOR", "PLANTA DE OMOSIS NUEVA", "PLANTA DE OMOSIS VIEJA", "TABLERO", "TK J11"
    ],
    "COMEDOR": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "COMEDOR CAMIONEROS": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "DEPOSITO": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "DESCARGA LATERAL": [
        "CINTA 1", "CINTA 2", "CINTA DE BASURA N°1", "CINTA DE BASURA N°2", "CINTA DE BASURA N°3",
        "CINTA DE BASURA N°4", "CINTA DE BASURA N°5", "CINTA DE BASURA N°6", "CINTA DE BASURA N°7", "CINTA DE QUIEBRE",
        "CINTA DE QUIEBRE N°1", "CINTA DE QUIEBRE N°2", "CINTA DE TACO", "CINTA ENTRADA A ELEVADOR", "CINTA PRINCIPAL",
        "ESPARCIDORA LINEA A", "ESPARCIDORA LINEA B", "LAVADORA LINEA A", "LAVADORA LINEA B", "MOLINETE N°1",
        "MOLINETE N°2", "MOLINETE N°3", "MOLINETE N°4", "MOLINETE N°5", "MOLINETE N°6", "MOLINETE N°7",
        "OTRO (SIN CLASIFICAR)", "TABLERO", "TRAMPA DE PIEDRA LINEA A", "TRAMPA DE PIEDRA LINEA B"
    ],
    "DESCARGAS TRASERA": [
        "CINTA ALIMENTACION A ELEVADOR PRINCIPAL LINEA 1", "CINTA DE BASURA", "CINTA DE BASURA 1", "CINTA DE BASURA 2",
        "CINTA DE FOSA A", "CINTA DE FOSA B", "CINTA ENTRADA AL ELEVADOR", "CINTA ESPARCIDORA", "CINTA INGRESO A TAMPA DE PIEDRA",
        "CINTA SALIDA DE ELEVADOR", "CINTA SALIDA ELEVADORES LA", "CINTA SALIDA ELEVADORES LB", "DESAGOTE BATEA",
        "ELEVADOR", "ELEVADOR A", "ELEVADOR B", "MESA DE RODILLOS", "MESA ESPARCIDORA DE TRAMPA DE PIEDRA",
        "MESA ESPARCIDORA DE TRAMPA DE PIEDRA 1", "MESA ESPARCIDORA DE TRAMPA DE PIEDRA 2", "MESA ESPARCIDORA SALIDA DE LAVADORA",
        "MESA ESPARCIDORA SALIDA DE MESA CEPILLO", "MESA LAVADORA", "MOLINETE 1", "MOLINETE 2", "OTRO (SIN CLASIFICAR)",
        "SINFIN DE BASURA", "TABLERO", "TRAMPA DE PIEDRA"
    ],
    "DESCERADO DE ACEITE": [
        "BBA DE BALANZA DESCERADO", "BBA DE FILTRO ROTATIVO 1", "BBA DE FILTRO ROTATIVO 2", "BOMBA SAN PIPER",
        "ENFRIADOR", "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "DESTILERIA": [
        "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "EFLUENTES": [
        "AEREADRO 4", "AGITADOR DE LODO", "AGITADOR DE PREPARADO DE POLIMEROS 3", "AGITADOR DE TK DUFFER 1",
        "AGITADOR DEL BUFFER CHICO", "AGITADOR TK DE LODO", "AIREADOR 1", "AIREADOR 2", "AIREADOR 3", "AIREADOR 4",
        "AIREADOR 5", "AIREADOR 6", "ALJIBE", "ALJIBE 2 ETAPA", "ANTORCHA", "BBA 1 DE PUMPI", "BBA 1500 BORNRMAN",
        "BBA DE INTERCAMBIADOR", "BBA DE LECHADA", "BBA DE LODO P1", "BBA DE LODO P2", "BBA DE LODO P3", "BBA DE PULPA",
        "BBA DE PULPA AUX", "BBA DEL REACTOR", "BBA MARIA", "BBA PARA CARGA DE LODO EN REACTOR", "BOMBA DE RIEGO 1",
        "BOMBA DE RIEGO 2", "BOMBA DE RIEGO 3", "BOMBA DE RIEGO 4", "CALDERA GONELLA", "CALDERIN", "CANAL PERIMETRAL",
        "CAÑERIA", "CARACOL COLECTOR DE DECANTER P3 Y P4", "CARACOL COLECTOR SALIDA DECANTER P1 Y P2", "CAUDALÍMETRO BOMBA MARÍA",
        "CAUDALIMETRO DE REACTOR A LAGUNA", "CAUDALIMETRO DE RIEGO", "CAUDALÍMETRO PARA CALDERA GONELA", "CENTRALINA DE LODO",
        "CHIMANDO 1", "CHIMANGO 2", "DAFF", "DECANTER 1", "DECANTER 2", "DECANTER 3", "DECANTER 4", "FINISHER",
        "GRUPO ELECTROGENO", "OTRO (SIN CLASIFICAR)", "POZO DE AGUA 3", "POZO DE RIEGO", "REACTOR", "REACTOR UASB",
        "SIN FIN DE P1 Y P2", "SIN FIN DE P3 Y P4", "TABLERO"
    ],
    "ENVASADO": [
        "AGITADORES", "CABINA DE ALERGENO", "CAMINERIA", "FILTRO SANITARIO", "FINISHER 100 2", "LINEA 1",
        "LINEA 2", "LINEA 3", "OTRO (SIN CLASIFICAR)", "PASTEURIZADOR FMC", "SALA DE ALERGENOS", "SALA DE BACHEO",
        "SALA DE ENVASE", "SALA DE TANQUES", "TABLERO"
    ],
    "ENVASADO DE ACEITE": [
        "ASEPTICO", "BALANZA 1", "BALANZA 2", "CAÑERIA", "CINTA DE RODILLOS SALIDA DE BALANZA", "CORTINA",
        "FOLDEADO", "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "ENVASADO DE AEL": [
        "FILTRO ROTATIVO DE AEL 1", "FILTRO ROTATIVO DE AEL 2"
    ],
    "ENVASADO DE JUGO": [
        "AGITADOR DEL TK B1", "AGITADOR TK 3", "AGITADOR TK B5", "APAREJO", "ASEPTICO", "BALANZA L1", "BALANZA L2",
        "BBA ALIMENTACION A CISTERNA", "BBA ALIMENTACION AL CREPACO", "BBA DE AGUA PASTEURIZADOR DE PULPA",
        "BBA DE ENFRIADOR DE ASEPTICO", "BBA DE LLENADORA 1", "BBA DE LLENADORA 2", "BBA DE OXONIA", "BBA DE PULPA",
        "CAÑERIA", "FILTRO CAMPANA", "FILTRO SANITARIO", "LLENADORA 1", "LLENADORA 2", "LLENADORA 3", "LLENADORA 4",
        "OTRO (SIN CLASIFICAR)", "TABLERO", "TANQUE 1", "TANQUE 10", "TANQUE 11", "TANQUE 12", "TANQUE 13", "TANQUE 2",
        "TANQUE 3", "TANQUE 4", "TANQUE 5", "TANQUE 6", "TANQUE 7", "TANQUE 8", "TANQUE 9", "TORRE DE ENFRIAMIENTO ASEPTICO"
    ],
    "FOLDEADO": [
        "AGITADOR", "BBA ALIMENTACION A TORRE", "BOMBA DOSIFICADORA", "CENTRIFUGA 5036", "DESTILADOR",
        "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "GENERAL": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "JUGOS ESPECIALES": [
        "BBA ALFA LAVAL", "BBA BAJO EL MOLINO", "BBA BORNEMAN 1900 SALIDA DE PRENSA", "BBA DE JUGO DE PRENSA PEEL",
        "BBA DE SALIDA DEL DECANTER JUMBO", "BBA WAKESHA 60", "BOMBA J 31", "BOMBA J 32", "BOMBA J 33", "BOMBA J 34",
        "BOMBA J 35", "BOMBA J 36", "BOMBA J 37", "CALENTADOR", "CALENTADOR DE JUGO", "CALENTADOR DEL PASTEURIZADOR",
        "CAÑERIA", "CAUDALIMETRO DE CORE", "CAUDALIMETRO DECANTER CORE", "CAUDALÍMETRO DECANTER SHARPLES", "DECANTER ALFA",
        "DECANTER JUMBO", "DECANTER PIRALLISSI", "DECANTER SHARPLER", "FINISHER 1 DE CORE", "FINISHER 1 DE PEEL",
        "FINISHER 2 DE CORE", "FINISHER 2 DE PEEL", "FINISHER DE JUGO", "PRENSA DE CORE", "PRENSA DE PEEL"
    ],
    "LABORATORIO": [
        "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "MOLINOS": [
        "BBA BORNEMAN 1900 2 BAJO MOLINO", "BOMBA 1", "BOMBA 2", "BOMBA 3", "BOMBA 4", "BOMBA BAJO MOLINO",
        "CAÑERIA", "CENTRALINA 1", "CENTRALINA 2", "CENTRALINA 3", "CENTRALINA 4", "CENTRALINA 5", "CENTRALINA 6",
        "MOLINO 1", "MOLINO 2", "MOLINO 3", "MOLINO 4", "MOLINO 5", "MOLINO 6", "OTRO (SIN CLASIFICAR)",
        "PRENSA 300", "PRENSA 530", "SIN FIN ALIMENTADOR A PRENSA 300", "SIN FIN ALIMENTADOR A PRENSA 530",
        "SIN FIN INCLINADADO L 1", "TABLERO"
    ],
    "PRECAMARA": [
        "OTRO (SIN CLASIFICAR)"
    ],
    "SALA BOE": [
        "BBA DE EMULSION", "BBA DE SODA", "BBA MICROFILTRO", "BBA RETRONO SODA", "BBA SALIDA DE MICRO FILTRO",
        "BERKEL", "BOE 2", "BOE 3", "BOE 4", "BOE 5", "BOE 6", "BOE 7", "BOE 8", "BOE 9", "CAÑERIA",
        "CINTA ALIMENTA BOE 2 Y 3", "CINTA ALIMENTA BOE 4 Y 5", "CINTA ALIMENTA BOE 6 Y 9", "CINTA ALIMENTA TAMAÑADORA LINEA 2Y3",
        "CINTA ALIMENTACION A BOE 4", "CINTA ALIMENTACION A BOE 5", "CINTA ALIMENTACIÓN DE TAMAÑADORA LARGA", "CINTA BASURA",
        "CINTA DE BASURA DE RACO", "CINTA DE QUIEBRE", "CINTA DE QUIEBRE SALIDA DE BOE 2 Y 3", "CINTA DE QUIEBRE SALIDA DE ELEVADOR",
        "CINTA ENTRADA TAMAÑADORA CHICA", "CINTA INCLINADA L1", "CINTA INCLINADA L2", "CINTA SALIDA BOE 2 Y 3",
        "CINTA SALIDA BOE 4 Y 5", "CINTA SALIDA BOE 6 Y 9", "CINTA SALIDA DE BOE 4", "CINTA SALIDA DE BOE 5",
        "CINTA SALIDA ELEVADOR PRINCIPAL", "CINTA SALIDA TAMAÑADORA", "CINTA SALIDA TAMAÑADORA CHICA", "CINTA SALIDA TAMAÑADORA LARGA",
        "ELEVADOR 2", "ELEVADOR 3", "ELEVADOR 4", "ELEVADOR 5", "ELEVADOR 6", "ELEVADOR 7", "ELEVADOR 8", "ELEVADOR 9",
        "ELEVADOR PRINCIPAL", "ESPARCIDORA", "EXTRACTORA JBT", "FINISHER 1", "FINISHER 2", "FINISHER 3", "FINISHER 4",
        "FINISHER 5", "JUGUERA FRESCH", "LABORATORIO", "LINEA ORGANICA", "OTRO (SIN CLASIFICAR)", "SIN FIN MICRO FILTRO",
        "TABLERO", "TAMAÑADORA CHICA", "TAMAÑADORA LARGA", "VECTRO"
    ],
    "SALA BOE L1": [
        "BBA DE EMULSION", "BBA SALIDA DE MICRO FILTRO", "BERKEL", "BOE 4", "BOE 5", "CAÑERIA",
        "CINTA ALIMENTACION A BOE 4", "CINTA ALIMENTACION A BOE 5", "CINTA ALIMENTACION A BOE 6", "CINTA DE BASURA DE RACO",
        "CINTA DE QUIEBRE SALIDA DE BOE 2 Y 3", "CINTA DE QUIEBRE SALIDA DE ELEVADOR", "CINTA ENTRADA TAMAÑADORA CHICA",
        "CINTA SALIDA DE BOE 4", "CINTA SALIDA DE BOE 5", "CINTA SALIDA TAMAÑADORA CHICA", "ELEVADOR 4", "ELEVADOR 5",
        "ELEVADOR PRINCIPAL", "ESPARCIDORA", "EXTRACTORA JBT", "FINSHER 1", "FINSHER 2", "FINSHER 3", "FINSHER 4",
        "JUGUERA FRESCH", "LABORATORIO", "LINEA ORGANICA", "OTRO (SIN CLASIFICAR)", "SIN FIN MICRO FILTRO", "TABLERO",
        "TAMAÑADORA CHICA", "VECTRO"
    ],
    "SALA BOE L2Y2": [
        "CINTA ALIMENTACION A BOE 7"
    ],
    "SALA BOE L2Y3": [
        "BOE 2", "BOE 3", "BOE 6", "BOE 7", "BOE 8", "BOE 9", "CAÑERIA", "CINTA ALIMENTA TAMAÑADORA LINEA 2Y3",
        "CINTA ALIMENTACION A BOE 8", "CINTA ALIMENTACION A BOE 9", "CINTA ALIMENTACIÓN DE TAMAÑADORA LARGA", "CINTA BASURA",
        "CINTA DE QUIEBRE", "CINTA SALIDA DE BOE 6", "CINTA SALIDA DE BOE 7", "CINTA SALIDA DE BOE 8", "CINTA SALIDA DE BOE 9",
        "CINTA SALIDA TAMAÑADORA LARGA", "ELEVADOR 2", "ELEVADOR 3", "ELEVADOR 6", "ELEVADOR 7", "ELEVADOR 8", "ELEVADOR 9",
        "ELEVADOR PRINCIPAL", "FINISHER 1", "FINISHER 2", "FINISHER 3", "FINISHER 4", "FINISHER 5", "OTRO (SIN CLASIFICAR)",
        "TABLERO", "TAMAÑADORA LARGA"
    ],
    "SALA DE CENTRÍFUGAS ACEITE": [
        "BBA DE CENTRIFUGA 230 1", "BBA DE CENTRIFUGA 230 2", "BBA DE CENTRIFUGA 230 3", "BBA DE CENTRIFUGA 230 4",
        "BBA DE CENTRIFUGA 230 5", "BBA DE CENTRIFUGA 714 5", "BBA DE CENTRIFUGA 714 6", "CALENTADOR DE EMULSIÓN",
        "CAÑERIA", "CENTRIFUGA 230 1", "CENTRIFUGA 230 2", "CENTRIFUGA 230 3", "CENTRIFUGA 230 4", "CENTRIFUGA 230 5",
        "CENTRIFUGA 617 APV", "CENTRIFUGA 714 5", "CENTRIFUGA 714 6", "CIP", "OTRO (SIN CLASIFICAR)", "PULIDORA 2", "TABLERO"
    ],
    "SALA DE CENTRÍFUGAS JUGO": [
        "CENTRIFUGA 618 1", "CENTRIFUGA 618 2", "CENTRIFUGA 717 1", "CENTRIFUGA 717 2", "CENTRIFUGA W 300",
        "CENTRIFUGAS 100", "CENTRIFUGAS 120", "EXTRACTORA 1", "OTRO (SIN CLASIFICAR)", "TABLERO"
    ],
    "SALA DE EXTRACTORAS": [
        "CAÑERIA", "CINTA ALIMENTACION L1", "CINTA ALIMENTACION L2", "CINTA ALIMENTACION L3", "CINTA DE QUIEBRE",
        "CINTA INCLINADA 1", "CINTA INCLINADA 2", "CINTA INCLINADA 3", "COMPRESOR 1 DE AIRE", "ELEVADOR DE RETORNO 1",
        "ELEVADOR DE RETORNO 2", "ELEVADOR DE RETORNO 3", "ELEVADOR PRINCIPAL 1", "ELEVADOR PRINCIPAL 2", "ELEVADOR PRINCIPAL 3",
        "ELEVADOR RETORNO L2", "EXTRACTORA 1", "EXTRACTORA 10", "EXTRACTORA 11", "EXTRACTORA 12", "EXTRACTORA 13",
        "EXTRACTORA 14", "EXTRACTORA 15", "EXTRACTORA 16", "EXTRACTORA 17", "EXTRACTORA 18", "EXTRACTORA 19", "EXTRACTORA 2",
        "EXTRACTORA 20", "EXTRACTORA 21", "EXTRACTORA 22", "EXTRACTORA 23", "EXTRACTORA 24", "EXTRACTORA 25", "EXTRACTORA 26",
        "EXTRACTORA 27", "EXTRACTORA 28", "EXTRACTORA 29", "EXTRACTORA 3", "EXTRACTORA 30", "EXTRACTORA 31", "EXTRACTORA 32",
        "EXTRACTORA 4", "EXTRACTORA 5", "EXTRACTORA 6", "EXTRACTORA 7", "EXTRACTORA 8", "EXTRACTORA 9", "FINISHER 1",
        "FINISHER 2", "FINISHER 210", "FINISHER 3", "FINISHER 4", "FINISHER 5", "FINISHER 6", "LINEA 1", "LINEA 2",
        "LINEA 3", "MESA ESPARCIDORA 1", "MESA ESPARCIDORA 2", "MESA ESPARCIDORA 3", "OTRO (SIN CLASIFICAR)",
        "PASTEURIZADOR FMC", "SIN FIN DE BASURA", "TABLERO", "TAMAÑADORA L1", "TAMAÑADORA L2", "TAMAÑADORA L3"
    ],
    "SALA DE MÁQUINAS": [
        "COMPRESOR 1 DE AMONIACO", "COMPRESOR 2 DE AIRE", "COMPRESOR 2 DE AMONIACO", "COMPRESOR 3 DE AIRE",
        "COMPRESOR 3 DE AMONIACO", "COMPRESOR 4 DE AIRE", "COMPRESOR 4 DE AMONIACO", "COMPRESOR 5 DE AIRE",
        "COMPRESOR 5 DE AMONIACO", "COMPRESOR 6 DE AIRE", "COMPRESOR 6 DE AMONIACO", "ECONOMIZADOR", "ENFRIADOR CREPACO",
        "ENFRIADOR DE AGUA", "ENFRIADOR DE AGUA CLARIFICADO", "OTRO (SIN CLASIFICAR)", "SEPARADOR 1", "SEPARADOR 2",
        "SEPARADOR 3", "TABLERO", "TORRE DE ENFRIAMENTO 1", "TORRE DE ENFRIAMENTO 2", "TORRE DE ENFRIAMENTO 3"
    ],
    "SALA DE TANQUES": [
        "CINCHONES"
    ],
    "SECADERO FAMAILLA": [
        "ALIMENTADOR DE SINFÍN DE REPROCESO", "CAÑERIA", "CINTA TRANSPORTADORA DE BOLSAS 1", "CINTA TRANSPORTADORA DE BOLSAS 2",
        "CINTAS QUE CONECTA AMBOS SECADEROS", "COMPACTADORA 1", "COMPACTADORA 2", "COMPACTADORA 3", "COMPACTADORA 4",
        "COMPACTADORA 5", "ELEVADOR 1", "ELEVADOR 2", "ELEVADOR 3", "LAVADOR 1", "LAVADOR 2", "LAVADOR 3",
        "OTRO (SIN CLASIFICAR)", "PRENSA 300 1", "PRENSA 300 2", "PRENSA 530 1", "PRENSA 530 2", "PRENSA 530 3",
        "PRENSA 530 4", "PRENSA 530 5", "PRESECADOR 1", "PRESECADOR 2", "PRESECADOR 3", "PRESECADOR 4", "PRESECADOR 5",
        "PRESECADOR 6", "SINFIN ALIMENTACION COMPACTADORA 1", "SINFIN ALIMENTACION COMPACTADORA 4", "SINFIN CHIMANDO 1",
        "SINFIN CHIMANGO 2", "SINFIN COMPACTADORA 1", "SINFIN COMPACTADORA 4", "SINFIN DE CASCARA SALIDA DEL SECADERO 6",
        "SINFIN DE CICLONES DE ENFRIADORES", "SINFIN DE POLVILLO SALIDA DE HIDROCICLÓN", "SINFIN DE QUIEBRE SALIDA DEL PRENSA 530 PROYECTO NO SECADO",
        "SINFIN DE REPROCESO", "SINFIN DE SALIDA DE CASCARA", "TABLERO", "VTI 1", "VTI 2", "VTI 3", "VTI 4", "VTI 5", "VTI 6"
    ],
    "SECADERO LAVALLE": [
        "BBA. DE CONDESADO", "CANAL DE DESAGUE", "CAÑERIA", "CARACOL ALIMENTADOR DE CASCARA SALIDA ENFRIADORES",
        "CARACOL COMPACTADORA 2", "CINTA TRANSPORTADORA DE BOLSA", "COMPACTADORA N°1", "COMPACTADORA N°2",
        "LAVADOR DE CASCARA 1", "LAVADOR DE CASCARA 2", "LAVADOR DE CASCARA 3", "OTRO (SIN CLASIFICAR)",
        "PASILLO DE SIN FIN ALIMENTACION A HORNO", "PRENSA 300 1", "PRENSA 300 2", "PRENSA 530 1", "PRENSA 530 2",
        "PRESECADOR 1 CHICO", "PRESECADOR 2 SAAB", "PRESECADOR 3 VINCENT", "PRESECADOR 4 DI BACCO",
        "SINFIN ALIMENTACION A ENFRIADORES", "SINFIN ALIMENTACION A ENFRIADORES INCLINADO", "SINFIN ALIMENTACION A PRESECADORES",
        "SINFIN ALIMENTACION A TOLVA", "SINFIN ALIMENTACION COMPACTADORA 1", "SINFIN ALIMENTACION COMPACTADORA 2",
        "SINFIN ALIMENTACION COMPACTADORA 3", "SINFIN ALIMENTACION DE PRESECADOR", "TABLERO", "VTI 1", "VTI 2",
        "VTI 3", "VTI 4", "VTI 5", "VTI 6"
    ],
    "TASTES": [
        "BBA 1 TASTES 5", "BBA 2 TASTES 5", "BBA 3 TASTES 5", "BBA 4 TASTES 5", "BBA 5 TASTES 5", "BBA 6 TASTES 5",
        "BBA 7 TASTES 5", "BBA 8 TASTES 5", "BBA DE CONDESADO TASTES 5", "BBA DEL 6 EFECTO TASTES 5", "BBA N°1 TASTES 1",
        "BBA N°1 TASTES 2", "BBA N°1 TASTES 3", "BBA N°1 TASTES 4", "BBA N°2 TASTES 1", "BBA N°2 TASTES 2",
        "BBA N°2 TASTES 3", "BBA N°2 TASTES 4", "BBA N°3 TASTES 1", "BBA N°3 TASTES 2", "BBA N°3 TASTES 3",
        "BBA N°3 TASTES 4", "BBA N°4 TASTES 1", "BBA N°4 TASTES 2", "BBA N°4 TASTES 4", "BBA N°5 TASTES 1",
        "BBA N°5 TASTES 2", "BBA N°5 TASTES 4", "BBA N°6 TASTES 1", "BBA N°6 TASTES 2", "BBA N°6 TASTES 4",
        "BBA N°7 TASTES 2", "BBA N°7 TASTES 4", "BBA SALIDA DE TORRE TASTES 4", "BBA SALIDA PRODUCTO TASTES 2",
        "BBA SALIDA PRODUCTO TASTES 5", "BOMBA A TORNILLO TASTES 4", "BOMBA DE AGUA DE TORRES TASTES 5",
        "BOMBA DE EFECTOS 1 TASTES 4", "BOMBA DE EFECTOS 2 TASTES 4", "BOMBA DE EFECTOS 3 TASTES 4",
        "BOMBA DE EFECTOS 4 TASTES 4", "BOMBA SALIDA PRODUCTO TASTES 5", "BOMBAS DE 2DO Y 5TO EFECTO TASTES 4",
        "CAÑERIA TASTES 1", "CAÑERIA TASTES 2", "CAÑERIA TASTES 3", "CAÑERIA TASTES 4", "CAÑERIA TASTES 5",
        "DESTILADOR CONTINUO", "OTRO (SIN CLASIFICAR) TASTES 1", "OTRO (SIN CLASIFICAR) TASTES 2", "OTRO (SIN CLASIFICAR) TASTES 3",
        "OTRO (SIN CLASIFICAR) TASTES 4", "OTRO (SIN CLASIFICAR) TASTES 5", "TABLERO", "TASTES 1", "TASTES 2",
        "TASTES 3", "TASTES 4", "TASTES 5"
    ]
}

TECNICOS_LISTA = [
    "ESCOBAR JOSE", "GONZALEZ RAUL", "ORTIZ VICTOR", "RODRIGUEZ JOSE LUIS", "SALICA JORGE",
    "CABRERA ROQUE", "ELIAS JUAN", "JAIME FERNANDO", "LAVERGNE PATRICIO", "MARTINEZ DANIEL",
    "ALVAREZ JORGE", "BARRIENTOS ALVARO", "BRITOS SEBASTIAN", "CORTES HERNAN", "DAZA ROBERTO",
    "DIAZ DANIEL", "DIAZ JORGE", "DIAZ MIGUEL", "FERNANDEZ ENRIQUE", "FERRO OSCAR",
    "GARCIA PRATS JUAN", "LUNA RODOLFO", "MEDINA MARIO", "MENDOZA CARLOS", "MENDOZA CARLOS MEN",
    "OLIVERA LUIS", "ORTIZ ARIEL", "OSORES JORGE", "RODRIGUEZ ESTEBAN", "SAJAMA PATRICIO",
    "TERCERO CARLOS", "VARELA MIGUEL", "ZAMORA PABLO", "MARTINEZ MAXI", "BAZAN HUGO",
    "BRITOS BRUNO", "CARRE CLAUDIO", "CENTENO ANGEL", "FERREIRA PEDRO", "GRAMAJO HECTOR",
    "JUAREZ VICTOR", "LEGIZAMON DANIEL"
]

TIPOS_TRABAJO = ["Mejora", "Predictivo", "Preventivo", "Inspeccion", "Correctivo"]
ESPECIALIDADES = ["Soldadura", "Electricidad", "Instrumentacion", "Automatizacion", "Mecanica"]

# ------------------------------------------------------------
#  ARCHIVO EXCEL
# ------------------------------------------------------------
EXCEL_FILE = "TAREAS REALIZADAS POR LOS TECNICOS.xlsx"
SHEET_NAME = "Tareas Realizadas"

COLUMNAS = [
    'Id', 'Hora de inicio', 'Fecha', 'Turno', 'Nombre de Colaborador',
    'Evento Reportado', 'N° tarea Plan.', 'Hora Inicio', 'Hora Fin',
    'Sector', 'Equipo', 'Descripción de Tarea', 'Ejecutantes',
    'Comentarios Adicionales', 'Impacto de la Falla', 'Estado',
    'Duración [min]', 'N° de p.', 'Día', 'Aprobación', 'Especialidad', 'Tipo de Trabajo'
]

DIAS_ES = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}


def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        try:
            return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        except Exception:
            pass
    return pd.DataFrame(columns=COLUMNAS)


def guardar_datos(df):
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=SHEET_NAME, index=False)


df_registros = cargar_datos()

# ------------------------------------------------------------
#  BARRA LATERAL
# ------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sm-logo-lateral"></div>', unsafe_allow_html=True)
    st.markdown("### Panel de control")

    total = len(df_registros)
    hoy = 0
    if total and 'Fecha' in df_registros:
        hoy = (df_registros['Fecha'].astype(str) == str(datetime.now().date())).sum()

    st.markdown(f"""
        <div class="sm-dato"><span>Tareas registradas</span><b>{total}</b></div>
        <div class="sm-dato"><span>Cargadas hoy</span><b>{hoy}</b></div>
        <div class="sm-dato"><span>Sectores</span><b>{len(SECTORES_EQUIPOS)}</b></div>
        <div class="sm-dato"><span>Técnicos</span><b>{len(TECNICOS_LISTA)}</b></div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="sm-nota">Cada registro se guarda al instante en la planilla '
        '<b>TAREAS REALIZADAS POR LOS TECNICOS.xlsx</b>, en esta misma carpeta.</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Cerrar sesión", **ANCHO):
        st.session_state.autenticado = False
        st.rerun()

# ------------------------------------------------------------
#  PORTADA
# ------------------------------------------------------------
st.markdown(f"""
<div class="sm-hero">
    <div class="sm-hero-txt">
        <span class="sm-hero-marca">San Miguel · Mantenimiento</span>
        <h1>Registro de tareas de mantenimiento</h1>
        <p>Cargá el trabajo del turno y seguí el histórico de intervenciones por sector y equipo.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Carga de tareas", "Histórico y control"])

# ============================================================
#  TAB 1 — CARGA
# ============================================================
with tab1:
    st.markdown('<div class="sm-titulo">Dónde se hizo el trabajo</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sector_seleccionado = st.selectbox("Sector", list(SECTORES_EQUIPOS.keys()), key="sector_dinamico")
    with col_f2:
        equipos_disponibles = SECTORES_EQUIPOS.get(sector_seleccionado, ["OTRO (SIN CLASIFICAR)"])
        equipo_seleccionado = st.selectbox("Equipo", equipos_disponibles, key="equipo_dinamico")

    st.markdown(
        f'<div class="sm-panel">Vas a registrar una tarea en <b>{sector_seleccionado}</b> — '
        f'<b>{equipo_seleccionado}</b>. Cambiá el sector para actualizar la lista de equipos.</div>',
        unsafe_allow_html=True
    )

    if "mensaje_exito" in st.session_state:
        st.success(st.session_state.mensaje_exito)
        del st.session_state.mensaje_exito

    with st.form("form_mantenimiento", clear_on_submit=True):
        st.markdown('<div class="sm-titulo">Datos del trabajo</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del trabajo", value=datetime.now())
            turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche", "Rotativo"])
            colaborador = st.selectbox("Colaborador que carga el registro", TECNICOS_LISTA)
            tipo_trabajo = st.selectbox("Tipo de trabajo", TIPOS_TRABAJO)
        with col2:
            especialidad = st.selectbox("Especialidad", ESPECIALIDADES)
            impacto = st.selectbox("Impacto de la falla", ["Sin Parada", "Parada Parcial", "Parada Total"])
            estado = st.selectbox("Estado", ["Completado", "Pendiente de Repuestos", "En Seguimiento"])

        tecnicos_seleccionados = st.multiselect("Ejecutantes", TECNICOS_LISTA,
                                                help="Podés elegir uno o varios técnicos.",
                                                **_kw_placeholder("Elegí uno o varios técnicos"))

        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            duracion = st.number_input("Duración [min]", min_value=0, value=60, step=15)
        with col_t2:
            n_tarea_plan = st.text_input("N° tarea planificada", placeholder="Opcional")
        with col_t3:
            n_piezas = st.text_input("N° de pieza / repuesto", placeholder="Opcional")

        st.markdown('<div class="sm-titulo">Qué pasó</div>', unsafe_allow_html=True)
        evento_reportado = st.text_input("Evento reportado", placeholder="Ej.: pérdida en sello de bomba")
        descripcion = st.text_area("Descripción de la tarea", height=110,
                                   placeholder="Contá qué se hizo, con qué repuestos y cómo quedó el equipo.")
        comentarios = st.text_input("Comentarios adicionales", placeholder="Opcional")

        submitted = st.form_submit_button("Guardar registro")

        if submitted:
            if not tecnicos_seleccionados:
                st.error("Falta elegir al menos un técnico en Ejecutantes.")
            elif not descripcion.strip():
                st.error("Falta la descripción de la tarea.")
            else:
                df_actual = cargar_datos()
                nuevo_id = len(df_actual) + 1

                nueva_fila = pd.DataFrame([{
                    'Id': nuevo_id,
                    'Hora de inicio': datetime.now().strftime("%H:%M:%S"),
                    'Fecha': str(fecha),
                    'Turno': turno,
                    'Nombre de Colaborador': colaborador,
                    'Evento Reportado': evento_reportado,
                    'N° tarea Plan.': n_tarea_plan,
                    'Hora Inicio': "",
                    'Hora Fin': "",
                    'Sector': sector_seleccionado,
                    'Equipo': equipo_seleccionado,
                    'Descripción de Tarea': descripcion,
                    'Ejecutantes': ", ".join(tecnicos_seleccionados),
                    'Comentarios Adicionales': comentarios,
                    'Impacto de la Falla': impacto,
                    'Estado': estado,
                    'Duración [min]': duracion,
                    'N° de p.': n_piezas,
                    'Día': DIAS_ES.get(fecha.strftime("%A"), fecha.strftime("%A")),
                    'Aprobación': "Pendiente",
                    'Especialidad': especialidad,
                    'Tipo de Trabajo': tipo_trabajo
                }])

                df_actual = pd.concat([df_actual, nueva_fila], ignore_index=True)
                guardar_datos(df_actual)

                st.session_state.mensaje_exito = f"Tarea #{nuevo_id} guardada en la planilla."
                st.rerun()

# ============================================================
#  TAB 2 — HISTÓRICO
# ============================================================
with tab2:
    df = cargar_datos()

    if df.empty:
        st.markdown(
            '<div class="sm-panel">Todavía no hay tareas cargadas. '
            'Registrá la primera desde la solapa <b>Carga de tareas</b> y acá vas a ver el histórico completo.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="sm-titulo">Resumen general</div>', unsafe_allow_html=True)

        duraciones = pd.to_numeric(df.get('Duración [min]'), errors='coerce')
        horas = round(duraciones.sum() / 60, 1) if duraciones.notna().any() else 0
        promedio = int(duraciones.mean()) if duraciones.notna().any() else 0
        paradas = int((df.get('Impacto de la Falla', pd.Series(dtype=str)).astype(str) != "Sin Parada").sum())

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tareas registradas", len(df))
        m2.metric("Horas de trabajo", f"{horas} h")
        m3.metric("Duración promedio", f"{promedio} min")
        m4.metric("Con parada de planta", paradas)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sm-titulo">Filtrar el histórico</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            f_sector = st.multiselect("Sector", sorted(df['Sector'].dropna().astype(str).unique()),
                                      **_kw_placeholder("Todos los sectores"))
        with c2:
            f_estado = st.multiselect("Estado", sorted(df['Estado'].dropna().astype(str).unique()),
                                      **_kw_placeholder("Todos los estados"))
        with c3:
            f_texto = st.text_input("Buscar en descripción o equipo", placeholder="Ej.: bomba, sello, motor")

        dfv = df.copy()
        if f_sector:
            dfv = dfv[dfv['Sector'].astype(str).isin(f_sector)]
        if f_estado:
            dfv = dfv[dfv['Estado'].astype(str).isin(f_estado)]
        if f_texto:
            t = f_texto.lower()
            dfv = dfv[
                dfv['Descripción de Tarea'].astype(str).str.lower().str.contains(t, na=False) |
                dfv['Equipo'].astype(str).str.lower().str.contains(t, na=False)
            ]

        g1, g2 = st.columns([1.3, 1])
        with g1:
            st.markdown('<div class="sm-titulo">Tareas por sector</div>', unsafe_allow_html=True)
            por_sector = dfv['Sector'].astype(str).value_counts().head(12)
            if not por_sector.empty:
                st.bar_chart(por_sector, color="#6BA82E", height=300)
        with g2:
            st.markdown('<div class="sm-titulo">Tareas por especialidad</div>', unsafe_allow_html=True)
            if 'Especialidad' in dfv:
                por_esp = dfv['Especialidad'].astype(str).value_counts()
                if not por_esp.empty:
                    st.bar_chart(por_esp, color="#8CC63F", height=300)

        st.markdown(f'<div class="sm-titulo">Detalle ({len(dfv)} registros)</div>', unsafe_allow_html=True)
        st.dataframe(dfv, **ANCHO, hide_index=True, height=420)

        if os.path.exists(EXCEL_FILE):
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(
                    label="Descargar planilla completa",
                    data=f,
                    file_name="TAREAS_REALIZADAS_POR_LOS_TECNICOS.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
