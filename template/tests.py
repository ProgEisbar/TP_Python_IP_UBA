import unittest
from arimaa import *

# Las piezas se representan con las siguientes letras:
#   E : elefante
#   M : camello
#   H : caballo
#   D : perro
#   C : gato
#   R : ratón
# donde
#   mayúscula : dorado
#   minúscula : plateado

def tablero_8x8_vacio():
    return leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])

def tablero_8x8_inicial_ejemplo():
    return leer_tablero([
              'hcdmedch', #7
              'rrrrrrrr', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              'RRRRRRRR', #1
              'HCDMEDCH', #0
              #01234567
            ])

def tablero_6x8():
    return leer_tablero([
        '--------', #5
        '--------', #4
        '--------', #3
        '--------', #2
        'RRRRRRRR', #1
        'HCDMEDCH', #0
        #01234567
    ])

def tablero_8x6():
    return leer_tablero([
            "------"  #7
            "------"  #6
            '------', #5
            '------', #4
            '------', #3
            '------', #2
            'RRRRRR', #1
            'HCDMED', #0
            #01234567
        ])

def tablero_deforme():
    return leer_tablero([
            "--------"  #6
            '--------', #5
            '-------', #4
            '------ee', #3
            '------hh', #2
            'RRRRRRRR', #1
            'HCDMED', #0
            #01234567
        ])


#### Ejercicio 1

class test_tablero_bien_formado(unittest.TestCase):

    def test_8x8_lleno(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(tablero_bien_formado(t))

    def test_falta_una_fila(self):
        t = tablero_6x8()
        self.assertFalse(tablero_bien_formado(t))

    def test_falta_una_columna(self):
        t = tablero_8x6()
        self.assertFalse(tablero_bien_formado(t))

    def test_distintos_largos_de_fila(self):
        t = tablero_deforme()
        self.assertFalse(tablero_bien_formado(t))


class test_posicion_en_tablero(unittest.TestCase):

    def test_posicion_ok(self):
        self.assertTrue(posicion_en_tablero(Posicion(5, 3)))

    def test_posicion_negativa(self):
        self.assertFalse(posicion_en_tablero(Posicion(-1,-2)))

    def test_falla_alto(self):
        self.assertFalse(posicion_en_tablero(Posicion(10,0)))
    
    def test_falla_ancho(self):
        self.assertFalse(posicion_en_tablero(Posicion(0,10)))

class test_movimiento_bien_formado(unittest.TestCase):

    def test_movimiento_ok(self):
        self.assertTrue(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])))

    def test_falla_pasos(self):
        self.assertFalse(movimiento_bien_formado(Movimiento(ARRASTRAR,Posicion(1,0),[NORTE])))
    
    def test_falla_posicion(self):
        self.assertFalse(movimiento_bien_formado(Movimiento(EMPUJAR,Posicion(16,2),[ESTE,NORTE])))
    

class test_juego_bien_formado(unittest.TestCase):

    def test_juego_ok(self):
        j = Juego(tablero_8x8_vacio(), DORADO, 0)
        self.assertTrue(juego_bien_formado(j))

    def test_juego_no_ok(self):
        j = Juego(tablero_8x8_inicial_ejemplo(),PLATEADO,5)
        self.assertFalse(juego_bien_formado(j))

    
#### Ejercicio 2

class test_posicion_vecina_hacia(unittest.TestCase):

    def test_vecina_al_norte(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), NORTE), Posicion(1, 0))
    
    def test_vecina_al_sur(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(1,0),SUR),Posicion(0,0))
    
    def test_vecina_al_este(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0,0),ESTE),Posicion(0,1))

    def test_vecina_al_oeste(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0,1),OESTE),Posicion(0,0))

class test_son_posiciones_vecinas(unittest.TestCase):

    def test_vecinas(self):
        self.assertTrue(son_posiciones_vecinas(Posicion(0, 0), Posicion(1, 0)))

