### PoC: extracción de jugadas desde video para visualización 3D

La idea es desarrollar un proceso de backend que permita **convertir un clip de un partido de fútbol 8 en datos de movimiento**, para reproducir la jugada en un visor 3D que se esta desarrollando.

En esta primera prueba trabajaremos con **un video de 10–20 segundos de una sola cámara fija**. El sistema permitirá:

- Calibrar manualmente la relación entre la imagen y las coordenadas de la cancha.
- Detectar automáticamente a las jugadoras visibles y seguir sus movimientos.
- Asignar manualmente equipos e identidades.
- Estimar sus posiciones sobre el terreno a lo largo del tiempo.
- Exportar un **JSON compatible con el front**, con posiciones, identificadores y tiempos.
- Generar un video de diagnóstico con las detecciones y sus IDs para revisar errores.

**El objetivo es validar si podemos reconstruir los movimientos con suficiente fidelidad para el análisis táctico y cuánto trabajo manual requiere corregirlos.** No buscamos una reconstrucción perfecta ni completamente automática.

La PoC utilizará herramientas de visión artificial y modelos abiertos, sin depender inicialmente de una API paga. Comenzará como un proceso ejecutable localmente; la integración mediante una API web se agregará después de validar la extracción.

En esta etapa, **la pelota podrá cargarse manualmente**. No se incluirán reconstrucción corporal, orientación de la mirada, combinación de varias cámaras ni estimación de jugadoras fuera del encuadre. Las posiciones faltantes o interpoladas se distinguirán de las obtenidas del video.

Si los resultados son útiles, el siguiente paso será incorporar **correcciones asistidas, tracking de pelota y soporte para múltiples cámaras**.