from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

#### Ejercicio 1

def tablero_bien_formado(t : Tablero) -> bool:
    """
    Indica si el tablero *t* está bien formado: tiene ALTO filas y cada fila
    tiene ANCHO casillas.
 
    PRE: True
 
    Args:
        t (Tablero): El tablero para el cual se indica si está bien formado o no.
 
    Returns:
        True si el tablero *t* está bien formado y False si no.
    """
    todas_con_ancho_correcto: bool = True
    fila: list[Casilla]
    for fila in t:
        todas_con_ancho_correcto = todas_con_ancho_correcto and len(fila) == ANCHO
    return len(t) == ALTO and todas_con_ancho_correcto

def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si la posición *pos* pertenece al tablero.
 
    PRE: True
 
    Args:
        pos (Posicion): La posición (fila, columna) que se quiere verificar.
 
    Returns:
        True si 0 <= fila < ALTO y 0 <= columna < ANCHO, y False si no.
    """
    return (0 <= pos.fila < ALTO and 0<= pos.columna < ANCHO )


def movimiento_bien_formado(m : Movimiento) -> bool:
    """
    Indica si el movimiento *m* está bien formado: su origen pertenece al
    tablero y tiene un paso si mueve a secas, o dos si arrastra o empuja.
 
    PRE: True
 
    Args:
        m (Movimiento): El movimiento para el cual se indica si está bien formado o no.
 
    Returns:
        True si el movimiento está bien formado, False si no.
    """
    cantidad_de_pasos_esperada: int
    if m.accion == MOVER_A_SECAS:
        cantidad_de_pasos_esperada = 1
    else:
        cantidad_de_pasos_esperada = 2
    return posicion_en_tablero(m.origen) and len(m.pasos) == cantidad_de_pasos_esperada


def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si el juego *j* está bien formado: su tablero está bien formado y
    los pasos consumidos están entre 0 (inclusive) y MAX_PASOS (exclusive).
 
    PRE: True
 
    Args:
        j (Juego): El juego para el cual se indica si está bien formado o no.
 
    Returns:
        True si el juego está bien formado, False si no.
    """
    return (tablero_bien_formado(j.tablero) and j.pasos_consumidos >= 0 and j.pasos_consumidos < MAX_PASOS)

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    """
    Devuelve la posición contigua a *pos* en la dirección *d*. El resultado
    puede caer fuera del tablero.
 
    PRE: True
 
    Args:
        pos (Posicion): La posición de partida.
        d (Direccion): La dirección en la que se avanza una casilla.
 
    Returns:
        La posición vecina: NORTE suma una fila, SUR la resta, ESTE suma una
        columna y OESTE la resta.
    """
    fila: int = pos.fila
    columna: int = pos.columna
    if d == NORTE:
        fila = fila + 1
    elif d == SUR:
        fila = fila - 1
    elif d == ESTE:
        columna = columna + 1
    else:
        columna = columna - 1
    return Posicion(fila, columna)

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """
    Devuelve el contenido de la casilla ubicada en la posición *p*.
 
    PRE: tablero_bien_formado(t) y posicion_en_tablero(p)
 
    Args:
        t (Tablero): El tablero a consultar.
        p (Posicion): La posición de la casilla.
 
    Returns:
        VACIA si la casilla no tiene pieza, o la Pieza que la ocupa.
    """
    return t[p.fila][p.columna]

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si la posición *pos* pertenece al tablero y su casilla está vacía.
 
    PRE: tablero_bien_formado(t)
        
    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la casilla.
 
    Returns:
        True si *pos* está en el tablero y su casilla está vacía. Si la casilla
        tiene una pieza, o *pos* está fuera del tablero, devuelve False.
    """
    return posicion_en_tablero(pos) and casilla_en_posicion(t, pos) == VACIA

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """
    Indica si en la posición *pos* hay una pieza del color *col*, sea cual
    sea su figura.
 
    PRE: tablero_bien_formado(t)
         (más débil que el del enunciado, que además pide posicion_en_tablero(pos):
         las funciones *_hacia la llaman con vecinas que pueden estar fuera del tablero)
 
    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición a consultar.
        col (Color): El color buscado.
 
    Returns:
        True si en *pos* hay una pieza de color *col*. Si la casilla está vacía,
        tiene una pieza del otro color o *pos* está fuera del tablero, devuelve False.
    """
    return (posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)
            and casilla_en_posicion(t, pos).color == col)


#### Ejercicio 3

def hay_casilla_vacia_hacia(t: Tablero, pos: Posicion, d: Direccion) -> bool:
    """
    Indica si la casilla vecina de la posición *pos* en dirección *d* está vacía.

    PRE: El tablero *t* tiene que ser válido y la posición *pos* tiene que existir en el tablero. 

    Args: 
        t (Tablero): El tablero a consultar. 
        pos (Posición): La posición de la que se quiere consultar su casilla vecina. 
        d (Dirección): La dirección de la casilla vecina respecto de *pos*
    
    Returns: 
        True si la posición vecina de *pos* en dirección *d* está vacía, False si no . 
    """
    return hay_casilla_vacia(t, posicion_vecina_hacia(pos, d))
    
def hay_pieza_amiga_vecina(t: Tablero, pos: Posicion) -> bool:
    """
    Indica si la pieza en posición *pos* tiene una pieza amiga vecina.
    
    PRE: El tablero *t* está bien formado, la posición *pos* existe en el tablero y en la casilla indicada por *pos*
    hay una pieza. 

    Args: 
        t(Tablero): El tablero a consultar. 
        pos(Posición): La posición de la pieza de la cual se quiere saber si tiene una pieza amiga vecina.

    Returns: 
        True si la pieza en posición *pos* tiene una pieza amiga vecina, False si no. 
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    for direccion in [NORTE, SUR, ESTE, OESTE]:
        vecina: Posicion = posicion_vecina_hacia(pos, direccion)
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if casilla != VACIA and casilla.color == pieza.color:
                encontrada = True
    return encontrada
    