class test_casilla_en_posicion(unittest.TestCase):

    def test_casilla_en_posicion(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 0)), Pieza(CABALLO, DORADO))
    
    def test_casilla_vacia(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t,Posicion(4,0)),VACIA)

class test_hay_casilla_vacia(unittest.TestCase):

    def test_casilla_vacia(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_casilla_vacia(t, Posicion(2, 1)))
    
    def test_falla_posicion(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_casilla_vacia(t,Posicion(0,10)))

class test_hay_pieza_de_color(unittest.TestCase):

    def test_hay_pieza_de_color_ok(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_pieza_de_color(t, Posicion(1, 4), DORADO))
    
    def test_no_hay_pieza_de_ese_color(self):
        t = tablero_8x8_inicial_ejemplo() 
        self.assertFalse(hay_pieza_de_color(t,Posicion(7,1),DORADO))
    
    def test_falla_posicion(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_pieza_de_color(t,Posicion(10,0),PLATEADO))

#### Ejercicio 3

class test_hay_casilla_vacia_hacia(unittest.TestCase):

    def test_hay_casilla_vacia_hacia(self):
        t = leer_tablero([
              '-r----rr', #7
              '-mrh----', #6
              '-r---r--', #5
              'd-EH---c', #4
              '-M--hD-d', #3
              '-R-e----', #2
              '---H-R-C', #1
              'R-R---RR', #0
              #01234567
            ])
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))

    def test_casilla_ocupada_o_fuera_del_tablero(self):
        t = tablero_8x8_vacio()
        t[0][0] = Pieza(CONEJO, DORADO)
        t[1][0] = Pieza(CONEJO, PLATEADO)

        self.assertFalse(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))
        self.assertFalse(hay_casilla_vacia_hacia(t, Posicion(0, 0), SUR))

class test_hay_pieza_amiga_vecina(unittest.TestCase):

    def test_hay_pieza_amiga_vecina(self):
        t = leer_tablero([
              'R-hRD-Rr', #7
              'M----d--', #6
              '-h-rrCR-', #5
              'R-rcE---', #4
              '--drRR--', #3
              '-HD-H--m', #2
              '--r-RCc-', #1
              're---r--', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_amiga_vecina(t, Posicion(4, 3)))

    def test_no_hay_pieza_amiga_vecina(self):
        t = tablero_8x8_vacio()
        t[0][0] = Pieza(GATO, DORADO)
        t[0][1] = Pieza(GATO, PLATEADO)

        self.assertFalse(hay_pieza_amiga_vecina(t, Posicion(0, 0)))

class test_hay_pieza_enemiga_mas_debil_hacia(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_debil_hacia(self):
        t = leer_tablero([
              '--Hdm---', #7
              'r--HhC--', #6
              'e---R-C-', #5
              'ME--d---', #4
              'h--RDcRr', #3
              'R-R-r--r', #2
              '-RRcrRD-', #1
              '--r---rr', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 3), OESTE))

    def test_no_hay_enemiga_mas_debil(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(CABALLO, DORADO)
        t[3][4] = Pieza(CABALLO, PLATEADO)

        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(3, 3), ESTE))
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(3, 3), NORTE))

