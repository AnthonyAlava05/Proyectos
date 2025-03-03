from xmlrpc.server import SimpleXMLRPCServer
import random
import os
import pygame

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()
pygame.mixer.init()

soundtrack = pygame.mixer.Sound("soundtrack.mp3")
inicio = pygame.mixer.Sound("inicio.mp3")
winning = pygame.mixer.Sound("winning.mp3")

JUGADOR_1 = "J1"
JUGADOR_2 = "J2"
DISPAROS_INICIALES = 50
MATRIZ_TAMANIO = 10
MAR = "~"
DISPARO_FALLADO = "O"
DISPARO_ACERTADO = "X"
BARCOS = {
    "portaaviones": 5,
    "acorazado": 4,
    "crucero": 3,
    "submarino": 3,
    "destructor": 2,
}

def obtener_matriz_inicial():
    return [[MAR for _ in range(MATRIZ_TAMANIO)] for _ in range(MATRIZ_TAMANIO)]

def colocar_barcos_aleatorios(matriz, jugador):
    for barco, tamano in BARCOS.items():
        colocado = False
        while not colocado:
            orientacion = random.choice(["horizontal", "vertical"])
            if orientacion == "horizontal":
                fila = random.randint(0, MATRIZ_TAMANIO - 1)
                col = random.randint(0, MATRIZ_TAMANIO - tamano)
                if all(matriz[fila][col + i] == MAR for i in range(tamano)):
                    for i in range(tamano):
                        matriz[fila][col + i] = jugador
                    colocado = True
            else:  # Vertical
                fila = random.randint(0, MATRIZ_TAMANIO - tamano)
                col = random.randint(0, MATRIZ_TAMANIO - 1)
                if all(matriz[fila + i][col] == MAR for i in range(tamano)):
                    for i in range(tamano):
                        matriz[fila + i][col] = jugador
                    colocado = True
    return matriz

def disparar(x, y, matriz_oponente):
    if matriz_oponente[y][x] != MAR:
        matriz_oponente[y][x] = DISPARO_ACERTADO
        return True
    matriz_oponente[y][x] = DISPARO_FALLADO
    return False

def todos_los_barcos_hundidos(matriz):
    return not any(celda not in (MAR, DISPARO_FALLADO, DISPARO_ACERTADO) for fila in matriz for celda in fila)

class BattleshipGame:
    def __init__(self):
        self.jugadores = {}
        self.matriz_j1 = obtener_matriz_inicial()
        self.matriz_j2 = obtener_matriz_inicial()
        self.disparos_restantes_j1 = DISPAROS_INICIALES
        self.disparos_restantes_j2 = DISPAROS_INICIALES
        self.turno_actual = JUGADOR_1
        self.matriz_j1 = colocar_barcos_aleatorios(self.matriz_j1, JUGADOR_1)
        self.matriz_j2 = colocar_barcos_aleatorios(self.matriz_j2, JUGADOR_2)

    def registrar_jugador(self, jugador, nombre):
        if jugador not in [JUGADOR_1, JUGADOR_2]:
            return {"resultado": "error", "mensaje": "Solo se permiten los jugadores J1 y J2."}

        if jugador not in self.jugadores:
            self.jugadores[jugador] = nombre
            inicio.play()  
            return {"resultado": "ok", "mensaje": f"Jugador {jugador} registrado como {nombre}"}

        return {"resultado": "error",
                "mensaje": f"El jugador {jugador} ya está registrado como {self.jugadores[jugador]}"}

    def ambos_jugadores_registrados(self):
        return JUGADOR_1 in self.jugadores and JUGADOR_2 in self.jugadores

    def obtener_disparos_restantes(self, jugador):
        if jugador == JUGADOR_1:
            return self.disparos_restantes_j1
        elif jugador == JUGADOR_2:
            return self.disparos_restantes_j2
        return -1

    def obtener_estado_tablero(self, jugador, mostrar_barcos):
        matriz = self.matriz_j1 if jugador == JUGADOR_1 else self.matriz_j2
        if mostrar_barcos:
            return matriz
        return [
            [celda if celda in (DISPARO_FALLADO, DISPARO_ACERTADO) else MAR for celda in fila]
            for fila in matriz
        ]

    def disparar(self, jugador, x, y):
        if not self.ambos_jugadores_registrados():
            return {"resultado": "error", "mensaje": "Ambos jugadores deben estar registrados para comenzar."}

        if self.turno_actual != jugador:
            return {"resultado": "error", "mensaje": "No es tu turno."}

        if not (0 <= x < MATRIZ_TAMANIO and 0 <= y < MATRIZ_TAMANIO):
            return {"resultado": "error", "mensaje": "Coordenadas fuera de rango."}

        matriz_oponente = self.matriz_j1 if jugador == JUGADOR_2 else self.matriz_j2
        acertado = disparar(x, y, matriz_oponente)

        if jugador == JUGADOR_1:
            self.disparos_restantes_j1 -= 1
        else:
            self.disparos_restantes_j2 -= 1

        if todos_los_barcos_hundidos(matriz_oponente):
            soundtrack.stop()
            winning.play()  
            return {"resultado": "victoria", "mensaje": f"{self.jugadores[jugador]} ha ganado."}

        if self.disparos_restantes_j1 <= 0 or self.disparos_restantes_j2 <= 0:
            return {"resultado": "fin", "mensaje": f"{self.jugadores[jugador]} ha perdido por quedarse sin disparos."}

        if not acertado:
            self.turno_actual = JUGADOR_2 if self.turno_actual == JUGADOR_1 else JUGADOR_1
            return {"resultado": "fallado", "mensaje": "Disparo fallado."}

        return {"resultado": "acertado", "mensaje": "¡Disparo acertado!"}

servidor = SimpleXMLRPCServer(("192.168.200.5", 9000), allow_none=True)
juego = BattleshipGame()
servidor.register_instance(juego)
print("Servidor de Batalla Naval en ejecución...")
servidor.serve_forever()