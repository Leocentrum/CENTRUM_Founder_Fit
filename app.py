Python 3.11.3 (tags/v3.11.3:f3909b8, Apr  4 2023, 23:49:59) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
import pandas as pd
import json
import os

# Configuración de la página
st.set_page_config(page_title="CENTRUM Founder Fit", layout="wide")

# Archivo para "simular" base de datos local (en un despliegue real, usarías una DB)
DB_FILE = 'respuestas_equipo.json'

def cargar_datos():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def guardar_datos(nuevos_datos):
    datos = cargar_datos()
    datos.append(nuevos_datos)
    with open(DB_FILE, 'w') as f:
        json.dump(datos, f)

# --- INTERFAZ ---
st.title("🧩 MBA Entrepreneurship: Founder-Market Fit Finder")
st.markdown("Herramienta de convergencia de perfiles para generación de Startups.")

# Sidebar para navegación
menu = st.sidebar.selectbox("Seleccionar Perfil", ["Ingresar Datos (Socio)", "Administrador (Solo Admin)"])

# --- VISTA USUARIO (SOCIOS) ---
if menu == "Ingresar Datos (Socio)":
    st.header("Cuestionario de Profundidad")
    st.info("Por favor, responde con total honestidad y detalle. Esta información será procesada por IA para encontrar nuestra idea ganadora.")
    
    with st.form("cuestionario_form"):
        nombre = st.text_input("Tu Nombre Completo")
        
        st.subheader("1. Effectuation: Quién eres y Qué sabes")
        trayectoria = st.text_area("Describe hitos clave donde resolviste problemas complejos o creaste algo de la nada:", height=100)
        conocimiento_unico = st.text_area("¿En qué temas eres un referente para tus conocidos? (Habilidades duras y blandas):", height=100)
        contactos_clave = st.text_area("Lista 3 industrias/empresas donde tienes contactos fuertes que nos contestarían el teléfono:", height=100)
        
        st.subheader("2. Ventaja Injusta (MILES)")
        insight_mercado = st.text_area("¿Qué ineficiencia o 'secreto' has descubierto en tu experiencia laboral que otros ignoran?", height=100)
        recursos_accesibles = st.text_area("¿A qué recursos 'raros' tienes acceso? (Capital, Licencias, Espacios, Reputación):", height=100)
        
        st.subheader("3. El Concepto del Erizo & Aspiraciones")
        pasion = st.text_area("¿Sobre qué temas podrías leer/trabajar horas sin aburrirte?", height=100)
        tareas_odiadas = st.text_area("¿Qué tareas operativas odias y cuáles no te molestan?", height=100)
        
        st.subheader("4. Propuestas Iniciales")
        propuesta_1 = st.text_input("Idea de Negocio 1 (Título y breve descripción)")
        propuesta_2 = st.text_input("Idea de Negocio 2 (Título y breve descripción)")
        propuesta_3 = st.text_input("Idea de Negocio 3 (Título y breve descripción)")
        
        submitted = st.form_submit_button("Enviar mis respuestas")
        
        if submitted:
            if nombre:
                datos_usuario = {
                    "Nombre": nombre,
                    "Trayectoria": trayectoria,
                    "Conocimiento": conocimiento_unico,
                    "Contactos": contactos_clave,
                    "Insight": insight_mercado,
                    "Recursos": recursos_accesibles,
                    "Pasion": pasion,
                    "Tareas": tareas_odiadas,
                    "Ideas": [propuesta_1, propuesta_2, propuesta_3]
                }
                guardar_datos(datos_usuario)
                st.success(f"¡Gracias {nombre}! Tus datos han sido registrados exitosamente.")
            else:
                st.error("Por favor, ingresa tu nombre.")

# --- VISTA ADMINISTRADOR ---
elif menu == "Administrador (Solo Admin)":
    password = st.sidebar.text_input("Contraseña de Administrador", type="password")
    
    if password == "PUCP":
        st.header("Panel de Control - Administrador")
        datos = cargar_datos()
        
        if datos:
            df = pd.DataFrame(datos)
            
            st.subheader("1. Vista de Datos Consolidados")
            st.dataframe(df)
            
            st.subheader("2. Imprimir/Exportar Datos Individuales")
            socio_sel = st.selectbox("Seleccionar Socio para ver detalle", [d['Nombre'] for d in datos])
            
            socio_data = next((item for item in datos if item["Nombre"] == socio_sel), None)
            if socio_data:
                st.markdown("---")
                st.markdown(f"### Perfil de: {socio_data['Nombre']}")
                for k, v in socio_data.items():
...                     if k != "Nombre":
...                         st.markdown(f"**{k}:** {v}")
...                 st.markdown("---")
...             
...             st.subheader("3. PROCESAMIENTO CON GEMINI AI")
...             st.markdown("Copia el siguiente texto y pégalo en tu chat con Gemini para obtener el análisis:")
...             
...             # Generador de Prompt Automático
...             prompt_texto = "Actúa como consultor experto. Aquí tienes los perfiles detallados de 4 socios para un emprendimiento. Analiza la convergencia de habilidades (Effectuation), ventajas injustas y pasiones. \n\n"
...             for d in datos:
...                 prompt_texto += f"--- SOCIO: {d['Nombre']} ---\n"
...                 prompt_texto += f"Perfil y Habilidades: {d['Trayectoria']} | {d['Conocimiento']}\n"
...                 prompt_texto += f"Red de Contactos: {d['Contactos']}\n"
...                 prompt_texto += f"Insights de Mercado: {d['Insight']} | Recursos: {d['Recursos']}\n"
...                 prompt_texto += f"Intereses/Pasiones: {d['Pasion']} | Tareas: {d['Tareas']}\n"
...                 prompt_texto += f"Ideas Propuestas: {d['Ideas']}\n\n"
...             
...             prompt_texto += "TAREA: Basado en esta data, 1) Identifica patrones de convergencia, 2) Genera 3 Ideas de Negocio sólidas que combinen los activos de los 4, 3) Desarrolla el Modelo de Negocio y Modelo de Ingresos para cada una."
...             
...             st.code(prompt_texto, language='text')
...             
...         else:
...             st.warning("Aún no hay datos registrados.")
...             
...     elif password:
