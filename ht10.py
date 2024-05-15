class GrafoLogistica:
    def __init__(self):
        self.vertices = set()
        self.matriz_adyacencia = {}

    def agregar_conexion(self, ciudad1, ciudad2, tiempos):
        self.vertices.add(ciudad1)
        self.vertices.add(ciudad2)
        self.matriz_adyacencia[(ciudad1, ciudad2)] = tiempos

    def quitar_conexion(self, ciudad1, ciudad2):
        if (ciudad1, ciudad2) in self.matriz_adyacencia:
            del self.matriz_adyacencia[(ciudad1, ciudad2)]

    def cambiar_clima(self, ciudad1, ciudad2, nuevo_clima):
        if (ciudad1, ciudad2) in self.matriz_adyacencia:
            tiempos = self.matriz_adyacencia[(ciudad1, ciudad2)]
            self.matriz_adyacencia[(ciudad1, ciudad2)] = (
                    tiempos[:nuevo_clima] + (nuevo_clima,) + tiempos[nuevo_clima + 1:])

    def calcular_centro_del_grafo(self):
        if not self.vertices:
            return "No vertices in the graph."
        distancias = self.floyd()
        [max(distancias[ciudad].values()) for ciudad in self.vertices]
        centro = min(self.vertices, key=lambda ciudad: max(distancias[ciudad].values()))
        return centro

    def floyd(self):
        inf = float('inf')
        distancias = {v: {u: inf for u in self.vertices} for v in self.vertices}
        for v, u in self.matriz_adyacencia.keys():
            distancias[v][u] = min(self.matriz_adyacencia[(v, u)])
        for v in self.vertices:
            distancias[v][v] = 0
        for k in self.vertices:
            for v in self.vertices:
                for u in self.vertices:
                    distancias[v][u] = min(distancias[v][u], distancias[v][k] + distancias[k][u])
        return distancias


class ProgramaLogistica:
    def __init__(self, grafo):
        self.grafo = grafo

    def cargar_grafo_desde_texto(self, texto_grafo):
        lineas = texto_grafo.strip().split('\n')
        for linea in lineas:
            datos = linea.strip().split(',')
            if len(datos) == 6:
                ciudad1, ciudad2, tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta = datos
                tiempos = (int(tiempo_normal), int(tiempo_lluvia), int(tiempo_nieve), int(tiempo_tormenta))
                self.grafo.agregar_conexion(ciudad1, ciudad2, tiempos)

    def cargar_grafo_desde_archivo(self, ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            texto_grafo = archivo.read()
            self.cargar_grafo_desde_texto(texto_grafo)

    def calcular_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        distancias = self.grafo.floyd()
        if ciudad_origen in distancias and ciudad_destino in distancias[ciudad_origen]:
            ruta = [ciudad_origen]
            while ruta[-1] != ciudad_destino:
                siguiente_ciudad = min((ciudad for ciudad in self.grafo.vertices if ciudad not in ruta),
                                       key=lambda ciudad: distancias[ruta[-1]][ciudad] + distancias[ciudad][
                                           ciudad_destino])
                ruta.append(siguiente_ciudad)
            return ruta
        else:
            return None

    def mostrar_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        ruta_mas_corta = self.calcular_ruta_mas_corta(ciudad_origen, ciudad_destino)
        if ruta_mas_corta:
            print(f"La ruta más corta entre {ciudad_origen} y {ciudad_destino} es {ruta_mas_corta}.")
        else:
            print(f"No se encontró una ruta entre {ciudad_origen} y {ciudad_destino}.")

    def ejecutar_menu(self):
        while True:
            print("\n--- Menú ---")
            print("1. Calcular ruta más corta")
            print("2. Mostrar centro del grafo")
            print("3. Modificar grafo")
            print("4. Imprimir matriz de adyacencia")
            print("5. Salir")
            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                ciudad_origen = input("Ingrese la ciudad de origen: ")
                ciudad_destino = input("Ingrese la ciudad de destino: ")
                self.mostrar_ruta_mas_corta(ciudad_origen, ciudad_destino)
            elif opcion == "2":
                centro_grafo = self.grafo.calcular_centro_del_grafo()
                if centro_grafo == "No hay vértices en el grafo.":
                    print(centro_grafo)
                else:
                    print(f"El centro del grafo es: {centro_grafo}")
            elif opcion == "3":
                self.modificar_grafo()
            elif opcion == "4":
                self.mostrar_matriz_adyacencia()
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def modificar_grafo(self):
        while True:
            print("\n--- Modificar Grafo ---")
            print("1. Interrumpir tráfico entre ciudades")
            print("2. Establecer conexión entre ciudades")
            print("3. Cambiar clima entre ciudades")
            print("4. Regresar al menú principal")
            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                self.grafo.quitar_conexion(ciudad1, ciudad2)
                print("Conexión interrumpida exitosamente.")
            elif opcion == "2":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                tiempo_normal = int(input("Ingrese el tiempo normal: "))
                tiempo_lluvia = int(input("Ingrese el tiempo con lluvia: "))
                tiempo_nieve = int(input("Ingrese el tiempo con nieve: "))
                tiempo_tormenta = int(input("Ingrese el tiempo con tormenta: "))
                tiempos = (tiempo_normal, tiempo_lluvia, tiempo_nieve, tiempo_tormenta)
                self.grafo.agregar_conexion(ciudad1, ciudad2, tiempos)
                print("Conexión establecida exitosamente.")
            elif opcion == "3":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                nuevo_clima = input("Ingrese el nuevo clima (normal, lluvia, nieve, tormenta): ")
                clima_opciones = {"normal": 0, "lluvia": 1, "nieve": 2, "tormenta": 3}
                if nuevo_clima in clima_opciones:
                    nuevo_clima_idx = clima_opciones[nuevo_clima]
                    self.grafo.cambiar_clima(ciudad1, ciudad2, nuevo_clima_idx)
                    print("Clima actualizado exitosamente.")
                else:
                    print("Opción de clima inválida.")
            elif opcion == "4":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def mostrar_matriz_adyacencia(self):
        vertices = sorted(list(self.grafo.vertices))
        print("Matriz de adyacencia:")
        print(" " + " ".join(vertices))
        for v in vertices:
            fila = []
            for u in vertices:
                if (v, u) in self.grafo.matriz_adyacencia:
                    fila.append(str(self.grafo.matriz_adyacencia[(v, u)]))
                else:
                    fila.append("-")
            print(f"{v}: {' '.join(fila)}")


if __name__ == "__main__":
    grafo = GrafoLogistica()
    programa = ProgramaLogistica(grafo)
    programa.cargar_grafo_desde_archivo('logistica.txt')
    programa.ejecutar_menu()
