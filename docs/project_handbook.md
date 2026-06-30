# DataScope Solutions: Project Handbook & Governance

**Proyecto:** Machine Learning Pipeline & Predictive Modeling
**Versión:** 2.1.0
**Fecha:** 30 de junio de 2026

---

## 1. Project Charter

Este documento define la metodología, gobernanza y estándares del proyecto DataScope Solutions.

El objetivo es desarrollar una solución de Machine Learning supervisado (clasificación o regresión) desde datos crudos hasta una propuesta de valor explicable para cliente.

El proyecto se desarrollará siguiendo un enfoque Agile adaptado a Scrum, promoviendo la colaboración, la trazabilidad del trabajo y la reproducibilidad técnica.

---

## 2. Equipo del Proyecto

### Miembros

* María
* Juan
* José
* Gema
* Joel

### Roles y Responsabilidades

#### Product Owner (PO) – María

Responsable de la visión de negocio y validación final del proyecto.

Funciones:

* Definir objetivos del proyecto.
* Priorizar backlog y entregables.
* Validar resultados obtenidos.
* Revisar el cumplimiento de objetivos.
* Coordinar la presentación final.
* Garantizar la alineación entre negocio y solución técnica.

#### Scrum Master (SM) – Juan

Responsable de facilitar el proceso Scrum y coordinar el equipo.

Funciones:

* Organizar Sprint Planning.
* Coordinar Daily Sync.
* Gestionar bloqueos.
* Supervisar el tablero Kanban.
* Asegurar el cumplimiento del proceso Scrum.
* Verificar la Definition of Done.
* Coordinar retrospectivas.

#### Development Team

**José, Gema y Joel**

Responsables de la implementación técnica del proyecto.

##### Propuesta inicial de distribución de responsabilidades

**José**

Responsable principal de análisis exploratorio.

Tareas:

* Exploratory Data Analysis (EDA).
* Estadística descriptiva.
* Identificación de valores nulos.
* Detección de anomalías.
* Análisis de correlaciones.
* Elaboración de visualizaciones.
* Documentación de hallazgos.

**Gema**

Responsable principal de preprocesamiento.

Tareas:

* Limpieza de datos.
* Tratamiento de valores faltantes.
* Transformación de variables.
* Codificación de variables categóricas.
* Escalado de variables.
* Feature Engineering.
* Construcción del pipeline de preprocesamiento.
* Validación de ausencia de data leakage.

**Joel**

Responsable principal de modelado.

Tareas:

* Selección de algoritmos candidatos.
* Entrenamiento de modelos.
* Comparación entre enfoques.
* Evaluación mediante métricas.
* Ajuste de hiperparámetros.
* Validación básica.
* Análisis de overfitting.
* Interpretación de resultados.

> La distribución de responsabilidades es orientativa y podrá ajustarse durante Sprint Planning según las necesidades del proyecto.

---

## 3. Problema de Negocio

El cliente dispone de datos históricos pero no tiene claridad sobre cómo aprovecharlos para generar información útil que apoye la toma de decisiones.

Actualmente el equipo está evaluando desarrollar un caso de estudio basado en datos históricos relacionados con el precio del oro.

El objetivo es determinar si es posible construir un modelo predictivo que permita estimar el comportamiento futuro de la variable objetivo e identificar patrones relevantes.

El equipo deberá:

* Determinar si el problema se aborda como clasificación o regresión.
* Definir el target adecuado.
* Construir un pipeline completo de Machine Learning supervisado.
* Evaluar el rendimiento predictivo del modelo.
* Traducir resultados técnicos a lenguaje de negocio.
* Comunicar conclusiones de manera clara y comprensible.

**Estado actual:** Dataset definitivo pendiente de selección.

---

## 4. Metodología de Trabajo (Agile - Scrum adaptado)

### 4.1 Rituales

* Sprint Planning: definición de tareas y dataset.
* Daily Sync: avances, bloqueos y próximos pasos.
* Sprint Review: presentación final al cliente.
* Retrospectiva: identificación de mejoras del proceso.

### 4.2 Kanban

Columnas:

* Por hacer
* En progreso
* Hecho

Herramienta recomendada:

* GitHub Projects
* Trello

---

## 5. Flujo de Trabajo Técnico (GitHub Flow)

Reglas:

1. Rama principal protegida (`main`)
2. Ramas por feature:

   * `feature/eda`
   * `feature/preprocessing`
   * `feature/modeling`
   * `feature/documentation`
3. Pull Requests obligatorios.
4. Revisión por pares antes del merge.

