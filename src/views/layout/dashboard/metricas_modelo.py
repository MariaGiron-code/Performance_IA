import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split


def vista_metricas_modelo():
    """
    Genera la interfaz de usuario para visualizar las métricas del modelo de predicción de deserción académica.
    
    Esta función realiza las siguientes acciones:
    1. Muestra un encabezado y descripción general de la sección
    2. Carga el dataset procesado y el modelo entrenado
    3. Prepara los datos para evaluación
    4. Calcula métricas de rendimiento del modelo
    5. Visualiza las métricas en tarjetas interactivas
    6. Genera una matriz de confusión para analizar errores de clasificación
    7. Muestra un reporte detallado de clasificación
    8. Visualiza la importancia de las características para el modelo
    9. Maneja errores de carga de datos o modelo
    
    Raises:
        Exception: Si ocurre un error al cargar datos o modelo
    """
    st.write("## Métricas del Modelo")
    st.info("Métricas de rendimiento del modelo Random Forest entrenado para predecir deserción académica.")
    
    # Cargar datos y modelo
    try:
        # Cargar dataset procesado (datos de entrenamiento etiquetados)
        df = pd.read_csv('data/processed/entrenamiento.csv')
        
        # Cargar modelo entrenado (Random Forest)
        modelo = joblib.load('model/modelo_a.pkl')
        
        # Preparar datos para evaluación
        objetivo = 'Es_Desertor'  # Nombre de la variable objetivo (0: No Desertor, 1: Desertor)
        x = df.drop(columns=[objetivo])  # Variables predictoras
        y = df[objetivo]  # Variable objetivo
        
        # Dividir datos en conjuntos de entrenamiento y prueba (mismo split que en el notebook)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, 
            test_size=0.2,  # 20% de los datos para prueba
            random_state=42,  # Semilla aleatoria para reproducibilidad
            stratify=y  # Mantener proporción de clases en ambos conjuntos
        )
        
        # Realizar predicciones con el modelo
        y_pred = modelo.predict(x_test)
        
        # Calcular métricas principales de rendimiento
        accuracy = accuracy_score(y_test, y_pred)  # Exactitud general
        reporte = classification_report(y_test, y_pred, output_dict=True)
        precision = reporte['1']['precision']  # Precisión para la clase "Desertor"
        recall = reporte['1']['recall']  # Sensibilidad para la clase "Desertor"
        f1_score = reporte['1']['f1-score']  # Puntuación F1 para la clase "Desertor"

        st.info("""
        **Explicación de las métricas:**
        - **Exactitud (Accuracy):** Porcentaje total de predicciones correctas (tanto de desertores como no desertores).
        - **Precisión:** Probabilidad de que un estudiante etiquetado como "Desertor" realmente sea un desertor (evita falsos positivos).
        - **Sensibilidad (Recall):** Probabilidad de identificar correctamente a los estudiantes que realmente son desertores (evita falsos negativos).
        - **Puntuación F1:** Balance entre precisión y sensibilidad; ideal para datos desbalanceados (como este caso de deserción académica).
        """)
        
        # Mostrar métricas en tarjetas interactivas
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Exactitud (Accuracy)", f"{accuracy:.2%}")
        col2.metric("Precisión", f"{precision:.2%}")
        col3.metric("Sensibilidad (Recall)", f"{recall:.2%}")
        col4.metric("Puntuación F1", f"{f1_score:.2%}")
        
        # Visualizar matriz de confusión
        st.write("### Matriz de Confusión")
        fig, ax = plt.subplots(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)  # Matriz de confusión
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=['No Desertor', 'Desertor'],
                   yticklabels=['No Desertor', 'Desertor'])
        plt.xlabel("Clase Predicha")
        plt.ylabel("Clase Real")
        st.pyplot(fig)
        
        # Mostrar reporte de clasificación detallado
        st.write("### Reporte de Clasificación")
        df_reporte = pd.DataFrame(reporte).T
        df_reporte = df_reporte.rename(index={
            "0": "Clase 0 (No Desertor)",
            "1": "Clase 1 (Desertor)",
            "accuracy": "Exactitud",
            "macro avg": "Promedio Macro",
            "weighted avg": "Promedio Ponderado"
        })
        df_reporte = df_reporte.rename(columns={
            "precision": "Precisión",
            "recall": "Sensibilidad",
            "f1-score": "Puntuación F1",
            "support": "Soporte"
        })
        st.dataframe(df_reporte.style.format("{:.4f}"))
        
        # Visualizar importancia de características
        st.write("### Importancia de Características")
        importancias = modelo.feature_importances_  # Importancia de cada característica
        nombres_caracteristicas = modelo.feature_names_in_  # Nombres de las características
        df_importancia = pd.DataFrame({
            'Característica': nombres_caracteristicas,
            'Importancia': importancias
        })
        df_importancia = df_importancia.sort_values(by='Importancia', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Importancia', y='Característica', data=df_importancia, ax=ax)
        plt.title("Top 10 Características Más Importantes")
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error al cargar las métricas: {e}")