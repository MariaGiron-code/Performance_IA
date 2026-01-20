import streamlit as st
import requests  # Para consumir la API

def vista_nueva_prediccion():
    # Aplicar estilos CSS
    st.markdown('<div class="nueva-prediccion">', unsafe_allow_html=True)
    
    st.write("## Nueva Predicción de Riesgo Académico")
    st.info("Ingresa los datos del estudiante para calcular la probabilidad de deserción.")

    # Diccionarios de mapeo para categorías (simplificados para claridad)
    modo_solicitud_map = {
        "Primera opción": 1,
        "Segunda opción": 2,
        "Tercera opción": 3,
        "Cuarta opción": 4,
        "Quinta opción": 5,
        "Sexta opción": 6,
        "Séptima opción": 7,
        "Otra": 8,
        "Transferencia": 9
    }
    carrera_map = {
        "Tecnologías de Producción de Biocombustibles": 1,
        "Diseño de Animación y Multimedia": 2,
        "Servicio Social (Diurno)": 3,
        "Agronomía": 4,
        "Comunicación de Diseño": 5,
        "Enfermería": 6,
        "Gestión": 7,
        "Servicio Social": 8,
        "Turismo": 9,
        "Enfermería (Diurno)": 10,
        "Periodismo y Comunicación": 11,
        "Educación Básica": 12,
        "Gestión (Diurno)": 13,
        "Informática de Gestión": 14,
        "Ingeniería Civil": 15,
        "Turismo (Diurno)": 16,
        "Otra": 17
    }
    ocupacion_map = {
        "Estudiante": 1,
        "Empleo a tiempo completo": 2,
        "Empleo a tiempo parcial": 3,
        "Emprendedor": 4,
        "Desempleado": 5,
        "Trabajador independiente": 6,
        "Trabajador del hogar": 7,
        "Otra": 8,
        "Desconocido": 9
    }
    calificacion_map = {
        "Secundaria": 1,
        "Bachillerato": 2,
        "Licenciatura": 3,
        "Maestría": 4,
        "Doctorado": 5,
        "Otra": 6
    }

    with st.form("form_prediccion"):
        
        # Campo para ingresar el nombre del estudiante, requerido para el historial
        nombre_estudiante = st.text_input("Nombre del estudiante", help="Ingresa el nombre del estudiante para registrar la predicción")
        
        # Descripción detallada del ajuste del umbral
        
        st.write("### Ajuste del Umbral de Riesgo")
        st.info("""
        El umbral de deserción determina a partir de qué probabilidad el sistema clasifica a un estudiante como 'Desertor' o 'No Desertor'. 
        - **Umbral bajo (ej. 0.3)**: Clasifica más estudiantes como 'Desertor', lo que aumenta la detección de riesgos potenciales, pero puede generar más alertas falsas (falsos positivos), es decir, estudiantes que no desertarán pero son marcados como de riesgo.
        - **Umbral alto (ej. 0.7)**: Clasifica menos estudiantes como 'Desertor', siendo más conservador, lo que reduce las alertas falsas pero puede pasar por alto riesgos reales (falsos negativos).
        Ajusta este valor según tu tolerancia al riesgo: si prefieres identificar más estudiantes en riesgo (aunque algunos no lo estén), baja el umbral; si quieres ser más preciso, súbelo.
        """)
        
        # Slider para ajustar el umbral de clasificación de deserción
        umbral = st.slider("Umbral de riesgo de deserción", min_value=0.0, max_value=1.0, value=0.5, step=0.01, help="Ajusta el umbral de probabilidad para clasificar como 'Desertor'. Valores bajos detectan más riesgos, altos son más conservadores.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Socio-demográfica", "Académica", "Entorno"])
        
        with tab1:
            st.subheader("Datos Socio-demográficos")
            modo_solicitud_sel = st.selectbox("Modo de solicitud", list(modo_solicitud_map.keys()), help="Indica cómo el estudiante aplicó a la universidad (primera fase general, decreto específico, etc.)")
            orden_solicitud = st.number_input("Orden de solicitud", min_value=0, value=1, help="Orden de prioridad en las aplicaciones del estudiante (1=primera, 2=segunda, etc.)")
            carrera_sel = st.selectbox("Carrera", list(carrera_map.keys()), help="Carrera universitaria a la que aplicó el estudiante")
            asistencia_diurna_nocturna = st.selectbox("Asistencia diurna/nocturna", ["Diurna", "Nocturna"], help="Si el estudiante asiste a clases diurnas o nocturnas")
            calificacion_previa_sel = st.selectbox("Calificación previa", list(calificacion_map.keys()), help="Nivel educativo más alto alcanzado antes de matricularse")
            calificacion_madre_sel = st.selectbox("Calificación madre", list(calificacion_map.keys()), help="Nivel educativo de la madre del estudiante")
            calificacion_padre_sel = st.selectbox("Calificación padre", list(calificacion_map.keys()), help="Nivel educativo del padre del estudiante")
            ocupacion_madre_sel = st.selectbox("Ocupación madre", list(ocupacion_map.keys()), help="Ocupación laboral de la madre del estudiante")
            ocupacion_padre_sel = st.selectbox("Ocupación padre", list(ocupacion_map.keys()), help="Ocupación laboral del padre del estudiante")
            desplazado = st.selectbox("Desplazado", ["Sí", "No"], help="Si el estudiante vive lejos de su hogar familiar")
            deudor = st.selectbox("Deudor", ["Sí", "No"], help="Si el estudiante tiene deudas pendientes")
            pagos_al_dia = st.selectbox("Pagos al día", ["Sí", "No"], help="Si el estudiante paga sus cuotas puntualmente")
            genero = st.selectbox("Género", ["Masculino", "Femenino"], help="Género del estudiante")
            becado = st.selectbox("Becado", ["Sí", "No"], help="Si el estudiante recibe beca financiera")
            edad_al_matricularse = st.number_input("Edad al matricularse", min_value=15, max_value=100, value=18, help="Edad del estudiante al momento de matricularse")
        
        with tab2:
            st.subheader("Datos Académicos")
            unidades_1er_sem_matriculadas = st.number_input("Número de créditos matriculados en 1er Semestre", min_value=0, value=6, help="Número de unidades curriculares inscritas al inicio del primer semestre")
            unidades_1er_sem_evaluaciones = st.number_input("Número de créditos evaluados en 1er Semestre", min_value=0, value=6, help="Número de unidades que fueron evaluadas (examinadas o calificadas) en el primer semestre")
            unidades_1er_sem_aprobadas = st.number_input("Número de créditos aprobados en 1er Semestre", min_value=0, value=6, help="Número de unidades que el estudiante aprobó (pasó) en el primer semestre")
            unidades_1er_sem_nota = st.number_input("Nota promedio en 1er Semestre", min_value=0.0, max_value=20.0, value=12.0, help="Nota promedio obtenida en las unidades del primer semestre (escala 0-20)")
            unidades_2do_sem_matriculadas = st.number_input("Número de créditos matriculados en 2do Semestre", min_value=0, value=6, help="Número de unidades curriculares inscritas al inicio del segundo semestre")
            unidades_2do_sem_evaluaciones = st.number_input("Número de créditos evaluados en 2do Semestre", min_value=0, value=6, help="Número de unidades que fueron evaluadas en el segundo semestre")
            unidades_2do_sem_aprobadas = st.number_input("Número de créditos aprobados en 2do Semestre", min_value=0, value=6, help="Número de unidades que el estudiante aprobó en el segundo semestre")
            unidades_2do_sem_nota = st.number_input("Nota promedio en 2do Semestre", min_value=0.0, max_value=20.0, value=12.0, help="Nota promedio obtenida en las unidades del segundo semestre (escala 0-20)")
        
        with tab3:
            st.subheader("Datos de Entorno")
            tasa_desempleo = st.number_input("Tasa de desempleo (%)", min_value=0.0, max_value=100.0, value=10.0, help="Tasa de desempleo en la región del estudiante")
            tasa_inflacion = st.number_input("Tasa de inflación (%)", min_value=0.0, max_value=50.0, value=2.0, help="Tasa de inflación económica en la región")
            pib = st.number_input("PIB (en miles)", min_value=0.0, value=50000.0, help="Producto Interno Bruto per cápita en la región (en miles de unidades monetarias)")
        
        submitted = st.form_submit_button("Ejecutar Análisis de riesgo académico")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            if not nombre_estudiante.strip():
                st.error("Debes ingresar el nombre del estudiante.")
                return
            
            # Validaciones básicas
            errores = []
            if unidades_1er_sem_aprobadas > unidades_1er_sem_matriculadas:
                errores.append("Número de créditos aprobados en 1er Semestre no puede exceder matriculados.")
            if unidades_1er_sem_evaluaciones > unidades_1er_sem_matriculadas:
                errores.append("Número de créditos evaluados en 1er Semestre no puede exceder matriculados.")
            if unidades_2do_sem_aprobadas > unidades_2do_sem_matriculadas:
                errores.append("Número de créditos aprobados en 2do Semestre no puede exceder matriculados.")
            if unidades_2do_sem_evaluaciones > unidades_2do_sem_matriculadas:
                errores.append("Número de créditos evaluados en 2do Semestre no puede exceder matriculados.")
            if errores:
                for error in errores:
                    st.error(error)
                return
            
            # Mapeo a valores numéricos
            datos = {
                'Modo_solicitud': modo_solicitud_map[modo_solicitud_sel],
                'Orden_solicitud': orden_solicitud,
                'Carrera': carrera_map[carrera_sel],
                'Asistencia_diurna_nocturna': 1 if asistencia_diurna_nocturna == "Diurna" else 0,
                'Calificacion_previa': calificacion_map[calificacion_previa_sel],
                'Calificacion_madre': calificacion_map[calificacion_madre_sel],
                'Calificacion_padre': calificacion_map[calificacion_padre_sel],
                'Ocupacion_madre': ocupacion_map[ocupacion_madre_sel],
                'Ocupacion_padre': ocupacion_map[ocupacion_padre_sel],
                'Desplazado': 1 if desplazado == "Sí" else 0,
                'Deudor': 1 if deudor == "Sí" else 0,
                'Pagos_al_dia': 1 if pagos_al_dia == "Sí" else 0,
                'Genero': 1 if genero == "Masculino" else 0,
                'Becado': 1 if becado == "Sí" else 0,
                'Edad_al_matricularse': edad_al_matricularse,
                'Unidades_1er_sem_matriculadas': unidades_1er_sem_matriculadas,
                'Unidades_1er_sem_evaluaciones': unidades_1er_sem_evaluaciones,
                'Unidades_1er_sem_aprobadas': unidades_1er_sem_aprobadas,
                'Unidades_1er_sem_nota': unidades_1er_sem_nota,
                'Unidades_2do_sem_matriculadas': unidades_2do_sem_matriculadas,
                'Unidades_2do_sem_evaluaciones': unidades_2do_sem_evaluaciones,
                'Unidades_2do_sem_aprobadas': unidades_2do_sem_aprobadas,
                'Unidades_2do_sem_nota': unidades_2do_sem_nota,
                'Tasa_desempleo': tasa_desempleo,
                'Tasa_inflacion': tasa_inflacion,
                'PIB': pib
            }
            
            # Integración con la API de FastAPI
            # Preparar payload con todos los datos requeridos
            payload = {
                "nombre_estudiante": nombre_estudiante,
                "umbral": umbral,
                "Modo_solicitud": datos['Modo_solicitud'],
                "Orden_solicitud": datos['Orden_solicitud'],
                "Carrera": datos['Carrera'],
                "Asistencia_diurna_nocturna": datos['Asistencia_diurna_nocturna'],
                "Calificacion_previa": datos['Calificacion_previa'],
                "Calificacion_madre": datos['Calificacion_madre'],
                "Calificacion_padre": datos['Calificacion_padre'],
                "Ocupacion_madre": datos['Ocupacion_madre'],
                "Ocupacion_padre": datos['Ocupacion_padre'],
                "Desplazado": datos['Desplazado'],
                "Deudor": datos['Deudor'],
                "Pagos_al_dia": datos['Pagos_al_dia'],
                "Genero": datos['Genero'],
                "Becado": datos['Becado'],
                "Edad_al_matricularse": datos['Edad_al_matricularse'],
                "Unidades_1er_sem_matriculadas": datos['Unidades_1er_sem_matriculadas'],
                "Unidades_1er_sem_evaluaciones": datos['Unidades_1er_sem_evaluaciones'],
                "Unidades_1er_sem_aprobadas": datos['Unidades_1er_sem_aprobadas'],
                "Unidades_1er_sem_nota": datos['Unidades_1er_sem_nota'],
                "Unidades_2do_sem_matriculadas": datos['Unidades_2do_sem_matriculadas'],
                "Unidades_2do_sem_evaluaciones": datos['Unidades_2do_sem_evaluaciones'],
                "Unidades_2do_sem_aprobadas": datos['Unidades_2do_sem_aprobadas'],
                "Unidades_2do_sem_nota": datos['Unidades_2do_sem_nota'],
                "Tasa_desempleo": datos['Tasa_desempleo'],
                "Tasa_inflacion": datos['Tasa_inflacion'],
                "PIB": datos['PIB']
            }
            
            try:
                # Hacer request a la API usando credenciales del usuario logueado
                user_email = st.session_state.user_info["email"]
                user_password = st.session_state.user_password
                response = requests.post("http://localhost:8000/predict", json=payload, auth=(user_email, user_password))
                if response.status_code == 200:
                    result = response.json()
                    probabilidad = result["probability"]
                    resultado = result["prediction"]
                else:
                    st.error(f"Error en la API: {response.status_code} - {response.text}")
                    return
            except requests.exceptions.RequestException as e:
                st.error(f"Error conectando a la API: {e}")
                return
            
            if probabilidad is not None:
                st.success(f"Probabilidad de deserción: {probabilidad:.2%}")
                st.info(f"Resultado con umbral {umbral:.2f}: {resultado}")
                
              
                
                # Gauge visual actualizado con el umbral ajustado
                import plotly.graph_objects as go
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probabilidad * 100,
                    title={'text': "Riesgo de Deserción"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [
                               {'range': [0, umbral*100], 'color': "green"},
                               {'range': [umbral*100, 100], 'color': "red"}]}
                ))
                st.plotly_chart(fig)
            else:
                st.error("Error en la predicción. Verifica los datos.")
    
    st.markdown('</div>', unsafe_allow_html=True)