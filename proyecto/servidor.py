import random
import xmlrpc.server

class BattleshipServer:
    def __init__(self):
        self.jugadores = {}  # Almacena los jugadores registrados
        self.tableros = {}  # Almacena los tableros de los jugadores
        self.barcos = {
            "portaaviones": 5,
            "acorazado": 4,
            "crucero": 3,
            "submarino": 3,
            "destructor": 2
        }
        self.victorias = {"J1": False, "J2": False}
        self.jugadores_registrados = 0  # Control de cuántos jugadores se han registrado

    def registrar_jugador(self, jugador, nombre):
        if self.jugadores_registrados >= 2:
            return {"resultado": "error", "mensaje": "Ya están registrados dos jugadores."}
        
        if jugador in self.jugadores:
            return {"resultado": "error", "mensaje": f"El jugador {jugador} ya está registrado."}

        if jugador not in ["J1", "J2"]:
            return {"resultado": "error", "mensaje": "El jugador debe ser J1 o J2."}

        # Registrar al jugador
        self.jugadores[jugador] = nombre
        self.jugadores_registrados += 1
        self.tableros[jugador] = self.colocar_barcos(jugador)
        
        return {"resultado": "exito", "mensaje": f"Jugador {jugador} ({nombre}) registrado correctamente."}

    def colocar_barcos(self, jugador):
        tablero = [["~" for _ in range(10)] for _ in range(10)]
        
        for barco, tamaño in self.barcos.items():
            colocado = False
            while not colocado:
                direccion = random.choice(["horizontal", "vertical"])
                fila = random.randint(0, 9)
                columna = random.randint(0, 9)
                if direccion == "horizontal":
                    if columna + tamaño <= 10 and all(tablero[fila][columna + i] == "~" for i in range(tamaño)):
                        for i in range(tamaño):
                            tablero[fila][columna + i] = "G"  # G de "barco colocado"
                        colocado = True
                else:
                    if fila + tamaño <= 10 and all(tablero[fila + i][columna] == "~" for i in range(tamaño)):
                        for i in range(tamaño):
                            tablero[fila + i][columna] = "G"  # G de "barco colocado"
                        colocado = True
        
        return tablero

    def obtener_estado_tablero(self, jugador, propio):
        if propio:
            return self.tableros[jugador]
        else:
            oponente = "J1" if jugador == "J2" else "J2"
            return [["~" if celda == "G" else celda for celda in fila] for fila in self.tableros[oponente]]

    def disparar(self, jugador, x, y):
        tablero = self.tableros[jugador]
        resultado = ""
        mensaje = ""

        if tablero[y][x] == "G":
            resultado = "acertado"
            tablero[y][x] = "X"  # Marca el barco como "hundido"
            mensaje = f"¡Acertaste! Has tocado un barco."
        else:
            resultado = "fallado"
            tablero[y][x] = "O"  # Marca el lugar como fallido
            mensaje = "¡Fallaste! No hay barco."

        if self.verificar_victoria(jugador):
            resultado = "victoria"
            mensaje = "¡Has ganado! Has hundido todos los barcos del oponente."
        return {"resultado": resultado, "mensaje": mensaje}

    def verificar_victoria(self, jugador):
        tablero = self.tableros[jugador]
        return all(celda != "G" for fila in tablero for celda in fila)

    def ambos_jugadores_registrados(self):
        return "J1" in self.jugadores and "J2" in self.jugadores


# Crear el servidor
server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
server.register_instance(BattleshipServer())
print("Servidor en ejecución en http://192.168.200.5:9000")
server.serve_forever()
