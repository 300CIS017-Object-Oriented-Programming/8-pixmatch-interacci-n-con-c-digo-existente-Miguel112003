import streamlit as st #Framework para la interfaz con el Usuario
import os #Utilizada para encontrar las direcciones de los archivos
import time as tm #Se utiliza para hacer pausas en la ejecucion de codigo
import random #Utilizada para aleatorizar la posicion de los emoticones
import base64 #Si no me equivoco es para decodificar las imagenes de forma que sean almacenables en variables
import json #Manejo de archivos bajo la Notacion de Objeto de Javascript
from PIL import Image #Esta sirve para manipular imagenes, tipo estirarlas o contraerlas
from streamlit_autorefresh import st_autorefresh #Algo de Streamlit

#Modificar el Nombre de la pagina en la barra de pestañas, asi como su icono, tambien determina que el menu desplegable inicie expandido
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

#Esta parte es para hallar la direccion donde se guardan los archivos del programa, se modifico para que no haya problemas si esta en el Disco C
#Ademas creo que no hay ningun otro uso para el modulo "os", considerare quitarlo.
#Renombro la variable para facilitar la lectura del Codigo
direccion_local = "./"

#Esta variable define un contenedor Generico en HTML con estilos de CSS implementados, Dios sabra que hace cada cosa al detalle pero deja un espacio para una variable
contenedor_emoji_grande = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

#Otro contenedor generico en HTML con estilos CSS, este es para mostrar el emoji en chiquito y una vez se presiona se pone o una x o un chulito
emoticon_presionado = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

# Las lineas moraditas que estan por todo lado
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"

#La definicion del Color Purpura en dominio RGB
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

#Un session_state es como una forma de almacenar multiples variables de estado, tipo un objeto con varios atributos
estado_app = st.session_state

# Almacena las celdas que han sido presionadas durante el juego para evitar repeticiones
if "expired_cells" not in estado_app: estado_app.expired_cells = []

# Mantiene la puntuación del jugador, ajustándose con respuestas correctas e incorrectas
if "myscore" not in estado_app: estado_app.myscore = 0

# Guarda el estado de cada botón en la cuadrícula (presionado, correcto/incorrecto, emoji mostrado)
if "plyrbtns" not in estado_app: estado_app.plyrbtns = {}

# Contiene el emoji actual en la barra lateral que los jugadores deben buscar en la cuadrícula
if "sidebar_emoji" not in estado_app: estado_app.sidebar_emoji = ''

# Lista de emojis disponibles para ser usados en los botones durante el juego
if "emoji_bank" not in estado_app: estado_app.emoji_bank = []

# Detalles del juego, incluyendo dificultad, intervalo de autogeneración de emojis, y detalles del jugador
if "GameDetails" not in estado_app:
    estado_app.GameDetails = [
        'Medium',   # Nivel de dificultad: Easy, Medium, Hard
        6,          # Intervalo en segundos para la autogeneración de emojis
        7,          # Número total de celdas por fila o columna
        ''          # Nombre y país del jugador, para la tabla de líderes
    ]


# Funciones comunes
def ReduceGapFromPageTop(wch_section='main page'):
    """
    Brief:
        Procedimiento que ajusta el espacio superior en la interfaz de Streamlit, permitiendo modificar el relleno
        superior de las secciones principales y de la barra lateral

    Parameters:
        wch_section (str): Define la sección de la página donde se aplicará el ajuste del espacio
                           Las opciones disponibles son:
                           - 'main page': Aplica el ajuste solo al area principal
                           - 'sidebar': Aplica el ajuste solo a la barra lateral
                           - 'all': Aplica el ajuste tanto a la área principal como a la barra lateral

    """
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


