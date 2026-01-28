from pathlib import Path

import pandas as pd

# Configuración y Constantes

RAW_DATA_PATH = Path("../data/raw/dataset.csv")
PROCESSED_DIR = Path("../data/processed")
PROCESSED_DIR.mkdir(
    parents=True, exist_ok=True
)  # Aquí se crea la carpeta si no existe.

# Columnas que serán eliminadas por baja relevancia o redundancia.
COLS_TO_DROP = [
    "Objetivo",
    "Internacional",
    "Nacionalidad",
    "Necesidades_educativas_especiales",
    "Estado_civil",
    "Unidades_1er_sem_acreditadas",
    "Unidades_2do_sem_acreditadas",
    "Unidades_1er_sem_sin_evaluaciones",
    "Unidades_2do_sem_sin_evaluaciones",
]

# Diccionario de traducción (Mapeo Inglés -> Español).
COLUMN_MAPPING = {
    "Marital status": "Estado_civil",
    "Application mode": "Modo_solicitud",
    "Application order": "Orden_solicitud",
    "Course": "Carrera",
    "Daytime/evening attendance": "Asistencia_diurna_nocturna",
    "Previous qualification": "Calificacion_previa",
    "Nacionality": "Nacionalidad",
    "Mother's qualification": "Calificacion_madre",
    "Father's qualification": "Calificacion_padre",
    "Mother's occupation": "Ocupacion_madre",
    "Father's occupation": "Ocupacion_padre",
    "Displaced": "Desplazado",
    "Educational special needs": "Necesidades_educativas_especiales",
    "Debtor": "Deudor",
    "Tuition fees up to date": "Pagos_al_dia",
    "Gender": "Genero",
    "Scholarship holder": "Becado",
    "Age at enrollment": "Edad_al_matricularse",
    "International": "Internacional",
    "Curricular units 1st sem (credited)": "Unidades_1er_sem_acreditadas",
    "Curricular units 1st sem (enrolled)": "Unidades_1er_sem_matriculadas",
    "Curricular units 1st sem (evaluations)": "Unidades_1er_sem_evaluaciones",
    "Curricular units 1st sem (approved)": "Unidades_1er_sem_aprobadas",
    "Curricular units 1st sem (grade)": "Unidades_1er_sem_nota",
    "Curricular units 1st sem (without evaluations)": "Unidades_1er_sem_sin_evaluaciones",
    "Curricular units 2nd sem (credited)": "Unidades_2do_sem_acreditadas",
    "Curricular units 2nd sem (enrolled)": "Unidades_2do_sem_matriculadas",
    "Curricular units 2nd sem (evaluations)": "Unidades_2do_sem_evaluaciones",
    "Curricular units 2nd sem (approved)": "Unidades_2do_sem_aprobadas",
    "Curricular units 2nd sem (grade)": "Unidades_2do_sem_nota",
    "Curricular units 2nd sem (without evaluations)": "Unidades_2do_sem_sin_evaluaciones",
    "Unemployment rate": "Tasa_desempleo",
    "Inflation rate": "Tasa_inflacion",
    "GDP": "PIB",
    "Target": "Objetivo",
}


# Funciones de Procesamiento
# Elimina duplicados y limpia los registros
def limpiar_dataset(df: pd.DataFrame) -> pd.DataFrame:
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Duplicados eliminados: {initial_len - len(df)}")

    # Se rellenan valores vacíos con la mediana.
    if df.isnull().values.any():
        print("Valores nulos detectados. Rellenando con la mediana...")
        df = df.fillna(df.median(numeric_only=True))

    return df


def main():
    print("Iniciando el procesamiento de datos...")

    # Carga
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"Dataset cargado. Dimensiones originales: {df.shape}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {RAW_DATA_PATH}")
        return

    # Se renombra las columnas al español para facilitar el análisis.
    df = df.rename(columns=COLUMN_MAPPING)

    # División Lógica
    mask_inscritos = df["Objetivo"] == "Enrolled"

    df_inscritos = df[mask_inscritos].copy()
    df_entrenamiento = df[~mask_inscritos].copy()

    # Aquí se crea la variable objetivo binaria: 1 si es Desertor, 0 si se Graduó.
    df_entrenamiento["Es_Desertor"] = (
            df_entrenamiento["Objetivo"] == "Dropout"
    ).astype(int)

    # Limpieza de Columnas
    df_entrenamiento = df_entrenamiento.drop(columns=COLS_TO_DROP)

    # Para inscritos, se eliminan las columnas que no son relevantes para el modelo.
    cols_to_drop_inscritos = (
        COLS_TO_DROP if "Objetivo" in COLS_TO_DROP else COLS_TO_DROP + ["Objetivo"]
    )
    df_inscritos = df_inscritos.drop(columns=cols_to_drop_inscritos)

    # Limpieza de Nulos/Duplicados
    print("\nProcesando Dataset de Entrenamiento:")
    df_entrenamiento = limpiar_dataset(df_entrenamiento)

    print("\nProcesando Dataset de Evaluación (Inscritos):")
    df_inscritos = limpiar_dataset(df_inscritos)

    # Aquí se exportan los datos procesados a la carpeta 'processed'.
    train_path = PROCESSED_DIR / "entrenamiento.csv"
    eval_path = PROCESSED_DIR / "evaluacion.csv"

    df_entrenamiento.to_csv(train_path, index=False)
    df_inscritos.to_csv(eval_path, index=False)

    print(f"\nArchivos generados exitosamente:")
    print(f"   -> {train_path}")
    print(f"   -> {eval_path}")


if __name__ == "__main__":
    main()
