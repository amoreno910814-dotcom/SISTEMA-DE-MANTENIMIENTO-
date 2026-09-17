import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Mantenimiento",
    page_icon="🔧",
    layout="wide"
)

# --- SISTEMA DE CONTRASEÑA ---
PASSWORD_CORRECTA = "mantenimiento2026"  # Puedes cambiar esta clave cuando gustes

def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("## 🔐 Acceso Restringido - Sistema de Mantenimiento")
        st.info("Por favor, introduce la contraseña para ingresar al sistema de cargas.")
        password_ingresada = st.text_input("Contraseña:", type="password")
        if st.button("Ingresar"):
            if password_ingresada == PASSWORD_CORRECTA:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Inténtalo de nuevo.")
        return False
    return True

if not verificar_password():
    st.stop()

# --- DATOS DE SECTORES Y EQUIPOS ---
SECTORES_EQUIPOS = {
    "Cosecha Mecanizada": [
        "Cosechadoras de Arándanos", "Cosechadoras de Caña", "Tractores de Apoyo", 
        "Carros Tolva", "Módulos de Carga", "Generadores Móviles", 
        "Lavadoras de Bins", "Cintas Transportadoras Portátiles"
    ],
    "Industrial": [
        "Línea de Empaque 1", "Línea de Empaque 2", "Calibradoras Ópticas", 
        "Túneles de Frío / Frio Industrial", "Calderas", "Compresores de Aire", 
        "Sistemas Contra Incendios", "Elevadores de Pallets", "Etiquetadoras Automáticas"
    ],
    "Transporte y Logística": [
        "Camiones de Transporte", "Autoelevadores (Montacargas)", "Zorras Eléctricas", 
        "Balanza de Piso", "Playón de Maniobras", "Sistema de Riego / Bombas"
    ],
    "Infraestructura General": [
        "Talleres de Mantenimiento (Herramientas)", "Iluminación Predial", 
        "Sistema de Cámaras de Seguridad", "Grupo Electrógeno Principal", "Oficinas y Sanitarios"
    ]
}

# Lista oficial de técnicos (36 técnicos)
TECNICOS_LISTA = [
    "Aguilar, Juan", "Alvarez, Carlos", "Benitez, Luis", "Caceres, Mario", 
    "Coronel, Jose", "Diaz, Roberto", "Fernandez, Miguel", "Gomez, Esteban", 
    "Gonzalez, Lucas", "Juarez, Martin", "Lopez, Javier", "Luna, Daniel", 
    "Martinez, Sergio", "Medina, Alejandro", "Molina, Pablo", "Moreno, Diego", 
    "Navarro, Cristian", "Ortiz, Fernando", "Perez, Gabriel", "Paz, Jorge", 
    "Ramirez, Adrian", "Rios, Marcelo", "Rodriguez, Walter", "Rojas, Hernán", 
    "Romero, Matias", "Ruiz, Victor", "Soria, Nicolas", "Suarez, Leonardo", 
    "Toledo, Federico", "Torres, Guillermo", "Valdez, Omar", "Vargas, Emanuel", 
    "Vera, Ricardo", "Villalba, Gonzalo", "Zarate, David", "Acosta, Emiliano"
]

EXCEL_FILE = "TAREAS REALIZADAS POR LOS TECNICOS.xlsx"
SHEET_NAME = "Tareas Realizadas"

def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        try:
            return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        except Exception:
            pass
    # Crear DataFrame vacío con las columnas exactas de tu Excel
    return pd.DataFrame(columns=[
        'Id', 'Hora de inicio', 'Fecha', 'Turno', 'Nombre de Colaborador', 
        'Evento Reportado', 'N° tarea Plan.', 'Hora Inicio', 'Hora Fin', 
        'Sector', 'Equipo', 'Descripción de Tarea', 'Ejecutantes', 
        'Comentarios Adicionales', 'Impacto de la Falla', 'Estado', 
        'Duración [min]', 'N° de p.', 'Día', 'Aprobación', 'Especialidad', 'Tipo de Trabajo'
    ])

def guardar_datos(df):
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=SHEET_NAME, index=False)

# Interfaz Principal
st.title("🔧 Sistema de Registro de Mantenimiento")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Carga de Tareas", "📊 Histórico y Control Visual"])

with tab1:
    st.subheader("Registro de Nueva Tarea Realizada")
    
    with st.form("form_mantenimiento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha del Trabajo", value=datetime.now())
            turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche", "Rotativo"])
            sector = st.selectbox("Sector", list(SECTORES_EQUIPOS.keys()))
            colaborador = st.selectbox("Nombre de Colaborador (Responsable de carga)", TECNICOS_LISTA)
            tipo_trabajo = st.selectbox("Tipo de Trabajo", ["Preventivo", "Correctivo", "Predictivo", "Mejora / Modificación"])
            
        with col2:
            equipos_disponibles = SECTORES_EQUIPOS.get(sector, [])
            equipo = st.selectbox("Equipo", equipos_disponibles)
            especialidad = st.selectbox("Especialidad", ["Mecánica", "Electricidad", "Instrumentación", "Lubricación", "General"])
            impacto = st.selectbox("Impacto de la Falla", ["Sin Parada", "Parada Parcial", "Parada Total"])
            estado = st.selectbox("Estado", ["Completado", "Pendiente de Repuestos", "En Seguimiento"])
            
        tecnicos_seleccionados = st.multiselect("Ejecutantes / Técnicos Asignados", TECNICOS_LISTA)
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            duracion = st.number_input("Duración [min]", min_value=0, value=60, step=15)
        with col_t2:
            n_tarea_plan = st.text_input("N° tarea Plan. (Opcional)")
        with col_t3:
            n_piezas = st.text_input("N° de p. / Repuestos (Opcional)")
            
        evento_reportado = st.text_input("Evento Reportado")
        descripcion = st.text_area("Descripción de Tarea")
        comentarios = st.text_input("Comentarios Adicionales (Opcional)")
        
        submitted = st.form_submit_button("💾 Guardar Registro en Excel")
        
        if submitted:
            if not tecnicos_seleccionados:
                st.error("Por favor, selecciona al menos un técnico en 'Ejecutantes'.")
            elif not descripcion.strip():
                st.error("Por favor, ingresa una descripción de la tarea.")
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
                    'Sector': sector,
                    'Equipo': equipo,
                    'Descripción de Tarea': descripcion,
                    'Ejecutantes': ", ".join(tecnicos_seleccionados),
                    'Comentarios Adicionales': comentarios,
                    'Impacto de la Falla': impacto,
                    'Estado': estado,
                    'Duración [min]': duracion,
                    'N° de p.': n_piezas,
                    'Día': fecha.strftime("%A"),
                    'Aprobación': "Pendiente",
                    'Especialidad': especialidad,
                    'Tipo de Trabajo': tipo_trabajo
                }])
                
                df_actual = pd.concat([df_actual, nueva_fila], ignore_index=True)
                guardar_datos(df_actual)
                
                st.success(f"¡Registro #{nuevo_id} guardado con éxito en el Excel!")

with tab2:
    st.subheader("Histórico de Tareas Registradas")
    df_actual = cargar_datos()
    
    if not df_actual.empty:
        st.dataframe(df_actual, use_container_width=True)
        
        with open(EXCEL_FILE, "rb") as f:
            st.download_button(
                label="📥 Descargar Archivo Excel Actualizado",
                data=f,
                file_name="TAREAS_REALIZADAS_POR_LOS_TECNICOS.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("Aún no hay registros en el archivo Excel.")