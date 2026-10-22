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
    Indica si el tablero *t* está bien formado. 
    
    PRE: True 

    Args: 
        t (Tablero): La matriz para el cual se indice si está bien formado o no. 
    
    Returns:
        True si el tablero *t* está bien formado y False si no. 
    """
    esta_bien_formado:bool = False
    for i in range(len(t)): 
        if len(t[i]) == ANCHO and len(t)==ALTO: 
            esta_bien_formado = True
        else: 
            return False
    return esta_bien_formado

def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si la posición *pos* está en el tablero. 

    PRE: True 

    Args: 
        pos (Posicion): La tupla con valores de fila y columna que se quiere 
        verificar si está en el tablero. 
    
    Returns: 
        True si la posición está en el tablero y False si no. 
    """
    (fila,columna) = pos 
    if 0 <= fila < ALTO and 0 <= columna < ANCHO: 
        return True 
    else: 
        return False 


def movimiento_bien_formado(m : Movimiento) -> bool:
    """
    Indica si el movimiento *m* está bien formado. 

    PRE: True

    Args: 
        m (Movimiento): El movimiento el cual se quiere indicar si está bien formado o no.

    Returns:
        True si el movimiento está bien formado, False si no.
    """
    (accion,origen,pasos) = m 
    res:bool= False
    if posicion_en_tablero(origen):
        if accion == MOVER_A_SECAS and len(pasos)==1:
            res = True
        elif accion == ARRASTRAR and len(pasos)==2:
            res = True 
        elif accion == EMPUJAR and len(pasos)==2:
            res = True 
        else: 
            return False 
    return res 
        

def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si el juego *j* está bien formado. 

    PRE: True 

    Args: 
        j(Juego): El juego para el cual se quiere determinar si está bien formado. 

    Returns: 
        True si el juego está bien formado, False si no. 
    
    """
    (tablero,color,pasosConsumidos) = j 
    if tablero_bien_formado(tablero) and 0 <= pasosConsumidos < MAX_PASOS:
        return True
    else: 
        return False 

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    """
    Indica la posición vecina de la posición *pos* en dirección *d*. 

    PRE: True

    Args: 
        pos(Posicion): Posición para la cual se quiere determinar su posición vecina en dirección *d*.
        d(Dirección): Dirección de la casilla vecina en relación a posición *pos*. 

    Returns: 
        Posición de la posición vecina en dirección *d*. 

    """
    (fila,columna) = pos 
    if d == NORTE: 
        pos_final = (fila+1,columna)
    elif d == SUR: 
        pos_final = (fila-1,columna)
    elif d == ESTE:
        pos_final = (fila,columna+1)
    else: 
        pos_final = (fila,columna-1)
    return pos_final 

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    (fila,columna) = p 
    return t[fila][columna]

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    if casilla_en_posicion(t,pos) == VACIA:
        return True 

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    if not hay_casilla_vacia(t,pos): 
        (figura,color) = casilla_en_posicion(t,pos)
        if color == col: 
            return True
        else: 
            return False

#### Ejercicio 3

def hay_casilla_vacia_hacia(
    t: Tablero, pos: Posicion, d: Direccion) -> bool:
    """
    Indica si la casilla vecina en la dirección d está vacía.
    """
    vecina: Posicion = Posicion(*posicion_vecina_hacia(pos, d))
    return (
        posicion_en_tablero(vecina)
        and t[vecina.fila][vecina.columna] == VACIA
    )
def hay_pieza_amiga_vecina(t: Tablero, pos: Posicion) -> bool:
    """
    Indica si la pieza en pos tiene una pieza amiga vecina.
    Precondición: la casilla pos contiene una pieza.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    for direccion in [NORTE, SUR, ESTE, OESTE]:
        vecina: Posicion = Posicion(
            *posicion_vecina_hacia(pos, direccion)
        )
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if casilla != VACIA and casilla.color == pieza.color:
                encontrada = True
    return encontrada
def hay_pieza_enemiga_mas_debil_hacia(
    t: Tablero, pos: Posicion, d: Direccion) -> bool:
    """
    Indica si en dirección d hay una pieza enemiga más débil.
    Precondición: la casilla pos contiene una pieza.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    vecina: Posicion = Posicion(*posicion_vecina_hacia(pos, d))
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
    Indica si la pieza en pos tiene una enemiga más fuerte al lado.
    Precondición: la casilla pos contiene una pieza.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    for direccion in [NORTE, SUR, ESTE, OESTE]:
        vecina: Posicion = Posicion(*posicion_vecina_hacia(pos, direccion))
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if casilla != VACIA:
                if (casilla.color != pieza.color and fuerza(casilla.figura) > fuerza(pieza.figura)):encontrada = True
    return encontrada
def hay_pieza_congelada(t: Tablero, pos: Posicion) -> bool:
    """
    Indica si la casilla pos contiene una pieza congelada.
    """
    return (
        t[pos.fila][pos.columna] != VACIA
        and hay_pieza_enemiga_mas_fuerte_vecina(t, pos)
        and not hay_pieza_amiga_vecina(t, pos))

#### EJERCICIO 4

def puede_realizar_movimiento(j: Juego, m: Movimiento) -> bool:
    """
    Indica si el movimiento puede realizarse en el juego.
    Precondición: j y m están bien formados.
    """
    t: Tablero = j.tablero
    pos: Posicion = m.origen
    pieza: Casilla = t[pos.fila][pos.columna]
    puede: bool = False
    if pieza != VACIA and pieza.color == j.turno:
        direccion_valida: bool = not (
            pieza.figura == CONEJO
            and (
                (pieza.color == DORADO and m.pasos[0] == SUR)
                or (pieza.color == PLATEADO and m.pasos[0] == NORTE))
        if (
            not hay_pieza_congelada(t, pos)
            and direccion_valida
            and j.pasos_consumidos + len(m.pasos) <= MAX_PASOS):
            if m.accion == MOVER_A_SECAS:
                puede = hay_casilla_vacia_hacia(t, pos, m.pasos[0])
            elif m.accion == ARRASTRAR:
                puede = (
                    hay_casilla_vacia_hacia(t, pos, m.pasos[0])
                    and hay_pieza_enemiga_mas_debil_hacia(
                        t, pos, opuesta(m.pasos[1])))
            elif m.accion == EMPUJAR:
                if hay_pieza_enemiga_mas_debil_hacia(t, pos, m.pasos[0]):
                    enemiga: Posicion = Posicion(
                        *posicion_vecina_hacia(pos, m.pasos[0])
                    )
                    puede = hay_casilla_vacia_hacia(t, enemiga, m.pasos[1])
    return puede
#### Ejercicio 5

def activar_trampas(t : Tablero) -> Tablero:
    raise Exception("No implementado")

#### Ejercicio 6

def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    raise Exception("No implementado")

#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")

