# Data Dictionary

## Raw Variables (from Yahoo Finance)

Cuatro tickers descargados con `yfinance` desde 2015-01-01:

| Ticker | Mnemónico | Descripción |
|--------|-----------|-------------|
| GC=F | gold | Futuros del oro (COMEX) — precio de referencia global |
| DX-Y.NYB | dxy | Dólar index (ICE) — fortaleza del dólar frente a 6 divisas |
| ^VIX | vix | Volatilidad S&P 500 (CBOE) — índice de miedo del mercado |
| ^TNX | tnx | Treasury Yield 10 years (CBOE) — tasa de interés de referencia |

Cada ticker incluye las columnas `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`.
Solo se usan las columnas `Close` (mergeadas como `gold`, `dxy`, `vix`, `tnx`).

En el notebook de clasificación también se usan `gold_open`, `gold_high`, `gold_low` para features OHLC.

---

## Engineered Features (28 total)

### Features de precio y retornos

| Variable | Tipo | Descripción | Fórmula |
|----------|------|-------------|---------|
| returns | float | Retorno diario del oro | `gold.pct_change()` |
| Gold_Return_3d | float | Retorno acumulado 3 días | `gold.pct_change(3)` |
| Gold_Return_7d | float | Retorno acumulado 7 días | `gold.pct_change(7)` |
| ma_5 | float | Media móvil simple 5 días | `gold.rolling(5).mean()` |
| ma_10 | float | Media móvil simple 10 días | `gold.rolling(10).mean()` |
| ma_21 | float | Media móvil simple 21 días | `gold.rolling(21).mean()` |
| Gold_Close_MA20_Ratio | float | Desviación del precio respecto a MA20 | `gold / ma_21 - 1` |

### Features de volatilidad

| Variable | Tipo | Descripción | Fórmula |
|----------|------|-------------|---------|
| volatility_5 | float | Volatilidad rolling 5 días | `returns.rolling(5).std()` |
| volatility_10 | float | Volatilidad rolling 10 días | `returns.rolling(10).std()` |
| volatility_21 | float | Volatilidad rolling 21 días | `returns.rolling(21).std()` |

### Features OHLC (candlestick)

| Variable | Tipo | Descripción | Fórmula |
|----------|------|-------------|---------|
| Gold_Body_pct | float | Tamaño del cuerpo de la vela (%) | `(gold_close - gold_open) / gold_open` |
| Gold_Range | float | Rango intradiario relativo | `(gold_high - gold_low) / gold_open` |

### Osciladores técnicos

| Variable | Tipo | Descripción | Fórmula |
|----------|------|-------------|---------|
| rsi | float | RSI período 14 — sobrecompra >70, sobreventa <30 | Cálculo estándar Wilder |
| macd | float | MACD línea principal | `ema_12 - ema_26` |
| macd_signal | float | Señal MACD (media móvil de MACD) | `macd.ewm(span=9).mean()` |
| MACD_Histogram | float | Histograma MACD | `macd - macd_signal` |

### Features macroeconómicas

| Variable | Tipo | Descripción | Fórmula |
|----------|------|-------------|---------|
| dxy_return | float | Retorno diario del dólar | `dxy.pct_change()` |
| vix_return | float | Cambio diario del VIX | `vix.pct_change()` |
| tnx_return | float | Cambio diario del TNX | `tnx.pct_change()` |
| DXY_MA_5 | float | Media móvil DXY 5 días | `dxy.rolling(5).mean()` |
| DXY_MA_20 | float | Media móvil DXY 20 días | `dxy.rolling(20).mean()` |
| DXY_Volatility_10 | float | Volatilidad DXY 10 días | `dxy_return.rolling(10).std()` |
| VIX_MA_5 | float | Media móvil VIX 5 días | `vix.rolling(5).mean()` |
| VIX_MA_20 | float | Media móvil VIX 20 días | `vix.rolling(20).mean()` |
| VIX_Volatility_10 | float | Volatilidad VIX 10 días | `vix_return.rolling(10).std()` |
| TNX_MA_5 | float | Media móvil TNX 5 días | `tnx.rolling(5).mean()` |
| TNX_MA_20 | float | Media móvil TNX 20 días | `tnx.rolling(20).mean()` |
| TNX_Volatility_10 | float | Volatilidad TNX 10 días | `tnx_return.rolling(10).std()` |

---

## Target Variables

| Variable | Tipo | Valores | Problema | Descripción |
|----------|------|---------|----------|-------------|
| target_bin | int | 0 = Down, 1 = Up | Clasificación binaria | ¿El oro subirá mañana? (dirección) |
| target_multi | int | 0 = Baja, 1 = Estable, 2 = Sube | Clasificación multiclase | Rangos definidos por cuantiles 33/66 del retorno futuro |

---

## Feature Selection (dashboard)

El dashboard usa un subconjunto de 14 features para el modelo en vivo:

`returns`, `ma_5`, `ma_10`, `ma_21`, `volatility_5`, `rsi`, `macd`, `macd_signal`,
`dxy_return`, `vix_return`, `tnx_return`, `dxy`, `vix`, `tnx`

Escaladas con `StandardScaler`. Modelo: `RandomForestClassifier(n_estimators=200, max_depth=10)`.

---

## Frecuencia de predicción

**Diaria.** El modelo se entrena con datos OHLC diarios (cierre) y predice la dirección del oro para el **siguiente día hábil**. No se hacen predicciones intradiarias ni semanales. Cada fila del dataset representa un día de trading.

