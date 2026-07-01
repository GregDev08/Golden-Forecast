# Decision Log

| Date | Decision | Justification |
|-------|----------|---------------|
| 29/06/2026 | Selección de dataset: GLD (Gold ETF) por Yahoo Finance | Datos públicos, históricos suficientes (2010-actualidad), volumen y precio disponibles |
| 30/06/2026 | María designada Product Owner | Responsable de visión de negocio y validación |
| 30/06/2026 | Juan designado Scrum Master | Responsable de coordinación y seguimiento |
| 30/06/2026 | Problema dual: clasificación + regresión | Aprovechar el mismo dataset para ambos enfoques y comparar resultados |
| 30/06/2026 | Ramas feature/ con PR a main protegida | Flujo profesional GitHub Flow con revisión de código |
| 30/06/2026 | Ticker: GC=F (futuros del oro) + DXY + VIX + TNX | Precio real del oro y 3 macroindicadores para enriquecer features |
| 30/06/2026 | Fecha inicio: 2015-01-01 | ~10 años de datos históricos (~2894 registros diarios) |
| 30/06/2026 | Documentación bilingüe (inglés/español) | README, ROADMAP y PR template en inglés; notebooks y decision_log bilingües |
| 30/06/2026 | Repositorio profesional estructurado | README, ROADMAP, PR template, decision_log, project_handbook incluidos |
| 30/06/2026 | Kanban en GitHub Projects | Seguimiento visual del sprint con columnas To Do / In Progress / Done |
| 30/06/2026 | Data lineage documentado en `data/README.md` | Trazabilidad del origen y transformación de datos |
| 30/06/2026 | Data dictionary en `docs/data_dictionary.md` | Definición de todas las variables del modelo |
| 30/06/2026 | 28 features técnicas + macro | Retornos, medias móviles, RSI, MACD, volatilidades, OHLC, indicadores macro (DXY, VIX, TNX) |
| 30/06/2026 | Random Forest como modelo principal | n_estimators=200, max_depth=10. Equilibrio entre precisión y robustez. Incluye Dummy, Logistic Regression y XGBoost como referencias |
| 30/06/2026 | Target multiclase por cuantiles 33/66 | Permite 3 categorías: baja/estable/sube, más informativo que binario puro |
| 30/06/2026 | Predicción diaria del oro | Frecuencia diaria con datos OHLC diarios de Yahoo Finance. Predice si el oro sube o baja al día siguiente hábil |
| 01/07/2026 | Dashboard salón del lejano oeste | Plotly Dash con temática Wild West (slot machine, madera, latón, dorado) para presentación a cliente no técnico |
| 01/07/2026 | Fondo SVG animado (`saloon_bg.svg`) | Vector art responsivo 1920×1080 con animaciones CSS embebidas (monedas, lámparas, reels, luces) |
| 01/07/2026 | Audio autoplay con fallback táctil | Música de salón con patrón estándar: intento play() + captura Promise + listener en primer click |
| 01/07/2026 | Logo corporativo en esquina del dashboard | Banner corporativo posicionado en esquina superior derecha del slot-header |
| 01/07/2026 | Descripciones en español para no técnicos | Cada tab del dashboard incluye párrafo explicativo del gráfico y su relevancia de negocio |
| 01/07/2026 | Justificación de modelos en tarjetas visuales | Grid de 4 tarjetas explicando por qué cada modelo fue elegido (Dummy→línea base, RF→principal, XGB→opcional) |
