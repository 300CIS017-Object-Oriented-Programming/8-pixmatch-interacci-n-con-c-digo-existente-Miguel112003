#  Entregable - Mejoras para pasar a POO
Detalla en este markdown lo siguiente: 
- **Clases a Definir:** Enumera las clases que se podrían definir, describe sus propósito y justifica porque crees que es una clase útil para mejorar el programa.
- **Métodos Importantes:** Enumera los métodos principales para cada clase. Incluye una descripción de cuál sería la utilidad de cada método
- **Imagen del UML del diagrama de clases**  Adjunta una imagen del UML del diagrama de clases como una forma visual de planificar y entender la estructura de las clases, métodos, atributos y relaciones que podría tener una versión mejorada del código fuente.
- **Organización de archivos:** Propon una estructura de organización de los archivos de este proyecto para que no queden todos en la raiz principal. Investiga cuáles podrían ser buenas formas de organizar los directorios y a partir de tu investigación indica qué directorios crearías y cómo los organizarías. 


# Clases a Definir
## Clase: Juego
### Atributos
Una clase para reemplazar al session state de streamlit, este contaria con algunos atributos del session state
añadiendo aspectos para facilitar la implementacion de metodos, y algo para determinar si una session termino, se puede
apreciar mas a fondo en el diagrama UML

### Metodos
Idealmente esta clase debe contar con metodos get/set, asi como metodos para definir el leaderboard y los jugadores.

## Clase: Emoticon
### Atributos
Implementar una clase emoticon de forma general que tenga dentro el listado de los emoticones y un metodo modifique
aleatoriamente el emoticon actual seria una forma de plantear el programa para facilitar su funcionamiento, en lugar de 
tener tantas listas con emoticones sueltas en una funcion mantenerlas en una clase facilitaria su manipulacion
Ademas debe contar con variables de estado Booleanas para definir las diferentes caracteristicas del emoticon
### Metodos
Esta clase debe contar con metodos para modificar sus atributos, asi como sus metodos get y set.

## Clase: Tablero
### Atributos
Representar el tablero como una matriz de objetos emoticon podria ser una forma de tener control sobre el tablero de juego
sin depender de tantas funciones y sobretodo de streamlit (No me gusta, no lo siento tan logico, quizas me falta practica)
puntualmente utilizaria una lista que cada posicion represente una posicion del tablero ya que no conozco si existen los
arreglos estaticos como en C pero en Python
### Metodos
Esta clase debe contar con metodos para construir, llenar, y reiniciar el tablero de juego, asi como sus metodos get y sets

## Clase: Jugador
### Atributos
Esta clase seria para definir los datos del jugador y tener acceso a ellos, no deberia ser nada especial, solo almacenar
todo en una variable.
### Metodos
Esta clase debe contar con metodos setters y getters.

# Diagrama UML
En general esete Diagrama resume lo que seria mi diseño propuesto bajo el paradigma de POO

![Diagrama UML Diseño](D:\8-pixmatch-interacci-n-con-c-digo-existente-Miguel112003\docs\img\Diagrama_UML.png)