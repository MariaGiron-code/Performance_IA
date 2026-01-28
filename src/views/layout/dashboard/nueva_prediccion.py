import os

import plotly.graph_objects as go
import requests
import streamlit as st
from dotenv import load_dotenv

from src.database import guardar_prediccion

load_dotenv()
API_BASE_URL = os.getenv("URL_API_BACKEND", "http://localhost:8000")


def vista_nueva_prediccion():
    st.markdown('<div class="nueva-prediccion">', unsafe_allow_html=True)

    col_header, col_logo = st.columns([5, 1])
    with col_header:
        st.write("## Nueva Predicción")
        st.info("Ingresa los datos del estudiante para calcular su riesgo académico.")

    # DICCIONARIOS DE MAPEO
    modo_solicitud_map = {
        "Primera opción": 1,
        "Segunda opción": 2,
        "Tercera opción": 3,
        "Cuarta opción": 4,
        "Quinta opción": 5,
        "Sexta opción": 6,
        "Séptima opción": 7,
        "Otra": 8,
        "Transferencia": 9,
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
        "Otra": 17,
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
        "Desconocido": 9,
    }
    calificacion_map = {
        "Secundaria": 1,
        "Bachillerato": 2,
        "Licenciatura": 3,
        "Maestría": 4,
        "Doctorado": 5,
        "Otra": 6,
    }

    #  FORMULARIO
    with st.form("form_prediccion"):

        # Datos Clave
        c1, c2 = st.columns([2, 1])
        with c1:
            nombre_estudiante = st.text_input(
                "Nombre del estudiante", placeholder="Ej. Ana García"
            )
        with c2:
            umbral = st.slider(
                "Sensibilidad del Modelo",
                0.0,
                1.0,
                0.5,
                0.05,
                help="A mayor valor, el sistema es menos alarmista. A menor valor, detecta más riesgo.",
            )

        # Pestañas de Datos
        tab1, tab2, tab3 = st.tabs(
            ["👤 Socio-demográfica", "🎓 Académica", "🌍 Entorno"]
        )

        with tab1:
            c_soc1, c_soc2 = st.columns(2)
            with c_soc1:
                modo_solicitud_sel = st.selectbox(
                    "Modo solicitud", list(modo_solicitud_map.keys())
                )
                orden_solicitud = st.number_input("Orden solicitud", 1, 10, 1)
                carrera_sel = st.selectbox("Carrera", list(carrera_map.keys()))
                genero = st.selectbox("Género", ["Masculino", "Femenino"])
                edad_al_matricularse = st.number_input(
                    "Edad al matricularse", 15, 80, 18
                )
                desplazado = st.selectbox(
                    "¿Es desplazado?", ["No", "Sí"]
                )  # Ajustado orden lógico

            with c_soc2:
                calificacion_previa_sel = st.selectbox(
                    "Estudios previos", list(calificacion_map.keys())
                )
                calificacion_madre_sel = st.selectbox(
                    "Nivel estudios Madre", list(calificacion_map.keys())
                )
                ocupacion_madre_sel = st.selectbox(
                    "Ocupación Madre", list(ocupacion_map.keys())
                )
                calificacion_padre_sel = st.selectbox(
                    "Nivel estudios Padre", list(calificacion_map.keys())
                )
                ocupacion_padre_sel = st.selectbox(
                    "Ocupación Padre", list(ocupacion_map.keys())
                )
                becado = st.selectbox("¿Tiene Beca?", ["No", "Sí"])
                deudor = st.selectbox("¿Tiene Deudas?", ["No", "Sí"])
                pagos_al_dia = st.selectbox("¿Pagos al día?", ["Sí", "No"])
                asistencia_diurna_nocturna = st.selectbox(
                    "Horario", ["Diurna", "Nocturna"]
                )

        with tab2:
            st.caption("Ingresa el rendimiento de los primeros dos semestres")
            c_aca1, c_aca2 = st.columns(2)
            with c_aca1:
                st.markdown("##### 1er Semestre")
                u1_mat = st.number_input("Créditos Matriculados (1er)", 0, 50, 6)
                u1_eval = st.number_input("Créditos Evaluados (1er)", 0, 50, 6)
                u1_aprob = st.number_input("Créditos Aprobados (1er)", 0, 50, 6)
                u1_nota = st.number_input("Promedio (1er)", 0.0, 20.0, 12.0)
            with c_aca2:
                st.markdown("##### 2do Semestre")
                u2_mat = st.number_input("Créditos Matriculados (2do)", 0, 50, 6)
                u2_eval = st.number_input("Créditos Evaluados (2do)", 0, 50, 6)
                u2_aprob = st.number_input("Créditos Aprobados (2do)", 0, 50, 6)
                u2_nota = st.number_input("Promedio (2do)", 0.0, 20.0, 12.0)

        with tab3:
            c_eco1, c_eco2, c_eco3 = st.columns(3)
            with c_eco1:
                tasa_desempleo = st.number_input(
                    "Desempleo Regional (%)", 0.0, 50.0, 10.0
                )
            with c_eco2:
                tasa_inflacion = st.number_input("Inflación (%)", 0.0, 100.0, 2.0)
            with c_eco3:
                pib = st.number_input("PIB Regional (k)", 0.0, 200000.0, 50000.0)

        st.markdown("---")
        submitted = st.form_submit_button(
            "🔍 Analizar Riesgo", use_container_width=True
        )

    # --- LÓGICA DE ENVÍO ---
    if submitted:
        if not nombre_estudiante.strip():
            st.error("⚠️ El nombre del estudiante es obligatorio.")
            return

        # 1. Validación de lógica académica
        errores = []
        if u1_aprob > u1_mat:
            errores.append("1er Sem: Aprobados no puede ser mayor a Matriculados")
        if u2_aprob > u2_mat:
            errores.append("2do Sem: Aprobados no puede ser mayor a Matriculados")

        if errores:
            for e in errores:
                st.error(f"❌ {e}")
            return

        # 2. Construcción del Payload
        # Convertimos Si/No a 1/0 y mapeamos los selects
        payload = {
            "nombre_estudiante": nombre_estudiante,
            "umbral": umbral,
            # Mapeos directos
            "Modo_solicitud": modo_solicitud_map[modo_solicitud_sel],
            "Orden_solicitud": orden_solicitud,
            "Carrera": carrera_map[carrera_sel],
            "Calificacion_previa": calificacion_map[calificacion_previa_sel],
            "Calificacion_madre": calificacion_map[calificacion_madre_sel],
            "Calificacion_padre": calificacion_map[calificacion_padre_sel],
            "Ocupacion_madre": ocupacion_map[ocupacion_madre_sel],
            "Ocupacion_padre": ocupacion_map[ocupacion_padre_sel],
            # Académicos
            "Unidades_1er_sem_matriculadas": u1_mat,
            "Unidades_1er_sem_evaluaciones": u1_eval,
            "Unidades_1er_sem_aprobadas": u1_aprob,
            "Unidades_1er_sem_nota": u1_nota,
            "Unidades_2do_sem_matriculadas": u2_mat,
            "Unidades_2do_sem_evaluaciones": u2_eval,
            "Unidades_2do_sem_aprobadas": u2_aprob,
            "Unidades_2do_sem_nota": u2_nota,
            # Binarios
            "Asistencia_diurna_nocturna": (
                1 if asistencia_diurna_nocturna == "Diurna" else 0
            ),
            "Desplazado": 1 if desplazado == "Sí" else 0,
            "Deudor": 1 if deudor == "Sí" else 0,
            "Pagos_al_dia": 1 if pagos_al_dia == "Sí" else 0,
            "Genero": 1 if genero == "Masculino" else 0,
            "Becado": 1 if becado == "Sí" else 0,
            # Numéricos simples
            "Edad_al_matricularse": edad_al_matricularse,
            "Tasa_desempleo": tasa_desempleo,
            "Tasa_inflacion": tasa_inflacion,
            "PIB": pib,
        }

        # 3. Consumo de API
        with st.spinner("🧠 Consultando a EduGuard AI..."):  # type: ignore
            try:
                user_email = st.session_state.user_info.get("email")
                user_password = st.session_state.get("user_password")

                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    json=payload,
                    auth=(user_email, user_password),
                    timeout=10,
                )

                if response.status_code == 200:
                    data_res = response.json()
                    probabilidad = data_res["probability"]
                    resultado_ia = data_res["prediction"]
                    explicaciones = data_res.get("explanations", {})

                    # 4. GUARDADO EN BASE DE DATOS LOCAL (INTEGRACIÓN)
                    exito_guardado = False
                    if "user_info" in st.session_state:
                        exito_guardado = guardar_prediccion(
                            usuario_id=st.session_state.user_info["id"],
                            nombre_est=nombre_estudiante.strip(),
                            datos_dict=payload,
                            prob=probabilidad,
                            resultado=resultado_ia,
                            umbral=umbral,
                            explicaciones=explicaciones,
                        )

                    # --- VISUALIZACIÓN DE RESULTADOS ---
                    st.divider()
                    col_res, col_graf = st.columns([1, 2])

                    with col_res:
                        st.subheader("Diagnóstico")
                        if resultado_ia == "Desertor":
                            st.error(f"⚠️ **RIESGO ALTO**")
                        else:
                            st.success(f"✅ **BAJO RIESGO**")

                        st.metric("Probabilidad de Deserción", f"{probabilidad:.2%}")

                        if exito_guardado:
                            st.toast("Predicción guardada en historial", icon="💾")
                        else:
                            st.warning(
                                "Resultado mostrado pero no guardado en historial."
                            )

                    with col_graf:
                        # Gráfico Gauge
                        fig = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=probabilidad * 100,
                                domain={"x": [0, 1], "y": [0, 1]},
                                title={"text": "Nivel de Riesgo"},
                                gauge={
                                    "axis": {"range": [0, 100]},
                                    "bar": {"color": "#1F2937"},
                                    "steps": [
                                        {
                                            "range": [0, umbral * 100],
                                            "color": "#10B981",
                                        },  # Verde
                                        {
                                            "range": [umbral * 100, 100],
                                            "color": "#EF4444",
                                        },  # Rojo
                                    ],
                                    "threshold": {
                                        "line": {"color": "black", "width": 4},
                                        "thickness": 0.75,
                                        "value": probabilidad * 100,
                                    },
                                },
                            )
                        )
                        fig.update_layout(
                            height=250, margin=dict(l=20, r=20, t=30, b=20)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # Gráfico de Factores (SHAP/Explicaciones)
                    if explicaciones:
                        st.subheader("🔍 Factores Determinantes")
                        st.caption(
                            "Variables que más empujaron la decisión del modelo (Positivo = Aumenta Riesgo)"
                        )

                        # Ordenar y filtrar top 5
                        sorted_items = sorted(
                            explicaciones.items(), key=lambda x: abs(x[1]), reverse=True
                        )[:5]
                        vars_n = [k for k, v in sorted_items]
                        vars_v = [v for k, v in sorted_items]

                        colors = ["#EF4444" if v > 0 else "#10B981" for v in vars_v]

                        fig_bar = go.Figure(
                            go.Bar(
                                x=vars_v,
                                y=vars_n,
                                orientation="h",
                                marker=dict(color=colors),
                            )
                        )
                        fig_bar.update_layout(
                            xaxis_title="Impacto en la probabilidad",
                            height=300,
                            margin=dict(l=0, r=0, t=0, b=0),
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

                else:
                    st.error(f"Error del servidor: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión con el servicio de IA: {e}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
