## Requisitos Funcionales y Criterios de Aceptación

### 1. Configuración de Nivel de Dificultad
**Requisito:** El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.

**Criterios de Aceptación:**
- Opciones de dificultad fácil, medio y difícil disponibles para selección.
- La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y la puntuación.
- Tiempos de regeneración específicos:
  - Fácil: cada 8 segundos.
  - Medio: cada 6 segundos.
  - Difícil: cada 5 segundos.

### 2. Gestión de Puntaje y Validación de Respuestas
**Requisito:** El sistema debe ser capaz de gestionar y actualizar el puntaje del jugador en tiempo real, basado en las respuestas del usuario durante el juego.

**Criterios de Aceptación:**
- El puntaje se actualiza inmediatamente después de que el jugador selecciona una casilla.
- Se otorga una puntuación positiva por cada selección correcta y una penalización por cada selección incorrecta.
- La cantidad de puntos ganados o perdidos varía según la dificultad del juego.

### 3. Visualización de Estado de Juego
**Requisito:** El sistema debe mostrar el estado actual del juego, incluyendo el puntaje actual, el número de celdas restantes por descubrir, y un emoji que refleje la situación actual del jugador.

**Criterios de Aceptación:**
- El puntaje actual y las celdas restantes deben estar visibles en todo momento durante el juego.
- Debe haber una representación visual (emoji) que cambie en respuesta al puntaje actual del jugador.

### 4. Reinicio y Preparación del Tablero de Juego
**Requisito:** El sistema debe ser capaz de preparar y reiniciar el tablero de juego al inicio de cada partida, asegurando que los emojis se distribuyan de manera aleatoria y que el emoji objetivo esté incluido en el tablero.

**Criterios de Aceptación:**
- El tablero se debe reiniciar completamente con cada nueva partida.
- El emoji objetivo debe estar presente al menos una vez en el tablero.

### 5. Gestión de la Tabla de Líderes
**Requisito:** El sistema debe proporcionar una tabla de líderes que registre los puntajes más altos alcanzados, mostrando los nombres de los jugadores y sus puntuaciones.

**Criterios de Aceptación:**
- La tabla de líderes debe actualizarse con cada partida que supere los puntajes previamente registrados.
- Debe mostrar los tres mejores puntajes.