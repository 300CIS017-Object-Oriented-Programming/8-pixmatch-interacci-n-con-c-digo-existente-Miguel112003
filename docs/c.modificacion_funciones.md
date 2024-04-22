
## Evidencia del cambio
> Ponga aquí evidencia con imágenes y fragmento de código


#### Archivo Json guarda 4 jugadores
```python
    elif what_to_do == 'read':
        if estado_app.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(direccion_local + 'leaderboard.json'):
                leaderboard = json.load(open(direccion_local + 'leaderboard.json'))  # read file

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, columna1, columna2, columna3 = st.columns((2, 2, 2, 2))
                rknt = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            columna1.write(
                                f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2:
                            columna2.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3:
                            columna3.write(
                                f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 4:
                            columna3.write(
                                f"4th | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
```
![Imagen JSON](D:\8-pixmatch-interacci-n-con-c-digo-existente-Miguel112003\docs\img\JSON4Jugadores.PNG)

#### Interfa gráfica muestra cuatro jugadores
![Imagen Leaderboard](D:\8-pixmatch-interacci-n-con-c-digo-existente-Miguel112003\docs\img\Leaderboard_4_jugadores.PNG)

#### Usuario pierde el juego cuando supera un máximo posible de fallos.
![Imagen Perder](D:\8-pixmatch-interacci-n-con-c-digo-existente-Miguel112003\docs\img\MensajePerder.PNG)
## Encuesta de la experiencia
Por favor, responde las siguientes preguntas basadas en tu experiencia modificando el código para incluir cuatro personas en el leaderboard en lugar de tres.

**Nombre:**

#### 1. ¿Cuánto tiempo te llevó entender las secciones del código relacionada con el leaderboard?
- [ ] Menos de 10 minutos
- [ ] Entre 10 y 30 minutos
- [ ] Entre 30 minutos y 1 hora
- [✅️] Más de 1 hora

#### 2. ¿Cuánto tiempo te llevó entender las secciones del código relacionada con hacer que el usuario pierda si supera x cantidad de turnos?
- [ ] Menos de 10 minutos
- [ ] Entre 10 y 30 minutos
- [ ] Entre 30 minutos y 1 hora
- [✅️] Más de 1 hora

#### 3. ¿Consideras que estaba documentada la lógica en el código para facilitar el cambio?
- [ ] Sí
- [✅️] No

#### 4. ¿Te pareció fácil identificar dónde y qué cambios realizar para aumentar el número de personas en el leaderboard de 3 a 4?
- [ ] Muy fácil
- [ ] Algo fácil
- [✅] Algo difícil
- [ ] Muy difícil


#### 5. ¿Te pareció fácil identificar dónde y qué cambios realizar para agregar la lógica de perder el juego?
- [ ] Muy fácil
- [ ] Algo fácil
- [✅️] Algo difícil
- [ ] Muy difícil


#### 6. ¿Qué tan seguro te sientes de que tus cambios no introdujeron errores en otras áreas del código?
- [ ] Muy seguro
- [✅️] Moderadamente seguro
- [ ] Poco seguro
- [ ] Nada seguro

#### 7. Después de realizar los cambios, ¿cuánto tiempo te tomó verificar que el cambio funcionó como se esperaba?
- [ ] Menos de 10 minutos
- [✅️] Entre 10 y 30 minutos
- [ ] Entre 30 minutos y 1 hora
- [ ] Más de 1 hora

#### 8. ¿Qué estrategia usaste para verificar que no habían problemas en el código fuente?
Jugar, intentar forzar el error durante la ejecución, además de intentar mantener los cambios al minimo, de forma que no
afecte a cosas que no necesitan modificarse.

#### 9. ¿Te enfrentaste a algún problema mientras intentabas realizar los cambios? Si es así, ¿cómo lo resolviste?
- [ ] No enfrenté problemas
- [ ] Revisé la documentación del código
- [ ] Busqué ayuda de un compañero o en línea
- [✅️] B y C son correctas

Había cosas que no entendía, por lo que además de detenerme a leer nuevamente en repetidas ocasiones también leia la 
documentation de streamlit, por lo que sería tanto la opción B como la C, además de entrar ocasionalmente a stackoverflow
para ver como solucionar los errores que me salian :D