### Conventional Commits

* feat: nueva funcionalidad
* fix: corrección de errores
* docs: documentación
* refactor: mejora de código
* chore: tareas de mantenimiento

---

## 6. Estructura del Repositorio

```text
/data
/notebooks
/src
/models
/docs

README.md
requirements.txt
```

---

## 7. Dataset

**Estado:** En evaluación

### Caso de estudio preliminar

Predicción del comportamiento histórico del precio del oro.

### Variables potenciales

* Fecha
* Open
* High
* Low
* Close
* Adj Close
* Volume
* Rendimientos diarios
* Variación porcentual
* Medias móviles
* Indicadores técnicos derivados

### Requisitos

* Dataset supervisado.
* Variables numéricas suficientes.
* Calidad adecuada para modelado.
* Datos públicos.
* Permisos de reutilización.
* Reproducibilidad del proceso.

### Fuentes candidatas

* Kaggle
* Yahoo Finance
* Alpha Vantage
* Investing.com
* FRED
* Hugging Face

### Decisión

La selección definitiva del dataset será realizada durante la Fase 0 (Setup) tras evaluación conjunta del equipo.

---

## 8. Pipeline de Machine Learning

1. Carga de datos
2. EDA (análisis exploratorio)
3. Limpieza de datos
4. Feature Engineering
5. Train/Test Split
6. Preprocesamiento
7. Entrenamiento de modelos
8. Evaluación
9. Comparación de resultados
10. Interpretación
11. Conclusiones

---

## 9. Métricas de Evaluación

### Clasificación

* Accuracy
* Precision
* Recall
* F1-score

### Regresión

* MAE
* RMSE
* R²

> La métrica principal será definida según el problema de negocio.

---

## 10. Definition of Done (DoD)

Una tarea está completada si:

* Código funcional sin errores.
* No existe data leakage.
* Pipeline reproducible.
* Documentación actualizada.
* Pull Request revisado.
* Peer review aprobado.
* Resultados interpretables.

---

## 11. Data Governance

* No se versionan datos sensibles.
* Se documenta el origen del dataset.
* Se evita data leakage.
* Se mantiene trazabilidad del pipeline.
* Se garantiza reproducibilidad.

---

## 12. Modelo y Validación

* Se entrenará al menos un modelo base.
* Se compararán al menos dos enfoques.
* Validación cruzada opcional.
* Se analizará overfitting.
* Se estudiará la interpretabilidad de resultados.

---

## 13. Registro de Decisiones (Decision Log)

| Fecha      | Decisión                                           | Justificación                                                     |
| ---------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| 29/06/2026 | Selección de dataset                               | Pendiente                                                         |
| 30/06/2026 | María designada Product Owner                      | Responsable de visión de negocio                                  |
| 30/06/2026 | Juan designado Scrum Master                        | Responsable de coordinación y seguimiento                         |
| 30/06/2026 | José, Gema y Joel asignados al Development Team    | Distribución de responsabilidades técnicas                        |
| 30/06/2026 | Evaluación del precio del oro como caso de estudio | Posible aplicación de modelos predictivos sobre series temporales |

---

## 14. Registro de Riesgos (Risk Log)

| Riesgo                | Impacto | Mitigación          |
| --------------------- | ------- | ------------------- |
| Overfitting           | Alto    | CV + regularización |
| Mala calidad de datos | Alto    | EDA exhaustivo      |
| Dataset insuficiente  | Medio   | Evaluación temprana |
| Retrasos              | Medio   | Kanban + Daily Sync |

---

## 15. Criterios de Evaluación del Proyecto

* Preparación correcta de datos.
* Modelado justificado.
* Métricas interpretadas adecuadamente.
* Código limpio y modular.
* Documentación completa.
* Comunicación clara.
* Trabajo colaborativo evidenciado.

---

## 16. Entregables

1. Notebook completo (EDA → modelo → evaluación)
2. Repositorio GitHub estructurado
3. Presentación tipo pitch (10–12 minutos)
4. Documentación técnica del proyecto

---

## 17. Presentación Final

Estructura:

1. Equipo
2. Problema de negocio
3. Dataset
4. Metodología
5. Resultados
6. Limitaciones
7. Conclusiones
8. Próximos pasos

---

## 18. Stack Tecnológico

* Python
* pandas
* numpy
* scikit-learn
* matplotlib
* seaborn
* Git
* GitHub
* Jupyter Notebook
* VS Code

---

## 19. Principio del Proyecto

> "De datos crudos a decisiones de negocio explicables."
