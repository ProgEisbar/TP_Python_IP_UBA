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
    res:bool = False
    for i in range(t): 
        if len(t[i]) == ANCHO and len(t)==ALTO: 
            res = True
        else: 
            return False
    return res

def posicion_en_tablero(pos : Posicion) -> bool:
    for (fila,columna) in pos: 
        if 0 <= fila < ALTO and 0 <= columna < ANCHO: 
            return True 
        else: 
            return False 


def movimiento_bien_formado(m : Movimiento) -> bool:
    for (accion,origen,pasos) in m: 
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
    (tablero,color,pasosConsumidos) = j 
    if tablero_bien_formado(tablero) and 0 <= pasosConsumidos < MAX_PASOS:
        return True
    else: 
        return False 

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
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

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    raise Exception("No implementado")

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

#### Ejercicio 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    raise Exception("No implementado")

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

