import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="Gestión de Tareas - San Miguel",
    page_icon="🟢",
    layout="wide"
)

# --- Estilos CSS personalizados (Identidad San Miguel) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6f8;
    }
    h1, h2, h3 {
        color: #004d26;
    }
    .stButton>button {
        background-color: #006633;
        color: white;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004d26;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Archivo de persistencia ---
EXCEL_FILE = "registro_tareas.xlsx"

def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        # Estructura inicial de la planilla
        return pd.DataFrame(columns=[
            'Id', 'Hora de inicio', 'Fecha', 'Turno', 'Nombre de Colaborador',
            'Evento Reportado', 'N° tarea Plan.', 'Hora Inicio', 'Hora Fin',
            'Sector', 'Equipo', 'Descripción de Tarea', 'Ejecutantes',
            'Comentarios Adicionales', 'Impacto de la Falla', 'Estado',
            'Duración [min]', 'N° de p.', 'Día', 'Aprobación', 'Especialidad', 'Tipo de Trabajo'
        ])

def guardar_datos(df):
    df.to_excel(EXCEL_FILE, index=False)

# --- Diccionarios de apoyo ---
DIAS_ES = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}

EQUIPOS_POR_SECTOR = {
    "Línea de Proceso 1": ["Despaletizador", "Lavadora de cajones", "Llenadora", "Etiquetadora"],
    "Línea de Proceso 2": ["Paletizador", "Túnel de frío", "Filtro de jugo", "Bomba principal"],
    "Sala de Máquinas": ["Compresor 1", "Compresor 2", "Torre de enfriamiento", "Caldera"],
    "Tratamiento de Efluentes": ["Bomba agitadora", "Soplador", "Medidor de pH"]
}

TECNICOS_POR_SECTOR = {
    "Línea de Proceso 1": ["Juan Pérez", "Carlos Gómez", "Luis Martínez"],
    "Línea de Proceso 2": ["Ana Torres", "Mario Ruiz", "Esteban Quito"],
    "Sala de Máquinas": ["Pedro Infante", "Jorge Reyes"],
    "Tratamiento de Efluentes": ["Sofía Albornoz", "Lucas Díaz"]
}

# --- Título Principal ---
st.title("🌿 San Miguel - Registro y Control de Tareas")
st.markdown("---")

# --- Formulario de Carga ---
st.subheader("📝 Carga de Nueva Tarea")

with st.form("form_carga_tarea", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fecha = st.date_input("Fecha", value=datetime.now())
        turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
        colaborador = st.text_input("Nombre de Colaborador", value="Operador Planta")
        sector_seleccionado = st.selectbox("Sector", list(EQUIPOS_POR_SECTOR.keys()))
        
    with col2:
        equipo_seleccionado = st.selectbox("Equipo", EQUIPOS_POR_SECTOR.get(sector_seleccionado, ["General"]))
        especialidad = st.selectbox("Especialidad", ["Mecánica", "Eléctrica", "Instrumentación", "Operativa"])
        tipo_trabajo = st.selectbox("Tipo de Trabajo", ["Correctivo", "Preventivo", "Mejora", "Rutina"])
        impacto = st.selectbox("Impacto de la Falla", ["Sin impacto", "Parcial", "Detención total"])
        
    with col3:
        estado = st.selectbox("Estado", ["Completado", "Pendiente", "En progreso"])
        duracion = st.number_input("Duración [min]", min_value=0, value=30, step=5)
        n_piezas = st.number_input("N° de piezas / Insumos", min_value=0, value=0)
        n_tarea_plan = st.text_input("N° tarea Plan. (Opcional)")

    evento_reportado = st.text_input("Evento Reportado")
    descripcion = st.text_area("Descripción de Tarea Realizada *")
    
    # Selección múltiple de técnicos filtrada por sector
    tecnicos_disponibles = TECNICOS_POR_SECTOR.get(sector_seleccionado, [])
    tecnicos_seleccionados = st.multiselect("Ejecutantes (Técnicos)", tecnicos_disponibles)
    
    comentarios = st.text_area("Comentarios Adicionales")

    st.markdown("---")

    # Distribución en columnas para colocar el botón de guardado y la leyenda de éxito alineados
    col_btn, col_msg = st.columns([1, 3], vertical_alignment="center")
    
    with col_btn:
        submitted = st.form_submit_button("Guardar registro")
        
    with col_msg:
        if "mensaje_exito" in st.session_state:
            st.success(st.session_state.mensaje_exito)
            del st.session_state.mensaje_exito

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

            st.session_state.mensaje_exito = f"¡Tarea #{nuevo_id} guardada con éxito en la planilla!"
            st.rerun()

# --- Visualizador de Registros ---
st.markdown("---")
st.subheader("📊 Registros Actuales")
df_registros = cargar_datos()

if not df_registros.empty:
    st.dataframe(df_registros, use_container_width=True)
    
    # Botón para descargar el Excel completo
    with open(EXCEL_FILE, "rb") as file:
        st.download_button(
            label="📥 Descargar Planilla Completa (Excel)",
            data=file,
            file_name="registro_tareas_san_miguel.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No hay tareas registradas todavía.")