def hay_pieza_enemiga_mas_debil_hacia(
    t: Tablero, pos: Posicion, d: Direccion) -> bool:
    """
    Indica si en dirección *d* hay una pieza enemiga más débil.

    PRE: El tablero *t* está bien formado, la posición *pos* existe en el tablero y en la casilla indicada por *pos*
    hay una pieza. 

    Args: 
        t (Tablero): El tablero a consultar. 
        pos (Posición): La posición de la pieza de la cual se quiere saber si tiene una pieza enemiga más débil vecina. 
        d (Dirección): La dirección en la que se quiere consultar si hay una pieza enemiga más débil. 
     
    Returns: 
        True si la pieza en dirección *d* respecto de la posición *pos* es una pieza enemiga más débil que la pieza en  *pos* 
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    vecina: Posicion = posicion_vecina_hacia(pos, d)
    encontrada: bool = False
    if posicion_en_tablero(vecina):
        casilla: Casilla = t[vecina.fila][vecina.columna]
        if casilla != VACIA:
            encontrada = (
                casilla.color != pieza.color
                and fuerza(casilla.figura) < fuerza(pieza.figura))
    return encontrada
        
def hay_pieza_enemiga_mas_fuerte_vecina(
    t: Tablero, pos: Posicion) -> bool:
    """
    Indica si la pieza en posición *pos* tiene una enemiga más fuerte al lado.

    PRE: El tablero *t* está bien formado, la posición *pos* existe en el tablero y en la casilla indicada por *pos*
    hay una pieza. 

    Args: 
        t (Tablero): El tablero a consultar. 
        pos (Posición): La posición de la pieza de la cual se quiere saber si tiene una pieza enemiga más fuerte vecina. 
        d (Dirección): La dirección en la que se quiere consultar si hay una pieza enemiga más vecina.

    Returns: 
        True si la pieza en dirección *d* respecto de la posición *pos* es una pieza enemiga más fuerte que la pieza en *pos* 

    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    for direccion in [NORTE, SUR, ESTE, OESTE]:
        vecina: Posicion = posicion_vecina_hacia(pos, direccion)
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if casilla != VACIA:
                if (casilla.color != pieza.color and fuerza(casilla.figura) > fuerza(pieza.figura)):encontrada = True
    return encontrada
def hay_pieza_congelada(t: Tablero, pos: Posicion) -> bool:
    """
    Indica si la casilla en posición *pos* contiene una pieza congelada.

    PRE: El tablero *t* está bien formado yla posición *pos* existe en el tablero. 

    Args: 
        t(Tablero): El tablero a consultar. 
        pos(Posición): La posición de la pieza de la cual se quiere saber si está congelada. 

    Returns: 
        True si la pieza en la posición *pos* está congelada, False si no. 

    """
    return (
        t[pos.fila][pos.columna] != VACIA
        and hay_pieza_enemiga_mas_fuerte_vecina(t, pos)
        and not hay_pieza_amiga_vecina(t, pos))