def Leaderboard(what_to_do):
    """
       Brief:
           Gestiona las operaciones sobre el leaderboard, para ya sea
           escribir en él o leer desde él, La acción específica depende del parámetro, ademas se almacenan
           los puntajes en un archivo de notacion de objeto javascript (JSON)

       Parameters:
           what_to_do (str): Indica la acción a realizar sobre el leaderboard. Las opciones son:
                             - 'create': Crea un archivo nuevo para el leaderboard si no existe
                             - 'write': Escribe en el leaderboard actualizando con el nombre del jugador y puntuacion
                             - 'read': Lee y muestra los datos del leaderboard
       """
    #Si no hay un Leaderboard se crea en la primera posibilidad del condicional
    if what_to_do == 'create':
        if estado_app.GameDetails[3] != '':
            if os.path.isfile(direccion_local + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(direccion_local + 'leaderboard.json', 'w'))  # write file

    #En caso de que ya haya sido creado se escribe en el el nuevo puntaje perteneciente al leaderboard
    elif what_to_do == 'write':
        if estado_app.GameDetails[3] != '':  # Solo guarda el puntaje si se dio el nombre del Jugador
            if os.path.isfile(direccion_local + 'leaderboard.json'):
                leaderboard = json.load(open(direccion_local + 'leaderboard.json'))  # read file
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': estado_app.GameDetails[3],
                                                                'HighestScore': estado_app.myscore}
                #Si mis profesores odiaban los "Break" no me imagino como sera cuando vean un Lambda
                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                #Si hay mas de 3 personas en la lista del leaderboard borra a la ultima
                if len(leaderboard) > 3:
                    for i in range(len(leaderboard) - 3): leaderboard.popitem()  # rmv last kdict ey

                json.dump(leaderboard, open(direccion_local + 'leaderboard.json', 'w'))  # write file

    #Este lee los datos guardados en el JSON con los tops
    elif what_to_do == 'read':
        if estado_app.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(direccion_local + 'leaderboard.json'):
                leaderboard = json.load(open(direccion_local + 'leaderboard.json'))  # read file

                leaderboard = dict(
                    sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, columna1, columna2, sc3 = st.columns((2, 3, 3, 3))
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
                            sc3.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")


def InitialPage():
    """
    Brief:
        Configura y muestra la página inicial del juego, incluyendo la barra lateral con la imagen del juego y las instrucciones
        de juego en el área principal, también se presenta la imagen de ayuda y los detalles del autor.
    """
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # Aqui define las reglas
    reglas = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>"""

    #Columna 1 es la derecha, 2 es la izquierda
    columna1, columna2 = st.columns(2)
    random.seed()
    imagen_ayuda_juego = direccion_local + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    imagen_ayuda_juego = Image.open(imagen_ayuda_juego).resize((550, 550))
    columna2.image(imagen_ayuda_juego, use_column_width='auto')

    columna1.subheader('Rules | Playing Instructions:')
    columna1.markdown(horizontal_bar, True)
    columna1.markdown(reglas, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    datalog_autor = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(datalog_autor, unsafe_allow_html=True)


def ReadPictureFile(wch_fl):
    """
    Brief:
        Lee un archivo de imagen desde una ubicación local y lo convierte a base64
        la cual es adecuada para transmisión o almacenamiento en formatos que solo admiten texto, segun google

    Parameters:
        wch_fl (str): El nombre del archivo de imagen que se desea leer. Este nombre debe incluir
                      la extensión del archivo (por ejemplo, 'imagen.jpg')

    Returns:
        str: Una cadena en formato base64 que representa el contenido del archivo de imagen
             Si ocurre un error durante la lectura del archivo, se devuelve una cadena vacía, posible error por eso
             utiliza el try-except??? me enseñaron try-catch pero este señor programa a toda maquina
    """
    try:
        pxfl = f"{direccion_local}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()

    except:
        return ""


def PressedCheck(indice_celda_presionada):
    """
    Brief:
        Verifica si el botón de una celda fue presionado y actualiza el estado del juego respecto a eso
        Aumenta o disminuye la puntuación basada en si la elección del jugador coincide con la imagen requerida

    Parameters:
        indice_celda_presionada (int): Índice de la celda que ha sido presionada. Este índice es utilizado para acceder a la
                     información específica del botón en el diccionario de estado del juego.
    """
    #Si no se ha presionado, se presiona y se añade a las celdas expiradas
    if estado_app.plyrbtns[indice_celda_presionada]['isPressed'] == False:
        estado_app.plyrbtns[indice_celda_presionada]['isPressed'] = True
        estado_app.expired_cells.append(indice_celda_presionada)

        #Si ademas el emoji de la celda es igual al que se busca se suma el puntaje, y que pija es "isTrueFalse"?? perdon??? Gauss?? ayuda
        if estado_app.plyrbtns[indice_celda_presionada]['eMoji'] == estado_app.sidebar_emoji:
            estado_app.plyrbtns[indice_celda_presionada]['isTrueFalse'] = True
            estado_app.myscore += 5
            #Ademas hay bonus por dificultad
            if estado_app.GameDetails[0] == 'Easy':
                estado_app.myscore += 5
            elif estado_app.GameDetails[0] == 'Medium':
                estado_app.myscore += 3
            elif estado_app.GameDetails[0] == 'Hard':
                estado_app.myscore += 1
        #O en caso de que no sea el Emoticon buscado, pues pierde puntos, bastante logico hasta aqui
        else:
            estado_app.plyrbtns[indice_celda_presionada]['isTrueFalse'] = False
            estado_app.myscore -= 1


def ResetBoard():
    """
    Brief:
        Reinicia el tablero del juego asignando nuevos emojis a las celdas no presionadas y garantiza
        que el emoji de la barra lateral esté presente al menos una vez en el tablero

    """
    #Obtiene el total de celdas
    total_cells_per_row_or_col = estado_app.GameDetails[2]

    #Cambia el emoticon del lado izq por un indice aleatorio
    sidebar_emoji_no = random.randint(1, len(estado_app.emoji_bank)) - 1
    #Luego pone el nuevo indice del emoji aleatorio a el emoji de la columna izq
    estado_app.sidebar_emoji = estado_app.emoji_bank[sidebar_emoji_no]

    sidebar_emoji_in_list = False
    #Esto no lo comprendo del t0do...
    for indice_celda_presionada in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(estado_app.emoji_bank)) - 1
        if estado_app.plyrbtns[indice_celda_presionada]['isPressed'] == False:
            vemoji = estado_app.emoji_bank[rndm_no]
            estado_app.plyrbtns[indice_celda_presionada]['eMoji'] = vemoji
            if vemoji == estado_app.sidebar_emoji: sidebar_emoji_in_list = True

    if sidebar_emoji_in_list == False:  # sidebar pix is not on any button; add pix randomly
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in estado_app.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            estado_app.plyrbtns[lptr]['eMoji'] = estado_app.sidebar_emoji


def PreNewGame():
    """
    Brief:
        Prepara el estado inicial para un nuevo juego, estableciendo los valores básicos y seleccionando
        una nueva pool de emojis según la dificultad elegida.

    """
    total_cells_per_row_or_col = estado_app.GameDetails[2]
    estado_app.expired_cells = []
    estado_app.myscore = 0

    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    #Genera la semilla de numeros aleatorios
    random.seed()
    #Dependiendo de la dificultad elige una pool de emojis
    if estado_app.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        estado_app.emoji_bank = locals()[wch_bank]

    elif estado_app.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        estado_app.emoji_bank = locals()[wch_bank]

    elif estado_app.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        estado_app.emoji_bank = locals()[wch_bank]

    estado_app.plyrbtns = {}
    for indice_celda_presionada in range(1, ((total_cells_per_row_or_col ** 2) + 1)): estado_app.plyrbtns[indice_celda_presionada] = {'isPressed': False,
                                                                                               'isTrueFalse': False,
                                                                                               'eMoji': ''}


def ScoreEmoji():
    """
    Brief:
        Determina un emoji segun el estado actual de la puntuación del jugador

    Returns:
        str: Un emoji como cadena de texto que representa visualmente el rango de puntuación actual del jugador.

    Description:
        - Esta función evalúa la puntuación actual almacenada en `estado_app.myscore` y devuelve un emoji correspondiente:
          * '😐' para una puntuación de cero
          * '😏' para puntuaciones entre -1 y -5
          * '☹️' para puntuaciones entre -6 y -10
          * '😖' para puntuaciones menores o iguales a -11
          * '🙂' para puntuaciones entre 1 y 5
          * '😊' para puntuaciones entre 6 y 10
          * '😁' para puntuaciones mayores a 10
    """
    if estado_app.myscore == 0:
        return '😐'
    elif -5 <= estado_app.myscore <= -1:
        return '😏'
    elif -10 <= estado_app.myscore <= -6:
        return '☹️'
    elif estado_app.myscore <= -11:
        return '😖'
    elif 1 <= estado_app.myscore <= 5:
        return '🙂'
    elif 6 <= estado_app.myscore <= 10:
        return '😊'
    elif estado_app.myscore > 10:
        return '😁'


def NewGame():
    """
    Brief:
        Configura y lanza una nueva instancia de juego, incluyendo la preparación de la interfaz de usuario y el tablero,
        y maneja el ciclo de vida del juego incluyendo el refresco de interfaz y la actualización de la puntuación.

    """
    ResetBoard()
    total_cells_per_row_or_col = estado_app.GameDetails[2]

    ReduceGapFromPageTop('sidebar')
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {estado_app.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        st.markdown(contenedor_emoji_grande.replace('|fill_variable|', estado_app.sidebar_emoji), True)

        aftimer = st_autorefresh(interval=(estado_app.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: estado_app.myscore -= 1

        st.info(
            f"{ScoreEmoji()} Score: {estado_app.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(estado_app.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            estado_app.runpage = Main
            st.rerun()

    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Dafaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big

    for i in range(1, (total_cells_per_row_or_col + 1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(tlst)

    for indice_celda_presionada in range(1, (total_cells_per_row_or_col ** 2) + 1):
        if 1 <= indice_celda_presionada <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= indice_celda_presionada <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        globals()['cols' + arr_ref][indice_celda_presionada - mval] = globals()['cols' + arr_ref][indice_celda_presionada - mval].empty()
        if estado_app.plyrbtns[indice_celda_presionada]['isPressed'] == True:
            if estado_app.plyrbtns[indice_celda_presionada]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][indice_celda_presionada - mval].markdown(emoticon_presionado.replace('|fill_variable|', '✅️'), True)

            elif estado_app.plyrbtns[indice_celda_presionada]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][indice_celda_presionada - mval].markdown(emoticon_presionado.replace('|fill_variable|', '❌'), True)

        else:
            vemoji = estado_app.plyrbtns[indice_celda_presionada]['eMoji']
            globals()['cols' + arr_ref][indice_celda_presionada - mval].button(vemoji, on_click=PressedCheck, args=(indice_celda_presionada,),
                                                             key=f"B{indice_celda_presionada}")

    st.caption('')  # vertical filler
    st.markdown(horizontal_bar, True)

    if len(estado_app.expired_cells) == (total_cells_per_row_or_col ** 2):
        Leaderboard('write')

        if estado_app.myscore > 0:
            st.balloons()
        elif estado_app.myscore <= 0:
            st.snow()

        tm.sleep(5)
        estado_app.runpage = Main
        st.rerun()


def Main():
    """
       Brief:
           Función principal que configura y muestra la página de inicio del juego, incluyendo la selección de dificultad
           y la opción de iniciar un nuevo juego.
       """
    #Establece el estilo del markdown
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    #Inicializa la pagina inicial, por redundante que suene
    InitialPage()
    with st.sidebar:
        estado_app.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        estado_app.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        #Si se presiona el boton de new game segun la dificultad selecciona se asignan valores a ciertas variables
        if st.button(f"🕹️ New Game", use_container_width=True):

            if estado_app.GameDetails[0] == 'Easy':
                estado_app.GameDetails[1] = 8  # secs interval
                estado_app.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif estado_app.GameDetails[0] == 'Medium':
                estado_app.GameDetails[1] = 6  # secs interval
                estado_app.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif estado_app.GameDetails[0] == 'Hard':
                estado_app.GameDetails[1] = 5  # secs interval
                estado_app.GameDetails[2] = 8  # total_cells_per_row_or_col

            #Se crea el Leaderboard
            Leaderboard('create')

            #Se utiliza el PreNewGame() para preparar la creacion de un nuevo juego
            PreNewGame()
            estado_app.runpage = NewGame
            st.rerun()

        st.markdown(horizontal_bar, True)


if 'runpage' not in estado_app: estado_app.runpage = Main
estado_app.runpage()