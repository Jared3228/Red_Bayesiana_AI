# Proyecto Integrador - Proyecto 2 (Red Bayesiana)

## 📋 Descripción
Este módulo implementa una Red Bayesiana para la **detección de brechas de seguridad** en el contexto del proyecto **CyberShield AI**. Utilizando algoritmos de Inteligencia Artificial fundamentados en probabilidad condicional, el sistema evalúa el riesgo de un ciberataque analizando indicadores clave extraídos de un entorno de red real (Dataset CIC-IDS).

## 🏗 Estructura de la Red
- **Variables:**
  - `PuertoAbierto`: Presencia de un puerto abierto inusual o alto. Estados: `{No, Sí}`
  - `Alertas`: Alertas generadas por flujos de duración anormal. Estados: `{Bajas, Altas}`
  - `Trafico`: Tráfico anómalo determinado por un conteo elevado de paquetes. Estados: `{Normal, Anómalo}`
  - `Brecha`: Ocurrencia de una brecha de seguridad (Ataque vs Tráfico Benigno). Estados: `{No, Sí}`

- **Dependencias:**
  La variable dependiente principal es `Brecha`. Su probabilidad está condicionada directamente por el estado de los tres indicadores de red. Es decir, `PuertoAbierto`, `Alertas` y `Trafico` son nodos "padre" que apuntan directamente al nodo "hijo" `Brecha`.

- **Diagrama:**
  ```text
  PuertoAbierto ──┐
                  ▼
  Alertas ───────► Brecha
                  ▲
  Tráfico ────────┘
  ```

## 📊 CPDs (Tablas de Probabilidad Condicional)

Las probabilidades no fueron asignadas arbitrariamente, sino que fueron aprendidas empíricamente mediante el método de **Máxima Verosimilitud (Maximum Likelihood Estimation)** procesando más de 225,745 registros del dataset público CIC-IDS.

| Variable | Padres | Descripción |
| :--- | :--- | :--- |
| `PuertoAbierto` | Ninguno | Probabilidad a priori de observar conexiones en puertos > 1024. |
| `Alertas` | Ninguno | Probabilidad a priori de observar flujos con duraciones inusualmente largas. |
| `Trafico` | Ninguno | Probabilidad a priori de registrar un alto volumen de paquetes por conexión. |
| `Brecha` | `PuertoAbierto`, `Alertas`, `Trafico` | Matriz condicional calculada empíricamente. Curiosamente, los datos demostraron que la mayor probabilidad de brecha (90.3%) ocurre cuando *no* se usan puertos altos y el tráfico parece *normal*, indicando que los atacantes intentan evadir la detección imitando el tráfico benigno en puertos bien conocidos (ej. 80, 22). |

## 🔍 Consultas de Inferencia

1. **Consulta 1:** P(Brecha | PuertoAbierto=Sí, Alertas=Altas)
- **Resultado:** P(Brecha=Sí) = 0.0001 (0.01%) / P(Brecha=No) = 0.9999 (99.99%)
- **Interpretación:** En contra de la intuición tradicional, cuando el sistema registra puertos altos (Sí) y alertas por flujos largos (Altas), es casi seguro (99.99%) que se trata de tráfico legítimo pesado (como la descarga de un archivo o streaming de un usuario) y no de un ciberataque.

2. **Consulta 2:** P(Brecha | Tráfico=Anómalo)
- **Resultado:** P(Brecha=Sí) = 0.0000 (0%) / P(Brecha=No) = 1.0000 (100%)
- **Interpretación:** En este dataset moderno, un alto volumen de paquetes (`Tráfico=Anómalo`) corresponde enteramente a comportamiento benigno. Los ataques registrados en esta red tienden a enviar ráfagas cortas de paquetes para evitar saturar la red y delatar su presencia.

## 🚀 Instrucciones de Ejecución
1. Clonar el repositorio: `git clone https://github.com/Jared3228/Red_Bayesiana_AI`
2. Navegar al directorio del proyecto: `cd [NOMBRE_DEL_DIRECTORIO]`
3. Instalar dependencias necesarias: `pip install -r requirements.txt`
   *(Nota: Asegúrate de tener Python instalado y el dataset CIC-IDS nombrado como `dataset_CIC-IDS.csv` en la raíz del proyecto).*
4. Ejecutar el script: `python cybershield_ai.py`
 *(Link al dataset utilizado: https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset/data?select=Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv)*
## 📸 Ejemplo de Salida

```text
[+] Archivo 'dataset_CIC-IDS.csv' encontrado. Procesando datos...
Mapeando columnas del dataset CIC-IDS a la Red Bayesiana...

Vista previa de los datos procesados (Total: 225745 filas):
  PuertoAbierto Alertas Trafico Brecha
0            Sí   Bajas  Normal     No
1            Sí   Bajas  Normal     No
...

[Consulta 1] P(Brecha | PuertoAbierto=Sí, Alertas=Altas)
+------------+---------------+
| Brecha     |   phi(Brecha) |
+============+===============+
| Brecha(No) |        0.9999 |
+------------+---------------+
| Brecha(Sí) |        0.0001 |
+------------+---------------+
```

## 🤖 Declaración de Uso de IA
- **Herramienta(s) utilizada(s):** Gemini 3.1 Pro
- **Propósito:** Apoyo en la generación de la estructura de código mediante la librería `pgmpy`, depuración de errores de compatibilidad en la fase de entrenamiento con Pandas y estructuración de la documentación final.
- **Prompt(s):** "En base a las instrucciones dentro del documento ayudame y guiame para crear el programa, sin generar código. Manteniendo enfasis en entender porqué estoy haciendo lo que hago, codigo limpio y el mejor camino sin codigo innecesario".
- **Declaración:** Declaro que el presente trabajo ha sido elaborado por el equipo. Hemos utilizado herramientas de IA para apoyar en la estructuración algorítmica y sintaxis de la librería, y todo el contenido técnico y código ha sido verificado, depurado y adaptado por nosotros. Adjuntamos los prompts utilizados como evidencia de nuestro proceso.