#### EJERCICIO 4

def direccion_de_movimiento_habilitada(
    t: Tablero, pos: Posicion, d: Direccion
) -> bool:
    """Indica si la pieza en pos puede moverse hacia d.

    Precondición: hay una pieza en pos.
    """
    pieza: Casilla = casilla_en_posicion(t, pos)
    return not (
        (pieza == Pieza(CONEJO, DORADO) and d == SUR)
        or (pieza == Pieza(CONEJO, PLATEADO) and d == NORTE)
    )


def puede_arrastrar(
    t: Tablero, pos: Posicion, d: Direccion, d_arrastre: Direccion
) -> bool:
    """Indica si la pieza en pos puede arrastrar según las direcciones dadas."""
    return (
        hay_casilla_vacia_hacia(t, pos, d)
        and hay_pieza_enemiga_mas_debil_hacia(t, pos, opuesta(d_arrastre))
    )


def puede_empujar(
    t: Tablero, pos: Posicion, d: Direccion, d_empuje: Direccion
) -> bool:
    """Indica si la pieza en pos puede empujar según las direcciones dadas."""
    enemiga: Posicion = posicion_vecina_hacia(pos, d)
    return (
        hay_pieza_enemiga_mas_debil_hacia(t, pos, d)
        and hay_casilla_vacia_hacia(t, enemiga, d_empuje)
    )


def puede_realizar_accion(t: Tablero, m: Movimiento) -> bool:
    """Indica si las casillas permiten realizar la acción de m."""
    puede: bool

    if m.accion == MOVER_A_SECAS:
        puede = hay_casilla_vacia_hacia(t, m.origen, m.pasos[0])
    elif m.accion == ARRASTRAR:
        puede = puede_arrastrar(t, m.origen, m.pasos[0], m.pasos[1])
    else:
        puede = puede_empujar(t, m.origen, m.pasos[0], m.pasos[1])

    return puede


def puede_realizar_movimiento(j: Juego, m: Movimiento) -> bool:
    """
    Indica si el movimiento *m* puede realizarse en el juego.

    PRE: El juego *j* y el movimiento *m* están bien formados. 

    Args: 
        j(Juego): El juego a consultar. 
        m(Movimiento): El movimiento a verficar si es válido. 
    
    Returns:
        True si el movimiento *m* es válido para el juego *j*. 
    """
    return (
        hay_pieza_de_color(j.tablero, m.origen, j.turno)
        and not hay_pieza_congelada(j.tablero, m.origen)
        and direccion_de_movimiento_habilitada(
            j.tablero, m.origen, m.pasos[0]
        )
        and j.pasos_consumidos + len(m.pasos) <= MAX_PASOS
        and puede_realizar_accion(j.tablero, m)
    )
#### Ejercicio 5

def copiar_tablero(t: Tablero) -> Tablero:
    """Devuelve una copia de t que no comparte filas con el tablero original."""
    res: Tablero = []
    fila: list[Casilla]

    for fila in t:
        res.append(fila.copy())

    return res

def activar_trampas(t : Tablero) -> Tablero:
    """
    Devuelve el tablero con las posiciones trampa ya activadas. 
 
    PRE: El tablero *t* tiene que estar bien formado

    Args: 
        t(Tablero): El tablero del cual se quieren activar las trampas. 

    Returns: 
        El tablero después de haber activado todas las trampas. 
        
    """
    res: Tablero = copiar_tablero(t)
    trampa: Posicion

    for trampa in POSICIONES_TRAMPA:
        if (
            casilla_en_posicion(res, trampa) != VACIA
            and not hay_pieza_amiga_vecina(res, trampa)
        ):
            res[trampa.fila][trampa.columna] = VACIA

    return res


#### Ejercicio 6

def tablero_trasladando_pieza(
    t: Tablero, origen: Posicion, destino: Posicion
) -> Tablero:
    """Devuelve una copia de t con la pieza de origen trasladada a destino."""
    res: Tablero = copiar_tablero(t)
    res[destino.fila][destino.columna] = res[origen.fila][origen.columna]
    res[origen.fila][origen.columna] = VACIA
    return res


