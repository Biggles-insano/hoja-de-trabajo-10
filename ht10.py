class GrafoLogistica:
    def __init__(self):
        self.vertices = set()
        self.matriz_adyacencia = {}

    def agregar_conexion(self, ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta):
        self.vertices.add(ciudad1)
        self.vertices.add(ciudad2)
        self.matriz_adyacencia[(ciudad1, ciudad2)] = (tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta)

    def quitar_conexion(self, ciudad1, ciudad2):
        if (ciudad1, ciudad2) in self.matriz_adyacencia:
            del self.matriz_adyacencia[(ciudad1, ciudad2)]

    def cambiar_clima(self, ciudad1, ciudad2, nuevo_clima):
        if (ciudad1, ciudad2) in self.matriz_adyacencia:
            tiempos = self.matriz_adyacencia[(ciudad1, ciudad2)]
            self.matriz_adyacencia[(ciudad1, ciudad2)] = tiempos[:nuevo_clima] + (nuevo_clima,) + tiempos[nuevo_clima + 1:]

    def calcular_centro_del_grafo(self):
        # Implementar algoritmo para calcular el centro del grafo
        pass

class ProgramaLogistica:
    def __init__(self, grafo):
        self.grafo = grafo

    def cargar_grafo_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'r') as file:
                for linea in file:
                    datos = linea.strip().split()
                    ciudad1, ciudad2 = datos[0], datos[1]
                    tiempos = tuple(map(int, datos[2:]))
                    self.grafo.agregar_conexion(ciudad1, ciudad2, *tiempos)
        except FileNotFoundError:
            print("El archivo no existe.")

    def calcular_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        # Implementar algoritmo de Floyd para calcular la ruta más corta entre ciudad_origen y ciudad_destino
        pass

    def mostrar_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        ruta_mas_corta = self.calcular_ruta_mas_corta(ciudad_origen, ciudad_destino)
        if ruta_mas_corta:
            print(f"La ruta más corta entre {ciudad_origen} y {ciudad_destino} es {ruta_mas_corta}.")

    def mostrar_centro_del_grafo(self):
        centro = self.grafo.calcular_centro_del_grafo()
        if centro:
            print(f"La ciudad que queda en el centro del grafo es {centro}.")

    def ejecutar(self):
        while True:
            print("Opciones:\n1. Calcular ruta más corta entre dos ciudades\n2. Calcular ciudad central del grafo\n3. Modificar el grafo\n4. Salir")
            opcion = input("Ingrese el número de la opción deseada: ")
            if opcion == '1':
                ciudad_origen = input("Ingrese la ciudad de origen: ")
                ciudad_destino = input("Ingrese la ciudad de destino: ")
                self.mostrar_ruta_mas_corta(ciudad_origen, ciudad_destino)
            elif opcion == '2':
                self.mostrar_centro_del_grafo()
            elif opcion == '3':
                # Implementar la modificación del grafo
                pass
            elif opcion == '4':
                break
            else:
                print("Opción no válida. Por favor, ingrese una opción válida.")

if __name__ == "__main__":
    grafo = GrafoLogistica()
    programa = ProgramaLogistica(grafo)
    programa.cargar_grafo_desde_archivo('logistica.txt')
    programa.ejecutar()
