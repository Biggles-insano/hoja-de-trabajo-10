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
            self.matriz_adyacencia[(ciudad1, ciudad2)] = tiempos[:nuevo_clima] + (nuevo_clima,) + tiempos[nuevo_clima + 1:]

    def calcular_centro_del_grafo(self):
        distancias = self.floyd()
        maximos = [max(distancias[ciudad].values()) for ciudad in self.vertices]
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
        for linea in lineas[1:]:  # Omitir la primera línea
            datos = linea.strip().split(',')
            ciudad1, ciudad2 = datos[0], datos[1]
            tiempos = tuple(map(int, datos[2:]))
            self.grafo.agregar_conexion(ciudad1, ciudad2, tiempos)

    def calcular_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        distancias = self.grafo.floyd()
        if ciudad_origen in distancias and ciudad_destino in distancias[ciudad_origen]:
            ruta = [ciudad_origen]
            while ruta[-1] != ciudad_destino:
                siguiente_ciudad = min((ciudad for ciudad in self.grafo.vertices if ciudad != ruta[-1]), key=lambda ciudad: distancias[ruta[-1]][ciudad])
                ruta.append(siguiente_ciudad)
            return ruta
        else:
            return None

    def mostrar_ruta_mas_corta(self, ciudad_origen, ciudad_destino):
        ruta_mas_corta = self.calcular_ruta_mas_corta(ciudad_origen, ciudad_destino)
        if ruta_mas_corta:
            print(f"La ruta más corta entre {ciudad_origen} y {ciudad_destino} es {ruta_mas_corta}.")

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
    texto_grafo = """
Ciudad1,Ciudad2
BuenosAires,SaoPaulo,10,15,20,50
BuenosAires,Lima,15,20,30,70
Lima,Quito,10,12,15,20
"""
    programa.cargar_grafo_desde_texto(texto_grafo)
    programa.mostrar_matriz_adyacencia()
    ciudad_origen = "BuenosAires"
    ciudad_destino = "Quito"
    programa.mostrar_ruta_mas_corta(ciudad_origen, ciudad_destino)