class Tarea:
    "Modelo de tarea"
    contador = 1

    def __init__(self, descripcion):
        self.id = Tarea.contador
        self.descripcion = descripcion
        Tarea.contador += 1


class GestionTareas:
    "Gestor de lógica para las tareas"

    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, descripcion):
        tarea = Tarea(descripcion)
        self.tareas.append(tarea)
        return tarea

    def obtener_tareas(self):
        return self.tareas

    def eliminar_tarea(self, id_tarea):
        for tarea in self.tareas:
            if tarea.id == id_tarea:
                self.tareas.remove(tarea)
                return True
        return False


class Vista:
    @staticmethod
    def menu():
        print("-----------Bienvenido a Task Manager-----------")
        print("1.- Agregar nueva tarea")
        print("2.- Obtener tareas")
        print("3.- Eliminar tarea")
        print("4.- Salir")

    @staticmethod
    def mostrar_tareas(tareas):
        if not tareas:
            print("No existen tareas actualmente")
        else:
            print("Listado de tareas actuales: ")
            for tarea in tareas:
                print(f"Id: {tarea.id}, Descripción: {tarea.descripcion}")

    @staticmethod
    def pedir_descripcion():
        return input("Ingrese la descripción de la nueva tarea: ")

    @staticmethod
    def pedir_id_tarea():
        try:
            return int(input("Ingresa el ID de la tarea que quieras eliminar: "))
        except ValueError:
            print("Id no válido, ingresa un ID válido por favor")
            return None

    @staticmethod
    def mensaje_usuario(mensaje):
        print(f"{mensaje}")


class Controlador:

    def __init__(self):
        self.gestion_tareas = GestionTareas()
        self.vista = Vista()

    def ejecucion(self):
        while True:
            self.vista.menu()
            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                self.vista.mensaje_usuario("Opción no válida, por favor ingrese un número.")
                continue

            if opcion == 1:
                descripcion = self.vista.pedir_descripcion()
                if descripcion:
                    tarea = self.gestion_tareas.agregar_tarea(descripcion)
                    self.vista.mensaje_usuario(f"Tarea agregada con éxito: ID {tarea.id}, Descripción: {tarea.descripcion}")

            elif opcion == 2:
                tareas = self.gestion_tareas.obtener_tareas()
                self.vista.mostrar_tareas(tareas)

            elif opcion == 3:
                id_tarea = self.vista.pedir_id_tarea()
                if id_tarea is not None:
                    exito = self.gestion_tareas.eliminar_tarea(id_tarea)
                    if exito:
                        self.vista.mensaje_usuario("La tarea ha sido eliminada")
                    else:
                        self.vista.mensaje_usuario("No se encontró la tarea")

            elif opcion == 4:
                self.vista.mensaje_usuario("Saliendo de TaskManager...")
                break

            else:
                self.vista.mensaje_usuario("Opción no válida, vuelve a ingresar la opción")


if __name__ == "__main__":
    controlador = Controlador()
    controlador.ejecucion()
