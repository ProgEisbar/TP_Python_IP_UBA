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
 
# Lo dejo con un solo return.
# len(t) == ALTO se volvía a evaluar en cada vuelta, junto con la del ancho.
# Ahora son condiciones aparte.
# Recorre directamente la secuencia con el for. 

def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si la posición *pos* pertenece al tablero.
 
    PRE: True
 
    Args:
        pos (Posicion): La posición (fila, columna) que se quiere verificar.
 
    Returns:
        True si 0 <= fila < ALTO y 0 <= columna < ANCHO, y False si no.
    """
    return (pos.fila >= 0 and pos.fila < ALTO and pos.columna >= 0 and pos.columna < ANCHO )
 
# Elimino el if que devuelve True en una rama y False en la otra, para no caer en lo que el PDF llama miedo al booleano.
# La condición ya es un booleano en sí misma. Y así queda un solo return.

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
 
# Simplifico un poco. Las tres ramas devolvían True y tanto Arrastrar como Empujar piden lo mismo, pueden compartir rama.
# Separa cuantos pasos corresponden a la acción y si el mov cumple además con tener origen en el tablero.
# Accion solo tres valores, entonces el else es Arrastrar o Empujar.

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
 
# Al desempaquetar  (tablero,color,pasosConsumidos) = j se creaba la variable color, pero no se usaba.
# Con el and ya hace la evaluación lógica
# Cambié el nombre pasosConsumidos por pasos_consumidos, del código.


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
 
#  Devolvía una tupla (fila, columna) y no una posición. Eso complicaba la escritura en el 3, con Posición(*posicion_vecina_... etc). Ya no se necesitan los *
# En cada rama asignaba pos_final. Ahora parte de fila y columna y las modifica si corresponde, recién al final construye Posicion.

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
 
# La condición en el return ya hace la evaluación lógica que antes estaba en el if. (lo del miedo al booleano)
# Antes tenía if pero no else. Sin el else, cuando la casilla está ocupada, termina sin return.
 
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
    # La primera condición protege el acceso a la casilla: si pos está fuera
    # del tablero, "and" no evalúa las demás.
    return (posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)
            and casilla_en_posicion(t,pos).color == col)
 
# Antes con la casilla vacía no entraba en ningyna rama. 
# Quito el desempaquetado, que creaba la variable figura que después no se usa. 

#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si la casilla contigua a *pos* en la dirección *d* existe y está vacía.

    PRE: tablero_bien_formado(t) y posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de partida.
        d (Direccion): La dirección en la que se mira.

    Returns:
        True si la vecina hacia *d* está dentro del tablero y vacía. Si la
        vecina cae fuera del tablero, devuelve False.
    """
    return hay_casilla_vacia(t, posicion_vecina_hacia(pos,d))

# Corrijo, a partir del cambio en el ejercicio 2 ya no se necesitan los * ni la variable vecina.

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si la pieza de *pos* tiene, en alguna de las cuatro direcciones,
    una pieza de su mismo color.

    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*

    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza.

    Returns:
        True si alguna vecina ortogonal es una pieza amiga, y False si no.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    direccion: Direccion
    for direccion in [NORTE, SUR, ESTE, OESTE]:
        vecina: Posicion = posicion_vecina_hacia(pos, direccion)
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if casilla != VACIA and casilla.color == pieza.color:
                encontrada = True
    return encontrada

# Igual que en el ejercicio anterior, sin los * paso de Posicion(*posicion_vecina_hacia(pos, direccion))a posicion_vecina_hacia(pos, direccion)
# Anoto la variable dirección del for


def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si la casilla contigua a *pos* en la dirección *d* tiene una pieza
    enemiga de fuerza estrictamente menor que la pieza de *pos*.

    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*

    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza.
        d (Direccion): La dirección en la que se mira.

    Returns:
        True si hacia *d* hay una enemiga más débil, y False si no.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    vecina: Posicion = posicion_vecina_hacia(pos, d)
    encontrada: bool = False
    if posicion_en_tablero(vecina):
        casilla: Casilla = t[vecina.fila][vecina.columna]
        if casilla != VACIA:
            encontrada = (casilla.color != pieza.color
                          and fuerza(casilla.figura) < fuerza(pieza.figura))
    return encontrada

# Cambio, como en los anteriores, Posicion(*...)

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si la pieza de *pos* tiene, en alguna de las cuatro direcciones,
    una pieza enemiga de fuerza estrictamente mayor.

    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*

    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza.

    Returns:
        True si alguna vecina ortogonal es una enemiga más fuerte, y False si no.
    """
    pieza: Casilla = t[pos.fila][pos.columna]
    encontrada: bool = False
    direccion: Direccion
    for direccion in [NORTE,SUR,ESTE,OESTE]:
        vecina: Posicion = posicion_vecina_hacia(pos,direccion)
        if posicion_en_tablero(vecina):
            casilla: Casilla = t[vecina.fila][vecina.columna]
            if (casilla != VACIA and casilla.color != pieza.color and fuerza(casilla.figura) >fuerza(pieza.figura)):
                encontrada = True
    return encontrada

# Reduje los anidamientos de 4 niveles (for + 3 if) a 3 (for + 2 if) utilizando un and.  
# Si la casilla está vacía, el and corta antes de pedir .color o .figura.


def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si en *pos* hay una pieza congelada: tiene una enemiga más fuerte
    al lado y ninguna amiga al lado.

    PRE: tablero_bien_formado(t) y posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición a consultar.

    Returns:
        True si en *pos* hay una pieza congelada. Si la casilla está vacía,
        devuelve False.
    """
    return (not hay_casilla_vacia(t,pos)
            and hay_pieza_enemiga_mas_fuerte_vecina(t,pos)
            and not hay_pieza_amiga_vecina(t,pos))

