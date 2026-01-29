from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Configuración de Rutas
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "entrenamiento.csv"
MODEL_PATH = BASE_DIR / "scripts" / "model" / "modelo_random_forest.pkl"


# Funciones con Caché (Mejora de Rendimiento)
@st.cache_data(show_spinner="Cargando dataset de entrenamiento...")
def cargar_datos():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos en: {DATA_PATH}")
    return pd.read_csv(DATA_PATH)


@st.cache_resource(show_spinner="Cargando modelo de IA...")
def cargar_modelo():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo del modelo en: {MODEL_PATH}"
        )
    return joblib.load(MODEL_PATH)


# Se genera la interfaz visual
def vista_metricas_modelo():
    st.markdown("## 📊 Métricas del Modelo")
    st.info(
        "Rendimiento del modelo Random Forest entrenado para predecir deserción académica."
    )

    try:
        # 1. Carga optimizada de recursos
        df = cargar_datos()
        modelo = cargar_modelo()

        # 2. Preparación de datos
        objetivo = "Es_Desertor"

        # Validación básica de columnas
        if objetivo not in df.columns:
            st.error(f"El dataset no contiene la columna objetivo '{objetivo}'")
            return

        X = df.drop(columns=[objetivo])
        y = df[objetivo]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # 3. Predicciones
        y_pred = modelo.predict(X_test)

        # 4. Cálculo de Métricas
        accuracy = accuracy_score(y_test, y_pred)
        reporte = classification_report(y_test, y_pred, output_dict=True)

        # Extracción de métricas para la clase positiva (1: Desertor)
        metricas_clase_1 = reporte.get("1", {})
        precision = metricas_clase_1.get("precision", 0)
        recall = metricas_clase_1.get("recall", 0)
        f1_score = metricas_clase_1.get("f1-score", 0)

        # Explicación desplegable para ahorrar espacio visual
        with st.expander("ℹ¿Qué significan estas métricas?"):
            st.markdown("""
            - **Exactitud (Accuracy):** % global de aciertos.
            - **Precisión:** De los que la IA dijo "Desertará", ¿cuántos realmente lo hicieron?
            - **Sensibilidad (Recall):** De todos los que realmente desertaron, ¿a cuántos detectó la IA?
            - **F1-Score:** Equilibrio entre Precisión y Sensibilidad.
            """)

        # 5. Tarjetas de Métricas (KPIs)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Exactitud", f"{accuracy:.1%}", help="Aciertos totales")
        col2.metric(
            "Precisión", f"{precision:.1%}", help="Calidad de la alarma de deserción"
        )
        col3.metric("Sensibilidad", f"{recall:.1%}", help="Capacidad de detección")
        col4.metric("F1-Score", f"{f1_score:.1%}", help="Balance general")

        st.markdown("---")

        # 6. Gráficos
        col_graf1, col_graf2 = st.columns([1, 1])

        with col_graf1:
            st.markdown("### 🔍 Matriz de Confusión")
            fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(
                cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                ax=ax_cm,
                xticklabels=["No Desertor", "Desertor"],
                yticklabels=["No Desertor", "Desertor"],
                cbar=False,
            )
            plt.ylabel("Realidad")
            plt.xlabel("Predicción IA")
            st.pyplot(fig_cm)
            plt.close(fig_cm)

        with col_graf2:
            st.markdown("### Importancia de Variables")
            try:
                if hasattr(modelo, "feature_importances_"):
                    importancias = modelo.feature_importances_
                    nombres = (
                        modelo.feature_names_in_
                        if hasattr(modelo, "feature_names_in_")
                        else X.columns
                    )

                    df_imp = pd.DataFrame(
                        {"Variable": nombres, "Importancia": importancias}
                    )
                    df_imp = df_imp.sort_values("Importancia", ascending=False).head(10)

                    fig_imp, ax_imp = plt.subplots(figsize=(5, 4))
                    sns.barplot(
                        x="Importancia",
                        y="Variable",
                        hue="Variable",
                        data=df_imp,
                        ax=ax_imp,
                        palette="viridis",
                        legend=False,
                    )
                    plt.title("Top 10 Factores de Riesgo")
                    st.pyplot(fig_imp)
                    plt.close(fig_imp)
                else:
                    st.warning(
                        "Este modelo no soporta visualización de importancia de características."
                    )
            except Exception as e:
                st.warning(f"No se pudieron cargar las importancias: {e}")

        # 7. Tabla detallada
        with st.expander("Ver reporte técnico detallado"):
            df_reporte = pd.DataFrame(reporte).T
            st.dataframe(df_reporte.style.format("{:.4f}"))

    except FileNotFoundError as e:
        st.error(f"Error de archivo: {e}")
        st.info(
            "Verifica que los archivos 'entrenamiento.csv' y 'modelo_a.pkl' estén en las carpetas 'data/processed' y 'model' respectivamente."
        )
    except Exception as e:
        st.error(f"Error inesperado al generar métricas: {e}")