class test_hay_pieza_enemiga_mas_fuerte_vecina(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_fuerte_vecina(self):
        t = leer_tablero([
              'R-e--mRr', #7
              '------dE', #6
              'h--Rr-RR', #5
              'c--R-C--', #4
              '-rCHDrr-', #3
              '----rc--', #2
              'h-R-M-R-', #1
              'rr-D-dH-', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_enemiga_mas_fuerte_vecina(t, Posicion(3, 1)))

    def test_no_hay_enemiga_mas_fuerte_vecina(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(CABALLO, DORADO)
        t[3][4] = Pieza(PERRO, PLATEADO)
        t[4][3] = Pieza(ELEFANTE, DORADO)

        self.assertFalse(hay_pieza_enemiga_mas_fuerte_vecina(t, Posicion(3, 3)))

class test_hay_pieza_congelada(unittest.TestCase):

    def test_hay_pieza_congelada(self):
        t = leer_tablero([
              '--d--H-D', #7
              '-hMc--r-', #6
              '--r--C-H', #5
              '--------', #4
              '-CeD----', #3
              '---R----', #2
              '--------', #1
              '--------', #0
              #01234567
            ])
        self.assertTrue(hay_pieza_congelada(t, Posicion(6, 1)))

    def test_una_amiga_vecina_descongela_la_pieza(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(GATO, DORADO)
        t[3][4] = Pieza(ELEFANTE, PLATEADO)
        t[3][2] = Pieza(CONEJO, DORADO)

        self.assertFalse(hay_pieza_congelada(t, Posicion(3, 3)))
        self.assertFalse(hay_pieza_congelada(t, Posicion(0, 0)))

#### Ejercicio 4

class test_puede_realizar_movimiento(unittest.TestCase):

    def test_mover_a_secas_ok(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j, m))

    def test_no_puede_mover_una_pieza_del_oponente(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(GATO, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [NORTE])

        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_conejo_dorado_no_puede_retroceder(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(CONEJO, DORADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [SUR])

        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_conejo_plateado_no_puede_retroceder(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [NORTE])

        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_puede_mover_si_supera_los_pasos_del_turno(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[3][2] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, DORADO, 3)
        m = Movimiento(ARRASTRAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_no_puede_mover_una_pieza_congelada(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(GATO, DORADO)
        t[3][4] = Pieza(ELEFANTE, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [NORTE])

        self.assertFalse(puede_realizar_movimiento(j, m))

    def test_puede_arrastrar_una_pieza_enemiga_mas_debil(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[3][2] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(ARRASTRAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertTrue(puede_realizar_movimiento(j, m))

    def test_puede_empujar_una_pieza_enemiga_mas_debil(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[4][3] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(EMPUJAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertTrue(puede_realizar_movimiento(j, m))

    def test_no_puede_empujar_si_el_destino_esta_ocupado(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[4][3] = Pieza(CONEJO, PLATEADO)
        t[4][4] = Pieza(GATO, DORADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(EMPUJAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertFalse(puede_realizar_movimiento(j, m))

#### Ejercicio 5

class test_activar_trampas(unittest.TestCase):

    def test_activar_trampas_ok(self):
        t0 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-r--E--', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-H--m--', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t1 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-------', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-------', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t2 = activar_trampas(t0)
        self.assertNotEqual(t0, t1)
        self.assertEqual(t2, t1)

    def test_la_trampa_no_modifica_el_tablero_original(self):
        t = tablero_8x8_vacio()
        t[2][2] = Pieza(GATO, DORADO)

        resultado = activar_trampas(t)

        self.assertEqual(t[2][2], Pieza(GATO, DORADO))
        self.assertEqual(resultado[2][2], VACIA)

class casilla_trampa_con_aliado_vecino(unittest.TestCase):
    def test_pieza_vecina_dorados(self):
        t0 = leer_tablero([   
               '-eRD--dr', #7
               '--M--R--', #6
               'H-D--R--', #5
               '-H---rCr', #4
               'R-------', #3
               '--R--H--', #2
               '--R--E--', #1
               'c-D---R-', #0
        ])
        t1 = leer_tablero([
               '-eRD--dr', #7
               '--M--R--', #6
               'H-D--R--', #5
               '-H---rCr', #4
               'R-------', #3
               '--R--H--', #2
               '--R--E--', #1
               'c-D---R-', #0
        ])
        t2 = activar_trampas(t0)
        self.assertEqual(t2,t1)

    def test_pieza_vecina_plateadas(self):
        t0 = leer_tablero([
            '-eRD--dr', #7
            '--m-----', #6
            'H-dD-rE-', #5
            '-H---c--', #4
            'R-------', #3
            '-rc--hm-', #2
            '--R--E--', #1
            'c-D---R-', #0
            #01234567
            ])
        t1 = leer_tablero([
            '-eRD--dr', #7
            '--m-----', #6
            'H-dD-rE-', #5
            '-H---c--', #4
            'R-------', #3
            '-rc--hm-', #2
            '--R--E--', #1
            'c-D---R-', #0
            #01234567
            ])
        t2 = activar_trampas(t0)
        self.assertEqual(t2,t1)

class test_tablero_vacio_igual(unittest.TestCase):
    def test_tablero_vacio8x8(self):
        t0= tablero_8x8_vacio()
        t1=tablero_8x8_vacio()
        t2= activar_trampas(t0)
        self.assertEqual(t2,t1)
    
#### Ejercicio 6

class test_realizar_movimiento(unittest.TestCase):
 
    def test_mover_a_secas(self):
        t0 = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '--------', #5
               '---m----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        tN = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '---m----', #5
               '--------', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        j0 = Juego(t0, PLATEADO, 0) 
        jN = Juego(tN, PLATEADO, 1) 
        mN = Movimiento(MOVER_A_SECAS, Posicion(4, 3), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, mN))
        self.assertEqual(realizar_movimiento(j0, mN), jN)

    def test_arrastrar(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[3][2] = Pieza(CONEJO, PLATEADO)
        esperado = tablero_8x8_vacio()
        esperado[4][3] = Pieza(ELEFANTE, DORADO)
        esperado[3][3] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(ARRASTRAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertEqual(
            realizar_movimiento(j, m), Juego(esperado, DORADO, 2)
        )

    def test_empujar(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(ELEFANTE, DORADO)
        t[4][3] = Pieza(CONEJO, PLATEADO)
        esperado = tablero_8x8_vacio()
        esperado[4][3] = Pieza(ELEFANTE, DORADO)
        esperado[4][4] = Pieza(CONEJO, PLATEADO)
        j = Juego(t, DORADO, 0)
        m = Movimiento(EMPUJAR, Posicion(3, 3), [NORTE, ESTE])

        self.assertEqual(
            realizar_movimiento(j, m), Juego(esperado, DORADO, 2)
        )

    def test_cuarto_paso_cambia_el_turno(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(GATO, DORADO)
        esperado = tablero_8x8_vacio()
        esperado[4][3] = Pieza(GATO, DORADO)
        j = Juego(t, DORADO, 3)
        m = Movimiento(MOVER_A_SECAS, Posicion(3, 3), [NORTE])

        self.assertEqual(
            realizar_movimiento(j, m), Juego(esperado, PLATEADO, 0)
        )

#### Ejercicio 7

class test_hay_conejo_en_tablero(unittest.TestCase):

    def test_tablero_sin_conejos(self):
        self.assertFalse(hay_conejo_en_tablero(tablero_8x8_vacio(), DORADO))

    def test_hay_un_conejo_del_color(self):
        t = tablero_8x8_vacio()
        t[3][3] = Pieza(CONEJO, DORADO)
        self.assertTrue(hay_conejo_en_tablero(t, DORADO))


class test_hay_conejo_en_fila_inicial_oponente(unittest.TestCase):

    def test_conejo_dorado_en_la_fila_7(self):
        t = tablero_8x8_vacio()
        t[7][4] = Pieza(CONEJO, DORADO)
        self.assertTrue(hay_conejo_en_fila_inicial_oponente(t, DORADO))

    def test_otra_figura_en_la_fila_no_cuenta(self):
        t = tablero_8x8_vacio()
        t[7][4] = Pieza(ELEFANTE, DORADO)     
        self.assertFalse(hay_conejo_en_fila_inicial_oponente(t, DORADO))


class test_ganador_del_juego(unittest.TestCase):

    def test_promueve_conejo_dorado_turno_del_oponente(self):
        t = leer_tablero([
              'rr----Rr', #7
              'c-----me', #6
              '---Ed-R-', #5
              '-M---R--', #4
              '---R----', #3
              '-rrrr---', #2
              '-H---DCC', #1
              'R-----RR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        self.assertTrue(hay_ganador_determinado(j))
        self.assertEqual(ganador_del_juego(j), DORADO)