# Solo cambio t[pos.fila][pos.columna] != VACIA a not hay_casilla_vacia para reutilizar la función.


#### Ejercicio 4
 
# Para que quede menos largo, más fácil de leer y sin tantos if en una sola función, lo modularicé. 
# Así al final puedeRealizarMovimiento termina siendo una unión  con and de cinco condiciones 
# Evita alias como t y pos para j.tablero y m.origen
# Como en los anteriores, ya no aparece Posicion(*...)
 
 
def direccion_de_movimiento_habilitada(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si la pieza de *pos* puede avanzar hacia *d* según su figura. Los
    conejos no retroceden: el dorado no va hacia el SUR y el plateado no va
    hacia el NORTE. Las demás figuras pueden ir hacia cualquier dirección.
 
    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*
 
    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza.
        d (Direccion): La dirección del movimiento.
 
    Returns:
        True si la pieza no estaría retrocediendo, y False si es un conejo
        yendo hacia atrás.
    """
    es_conejo_dorado: bool = casilla_en_posicion(t, pos) == Pieza(CONEJO, DORADO)
    es_conejo_plateado: bool = casilla_en_posicion(t, pos) == Pieza(CONEJO, PLATEADO)
    return (not (es_conejo_dorado and d == SUR)
            and not (es_conejo_plateado and d == NORTE))
 
def puede_arrastrar(t : Tablero, pos : Posicion, d : Direccion, darrastre : Direccion) -> bool:
    """
    Indica si la pieza de *pos* puede avanzar hacia *d* (casilla vacía)
    arrastrando a una enemiga más débil. La arrastrada está del lado opuesto
    a *darrastre*: se mueve hacia *darrastre* y ocupa el lugar que deja la
    pieza que se mueve.
 
    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*
 
    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza que se mueve.
        d (Direccion): La dirección en la que avanza la pieza que se mueve.
        darrastre (Direccion): La dirección en la que se mueve la pieza arrastrada.
 
    Returns:
        True si el arrastre es posible, y False si no.
    """
    return (hay_casilla_vacia_hacia(t, pos, d)
            and hay_pieza_enemiga_mas_debil_hacia(t, pos, opuesta(darrastre)))
 
def puede_empujar(t : Tablero, pos : Posicion, d : Direccion, dempuje : Direccion) -> bool:
    """
    Indica si la pieza de *pos* puede avanzar hacia *d* empujando a la enemiga
    más débil que ocupa esa casilla hacia una casilla vacía (en la dirección
    *dempuje*).
 
    PRE: tablero_bien_formado(t), posicion_en_tablero(pos) y hay una pieza en *pos*
 
    Args:
        t (Tablero): El tablero a consultar.
        pos (Posicion): La posición de la pieza que se mueve.
        d (Direccion): La dirección en la que avanza la pieza que se mueve.
        dempuje (Direccion): La dirección en la que se mueve la pieza empujada.
 
    Returns:
        True si el empuje es posible, y False si no.
    """
    return (hay_pieza_enemiga_mas_debil_hacia(t, pos, d)
            and hay_casilla_vacia_hacia(t, posicion_vecina_hacia(pos, d), dempuje))
 
def puede_realizar_accion(t : Tablero, m : Movimiento) -> bool:
    """
    Indica si la acción del movimiento *m* (mover a secas, arrastrar o
    empujar) es posible sobre el tablero. No considera de quién es el turno,
    ni el congelamiento, ni la cantidad de pasos.
 
    PRE: tablero_bien_formado(t), movimiento_bien_formado(m) y hay una pieza
         en el origen de *m*
 
    Args:
        t (Tablero): El tablero a consultar.
        m (Movimiento): El movimiento a analizar.
 
    Returns:
        True si las casillas involucradas permiten la acción, y False si no.
    """
    puede: bool
    if m.accion == MOVER_A_SECAS:
        puede = hay_casilla_vacia_hacia(t, m.origen, m.pasos[0])
    elif m.accion == ARRASTRAR:
        puede = puede_arrastrar(t, m.origen, m.pasos[0], m.pasos[1])
    else:
        puede = puede_empujar(t, m.origen, m.pasos[0], m.pasos[1])
    return puede
 
def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    """
    Indica si el jugador al que le toca puede realizar el movimiento *m*:
    mueve una pieza propia que no está congelada, hacia una dirección que su
    figura permite, sin superar MAX_PASOS en el turno y con la acción posible
    sobre el tablero.
 
    PRE: juego_bien_formado(j) y movimiento_bien_formado(m)
 
    Args:
        j (Juego): El estado actual del juego.
        m (Movimiento): El movimiento propuesto.
 
    Returns:
        True si el movimiento es legal en *j*, y False si no.
    """
    return (hay_pieza_de_color(j.tablero, m.origen, j.turno)
            and not hay_pieza_congelada(j.tablero, m.origen)
            and direccion_de_movimiento_habilitada(j.tablero, m.origen, m.pasos[0])
            and j.pasos_consumidos + len(m.pasos) <= MAX_PASOS
            and puede_realizar_accion(j.tablero, m))
 
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

