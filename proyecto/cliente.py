import tkinter as tk
import xmlrpc.client
import pygame

# Inicialización de Pygame para el manejo de audio
pygame.init()
pygame.mixer.init()

# Cargar pistas de audio
sonido_acertado = pygame.mixer.Sound("acertado.wav")
sonido_fallado = pygame.mixer.Sound("fallado.wav")
sonido_inicio = pygame.mixer.Sound("inicio.mp3")
soundtrack = pygame.mixer.Sound("soundtrack.mp3")
sonido_ganador = pygame.mixer.Sound("winning.mp3")

class BattleshipClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente - Batalla Naval")
        self.server = xmlrpc.client.ServerProxy("http://192.168.200.5:9000", allow_none=True)
        self.jugador = ""
        self.nombre = ""
        self.tablero_activo = False
        self.disparos_realizados = 0

        # Mensaje informativo sobre la flota de barcos
        self.info_frame = tk.Frame(self.master)
        self.info_frame.pack(pady=10)
        info_text = (
            "Cada jugador tiene una flota de cinco barcos de diferentes tamaños:\n"
            "- Un portaaviones de 5 agujeros\n"
            "- Un acorazado de 4 agujeros\n"
            "- Un crucero de 3 agujeros\n"
            "- Un submarino de 3 agujeros\n"
            "- Un destructor de 2 agujeros"
        )
        tk.Label(self.info_frame, text=info_text, justify="left", fg="black").pack()

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(pady=10)

        tk.Label(self.board_frame, text="Tu Tablero").grid(row=0, column=0)
        self.tablero_propio_frame = tk.Frame(self.board_frame)
        self.tablero_propio_frame.grid(row=1, column=0, padx=10)
        self.botones_tablero_propio = self.crear_tablero(self.tablero_propio_frame, interactivo=False)

        tk.Label(self.board_frame, text="Tablero del Oponente").grid(row=0, column=1)
        self.tablero_oponente_frame = tk.Frame(self.board_frame)
        self.tablero_oponente_frame.grid(row=1, column=1, padx=10)
        self.botones_tablero_oponente = self.crear_tablero(self.tablero_oponente_frame, interactivo=True)

        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack(pady=10)
        tk.Label(self.entry_frame, text="Jugador (J1/J2):").grid(row=0, column=0)
        self.jugador_entry = tk.Entry(self.entry_frame, width=5)
        self.jugador_entry.grid(row=0, column=1)
        tk.Label(self.entry_frame, text="Nombre:").grid(row=0, column=2)
        self.nombre_entry = tk.Entry(self.entry_frame, width=10)
        self.nombre_entry.grid(row=0, column=3)
        tk.Button(self.entry_frame, text="Registrar", command=self.registrar).grid(row=0, column=4, padx=10)

        self.mensaje_label = tk.Label(self.master, text="", fg="blue")
        self.mensaje_label.pack(pady=5)

        self.disparos_label = tk.Label(self.master, text="Disparos realizados: 0", fg="blue")
        self.disparos_label.pack(pady=5)

    def registrar(self):
        self.jugador = self.jugador_entry.get().strip().upper()
        self.nombre = self.nombre_entry.get().strip()
        if self.jugador not in ["J1", "J2"]:
            self.mensaje_label.config(text="El jugador debe ser J1 o J2.", fg="red")
            return
        registro = self.server.registrar_jugador(self.jugador, self.nombre)
        if registro["resultado"] == "error":
            self.mensaje_label.config(text=registro["mensaje"], fg="red")
        else:
            self.mensaje_label.config(text=registro["mensaje"], fg="blue")
            self.check_otros_jugador_frame()

    def check_otros_jugador_frame(self):
        if self.server.ambos_jugadores_registrados():
            self.mensaje_label.config(text="Ambos jugadores registrados. ¡Comienza el juego!", fg="green")
            self.tablero_activo = True
            sonido_inicio.play()
        else:
            self.mensaje_label.config(text="Esperando al segundo jugador...", fg="orange")

    def crear_tablero(self, frame, interactivo=True):
        botones = []
        for row in range(10):
            fila = []
            for col in range(10):
                boton = tk.Button(frame, text="~", width=3, height=1,
                                  command=(lambda x=col, y=row: self.disparar(x, y)) if interactivo else None)
                boton.grid(row=row, column=col)
                fila.append(boton)
            botones.append(fila)
        return botones

    def disparar(self, x, y):
        if not self.tablero_activo:
            self.mensaje_label.config(text="Espera a que ambos jugadores se registren.", fg="red")
            return

        resultado = self.server.disparar(self.jugador, x, y)
        self.mensaje_label.config(text=resultado["mensaje"], fg="black")

        if resultado["resultado"] == "acertado":
            sonido_acertado.play()
        elif resultado["resultado"] == "fallado":
            sonido_fallado.play()

        self.disparos_realizados += 1
        self.disparos_label.config(text=f"Disparos realizados: {self.disparos_realizados}")

        self.actualizar_tablero_propio()
        self.actualizar_tablero_oponente()

        if resultado["resultado"] == "victoria":
            self.mensaje_label.config(text="¡Has ganado!", fg="green")
            sonido_ganador.play()

    def actualizar_tablero_propio(self):
        tablero = self.server.obtener_estado_tablero(self.jugador, True)
        for i in range(10):
            for j in range(10):
                celda = tablero[i][j]
                color = "green" if celda == "G" else "lightblue"
                self.botones_tablero_propio[i][j].config(text=celda, bg=color)

    def actualizar_tablero_oponente(self):
        tablero = self.server.obtener_estado_tablero(self.jugador, False)
        for i in range(10):
            for j in range(10):
                celda = tablero[i][j]
                color = "lightblue" if celda == "~" else "grey" if celda == "O" else "red"
                self.botones_tablero_oponente[i][j].config(text=celda, bg=color)

root = tk.Tk()
app = BattleshipClient(root)
root.mainloop()
