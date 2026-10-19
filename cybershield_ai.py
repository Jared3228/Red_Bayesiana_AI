import os
import pandas as pd
import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

def preprocesar_dataset_real(ruta_csv):
    print("Mapeando columnas del dataset CIC-IDS a la Red Bayesiana...")
    df_raw = pd.read_csv(ruta_csv)
    df_procesado = pd.DataFrame()
    
    # Limpiar espacios en blanco de los nombres de las columnas (error muy común en CIC-IDS)
    df_raw.columns = df_raw.columns.str.strip()
    
    # 1. PuertoAbierto {No, Sí}: Puertos destino inusuales (por encima de los puertos bien conocidos)
    df_procesado['PuertoAbierto'] = np.where(df_raw['Destination Port'] > 1024, 'Sí', 'No')
    
    # 2. Alertas {Bajas, Altas}: Flujos anormalmente largos generan alertas
    df_procesado['Alertas'] = np.where(df_raw['Flow Duration'] > 1000000, 'Altas', 'Bajas')
    
    # 3. Trafico {Normal, Anómalo}: Tráfico con un conteo elevado de paquetes
    df_procesado['Trafico'] = np.where(df_raw['Total Fwd Packets'] > 15, 'Anómalo', 'Normal')
    
    # 4. Brecha {No, Sí}: La columna 'Label' dice 'BENIGN' si todo está bien, o el nombre del ataque
    df_procesado['Brecha'] = np.where(df_raw['Label'] != 'BENIGN', 'Sí', 'No')
    
    return df_procesado

def main():
    print("=== CyberShield AI: Red Bayesiana con Aprendizaje de Datos ===\n")
    
    # 1. Definir la estructura del DAG
    model = DiscreteBayesianNetwork([
        ('PuertoAbierto', 'Brecha'),
        ('Alertas', 'Brecha'),
        ('Trafico', 'Brecha')
    ])

    ruta_dataset = "dataset_CIC-IDS.csv" # Nombre del archivo CSV que contienen los datos a procesar. Cambiar de ser necesario.
    
    # 2. Obtener los datos (Reales o Sintéticos)
    # Si el archivo no existe, se generará un dataset sintético
    ruta_dataset = "dataset_CIC-IDS.csv" 
    
    if os.path.exists(ruta_dataset):
        print(f"[+] Archivo '{ruta_dataset}' encontrado. Procesando datos...")
        # Preprocesar el dataset real para mapearlo a las variables de la Red Bayesiana
        df = preprocesar_dataset_real(ruta_dataset)
    else:
        print(f"[-] Archivo '{ruta_dataset}' no encontrado.")
        print("Terminando el programa. Por favor, asegúrate de tener el archivo CSV en la ruta especificada.")
        return 
        
    print(f"\nVista previa de los datos procesados (Total: {len(df)} filas):")
    print(df.head())
    print("-" * 50)

    print("Entrenando el modelo Bayesiano...")
    model.fit(df)
    
    # Verificar que el modelo se haya construido correctamente
    assert model.check_model(), "Error al ajustar el modelo con los datos."
    
    # 4. Mostrar las CPDs calculadas para validar
    print("\nCPD Calculada para la variable 'Brecha' a partir de los datos:")
    print(model.get_cpds('Brecha'))
    print("-" * 50)

    # 5. Preparar el motor de inferencia
    infer = VariableElimination(model)

    # 6. Consultas de Inferencia Requeridas por el Documento
    print("\n[Consulta 1] P(Brecha | PuertoAbierto=Sí, Alertas=Altas)")
    q1 = infer.query(variables=['Brecha'], evidence={'PuertoAbierto': 'Sí', 'Alertas': 'Altas'})
    print(q1)
    
    print("\n[Consulta 2] P(Brecha | Tráfico=Anómalo)")
    q2 = infer.query(variables=['Brecha'], evidence={'Trafico': 'Anómalo'})
    print(q2)

if __name__ == '__main__':
    main()