def tablero_post_movimiento(t: Tablero, m: Movimiento) -> Tablero:
    """Devuelve el tablero resultante de m luego de activar las trampas."""
    destino: Posicion = posicion_vecina_hacia(m.origen, m.pasos[0])
    resultado: Tablero

    if m.accion == MOVER_A_SECAS:
        resultado = tablero_trasladando_pieza(t, m.origen, destino)
    elif m.accion == ARRASTRAR:
        pos_enemiga: Posicion = posicion_vecina_hacia(
            m.origen, opuesta(m.pasos[1])
        )
        con_la_propia_movida: Tablero = tablero_trasladando_pieza(
            t, m.origen, destino
        )
        resultado = tablero_trasladando_pieza(
            con_la_propia_movida, pos_enemiga, m.origen
        )
    else:
        pos_hueco: Posicion = posicion_vecina_hacia(destino, m.pasos[1])
        con_la_enemiga_empujada: Tablero = tablero_trasladando_pieza(
            t, destino, pos_hueco
        )
        resultado = tablero_trasladando_pieza(
            con_la_enemiga_empujada, m.origen, destino
        )

    return activar_trampas(resultado)


def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    """
    Realiza el movimiento *m* en el juego *j*: mueve, arrastra o empuja según
    la acción, activa las trampas y pasa el turno al oponente si con este
    movimiento el jugador completa sus MAX_PASOS.

    PRE: juego_bien_formado(j), movimiento_bien_formado(m) y
         puede_realizar_movimiento(j, m)

    Args:
        j (Juego): El estado del juego antes del movimiento. No se modifica.
        m (Movimiento): El movimiento a realizar.

    Returns:
        Un juego nuevo, bien formado, con el tablero resultante y el turno y
        los pasos consumidos actualizados.
    """
    tablero_final: Tablero = tablero_post_movimiento(j.tablero, m)
    pasos_totales: int = j.pasos_consumidos + len(m.pasos)
    resultado: Juego
    if pasos_totales == MAX_PASOS:
        resultado = pasar_turno(Juego(tablero_final, j.turno, pasos_totales))
    else:
        resultado = Juego(tablero_final, j.turno, pasos_totales)
    return resultado

#### Ejercicio 7

def hay_conejo_en_tablero(t: Tablero, col: Color) -> bool:
    """Indica si queda al menos un conejo del color col en el tablero."""
    hay_conejo: bool = False
    fila: list[Casilla]

    for fila in t:
        casilla: Casilla

        for casilla in fila:
            if (
                casilla != VACIA
                and casilla.figura == CONEJO
                and casilla.color == col
            ):
                hay_conejo = True

    return hay_conejo


def hay_conejo_en_fila_inicial_oponente(
    t: Tablero, col: Color
) -> bool:
    """Indica si un conejo de col llegó a la fila inicial de su oponente."""
    fila_objetivo: int = 0
    hay_conejo: bool = False
    casilla: Casilla

    if col == DORADO:
        fila_objetivo = ALTO - 1

    for casilla in t[fila_objetivo]:
        if (
            casilla != VACIA
            and casilla.figura == CONEJO
            and casilla.color == col
        ):
            hay_conejo = True

    return hay_conejo

def reune_condiciones_de_ganar(j: Juego, col: Color) -> bool:
    """Indica si el color col cumple alguna condición de victoria."""
    return (
        hay_conejo_en_fila_inicial_oponente(j.tablero, col)
        or not hay_conejo_en_tablero(j.tablero, oponente(col))
    )

def hay_ganador_determinado(j: Juego) -> bool:
    """Indica si existe un ganador determinado al inicio de un turno."""
    return (
        j.pasos_consumidos == 0
        and (
            reune_condiciones_de_ganar(j, DORADO)
            or reune_condiciones_de_ganar(j, PLATEADO)
        ))
    

def ganador_del_juego(j : Juego) -> Color:
    """
    Devuelve el color ganador del juego.
    Precondición: hay_ganador_determinado(j).  
    """  
    jugador_anterior: Color = oponente(j.turno)
    ganador: Color = j.turno
    if reune_condiciones_de_ganar(j, jugador_anterior):
        ganador = jugador_anterior
    return ganador




